# DOT503 Assessment 2

## PQS Order Calculator

PQS Order Calculator is a small Python 3 command-line application for calculating a sample customer order. It separates the command-line interface in `app.py` from the business logic in `order_calculator.py`.

The calculator validates item data, calculates a subtotal, applies a discount, adds simple shipping, calculates tax, and prints the final total. Monetary calculations use Python's `Decimal` type.

## Project Structure

```text
DOT503-Assessment-2/
├── app.py
├── order_calculator.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Requirements

- Python 3
- No third-party runtime packages

## Run the Application

From the project directory, run:

```bash
python3 app.py
```
