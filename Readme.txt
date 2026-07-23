PQS Order Calculator Build Instructions

Required Python version:
Python 3. The project was verified with Python 3.12.

Create and activate a virtual environment on macOS:
python3 -m venv .venv
source .venv/bin/activate

Install requirements:
python3 -m pip install -r requirements.txt

Run standard CI mode:
python3 build.py

Standard CI mode cleans previous outputs, compiles app.py and order_calculator.py, and runs pytest. Because Assessment 2 intentionally includes two failing tests, this mode reports the test failure and exits with a non-zero status. This is the mode intended for later Jenkins use.

Run assessment packaging mode:
python3 build.py --continue-on-test-failure

Assessment packaging mode cleans previous outputs, compiles the source files, runs pytest, reports the expected result of three passed tests and two failed tests, and continues to package the application with PyInstaller.

The two failing tests are intentional for Assessment 2. They demonstrate that automated testing detects incorrect expectations: one outdated shipping expectation and one incorrect tax expectation.

Executable output:
The packaged executable is created at:
dist/PQSOrderCalculator

Run the executable on macOS:
./dist/PQSOrderCalculator
