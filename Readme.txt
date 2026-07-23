PQS Order Calculator Build Instructions

Project Overview

The PQS Order Calculator is a Python 3 command-line application used to demonstrate source control, unit testing, build automation, and executable packaging for DOT503 Assessment 2.

Required Software

- Python 3
- pip
- macOS Terminal

The project was verified using Python 3.12.

Create and Activate a Virtual Environment

From the project root directory, run:

python3 -m venv .venv
source .venv/bin/activate

Install Project Requirements

Run:

python3 -m pip install -r requirements.txt

This installs pytest for unit testing and PyInstaller for executable packaging.

Standard CI Mode

Run:

python3 build.py

The standard CI mode performs the following stages:

1. Cleans previous build outputs.
2. Compiles and validates app.py and order_calculator.py.
3. Runs all five pytest unit tests.
4. Stops with a non-zero exit status if any test fails.

Assessment 2 intentionally includes two failing tests. Therefore, standard CI mode is expected to report:

3 passed
2 failed

This behaviour demonstrates that automated testing correctly detects incorrect expectations. It is also the mode intended for later use with Jenkins in Assessment 3.

Assessment Packaging Mode

Run:

python3 build.py --continue-on-test-failure

The assessment packaging mode performs the same clean, compile, and test stages, but continues to package the application after confirming the expected Assessment 2 result of three passed tests and two failed tests.

The two intentional failures demonstrate:

- an outdated shipping expectation
- an incorrect tax expectation

The build continues only because the --continue-on-test-failure option was explicitly supplied.

Executable Location

After a successful packaging build, the executable is created at:

dist/PQSOrderCalculator

Run the Executable

On macOS, run:

./dist/PQSOrderCalculator

Expected Output

PQS Order Calculator
Subtotal: $74.48
Discount: $7.45
Shipping: $6.50
Tax: $7.35
Final total: $80.88

Troubleshooting

If pytest or PyInstaller is not available, confirm that the virtual environment is active and reinstall the requirements:

python3 -m pip install -r requirements.txt

If permission is denied when running the executable, run:

chmod +x dist/PQSOrderCalculator

Then try again:

./dist/PQSOrderCalculator

Deactivate the Virtual Environment

When finished, run:

deactivate
