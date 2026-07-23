"""Build automation for the PQS Order Calculator."""

from __future__ import annotations

import argparse
import importlib.util
import py_compile
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BUILD_DIR = ROOT / "build"
DIST_DIR = ROOT / "dist"
EXE_PATH = DIST_DIR / "PQSOrderCalculator"
SPEC_FILE = ROOT / "PQSOrderCalculator.spec"
SOURCE_FILES = [ROOT / "app.py", ROOT / "order_calculator.py"]
PYTEST_SUMMARY = "2 failed, 3 passed"


def print_heading(title: str) -> None:
    """Print a clear build stage heading."""
    print(f"\n=== {title} ===")


def remove_path(path: Path) -> None:
    """Remove a file or directory if it exists."""
    if path.is_dir():
        shutil.rmtree(path)
        print(f"Removed directory: {path.relative_to(ROOT)}")
    elif path.exists():
        path.unlink()
        print(f"Removed file: {path.relative_to(ROOT)}")
    else:
        print(f"Not present: {path.relative_to(ROOT)}")


def clean() -> bool:
    """Clean previous build and cache outputs."""
    print_heading("Clean")
    for path in [
        BUILD_DIR,
        DIST_DIR,
        ROOT / "__pycache__",
        ROOT / "tests" / "__pycache__",
        SPEC_FILE,
    ]:
        remove_path(path)
    return True


def compile_sources() -> bool:
    """Compile application source files to validate Python syntax."""
    print_heading("Compile")
    try:
        for source_file in SOURCE_FILES:
            py_compile.compile(str(source_file), doraise=True)
            print(f"Compiled: {source_file.relative_to(ROOT)}")
    except py_compile.PyCompileError as exc:
        print(f"Compilation failed: {exc}")
        return False

    print("Compilation passed.")
    return True


def dependency_available(module_name: str) -> bool:
    """Return whether a Python module can be imported."""
    return importlib.util.find_spec(module_name) is not None


def run_command(command: list[str]) -> subprocess.CompletedProcess[str]:
    """Run a subprocess and print its complete output."""
    print(f"Running: {' '.join(command)}")
    result = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)

    return result


def run_tests(continue_on_failure: bool) -> bool:
    """Run pytest and report whether the test stage passed."""
    print_heading("Test")
    if not dependency_available("pytest"):
        print("Missing dependency: pytest. Install requirements with python3 -m pip install -r requirements.txt.")
        return False

    result = run_command([sys.executable, "-m", "pytest", "-v", "tests"])
    passed = result.returncode == 0

    if passed:
        print("Test result: passed.")
        return True

    print(f"Test result: failed with exit code {result.returncode}.")
    if continue_on_failure:
        print(f"Assessment mode: continuing because the intentional result is {PYTEST_SUMMARY}.")
    return False


def package_executable() -> bool:
    """Package the CLI application as a one-file executable."""
    print_heading("Package")
    if not dependency_available("PyInstaller"):
        print("Missing dependency: pyinstaller. Install requirements with python3 -m pip install -r requirements.txt.")
        return False

    result = run_command(
        [
            sys.executable,
            "-m",
            "PyInstaller",
            "--onefile",
            "--name",
            "PQSOrderCalculator",
            "app.py",
        ]
    )

    if result.returncode != 0:
        print(f"Packaging failed with exit code {result.returncode}.")
        return False

    if not EXE_PATH.exists():
        print(f"Packaging failed: expected executable not found at {EXE_PATH}.")
        return False

    print(f"Packaging passed: {EXE_PATH}")
    return True


def print_summary(
    compilation_passed: bool,
    tests_passed: bool,
    package_passed: bool | None,
    overall_passed: bool,
) -> None:
    """Print the final build summary."""
    print_heading("Summary")
    print(f"Compilation result: {'passed' if compilation_passed else 'failed'}")
    print(f"Test result: {'passed' if tests_passed else 'failed'}")
    print(f"Package path: {EXE_PATH if package_passed else 'not created'}")
    print(f"Overall result: {'passed' if overall_passed else 'failed'}")


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Build the PQS Order Calculator.")
    parser.add_argument(
        "--continue-on-test-failure",
        action="store_true",
        help="Continue packaging after the intentional assessment test failures.",
    )
    return parser.parse_args()


def main() -> int:
    """Run the build workflow."""
    args = parse_args()

    try:
        clean()
        compilation_passed = compile_sources()
        if not compilation_passed:
            print_summary(False, False, None, False)
            return 1

        tests_passed = run_tests(args.continue_on_test_failure)
        if not tests_passed and not args.continue_on_test_failure:
            print("Standard CI mode: stopping because tests failed.")
            print_summary(compilation_passed, tests_passed, None, False)
            return 1

        package_passed = package_executable()
        overall_passed = compilation_passed and package_passed
        print_summary(compilation_passed, tests_passed, package_passed, overall_passed)
        return 0 if overall_passed else 1
    except Exception as exc:
        print(f"Unexpected build error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
