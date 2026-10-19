# Inventory and Sales Management System

A command-line Python project for practicing inventory, sales, JSON persistence, validation, and automated tests.

## Requirements
- Python 3.10+
- No third-party packages

## Start the application
```bash
python main.py
```

## Run tests
```bash
python -m unittest discover -s tests -v
```

## Features
- Add products with unique SKUs
- List and search products
- Restock products
- Record sales and reduce inventory
- Prevent sales beyond available stock
- Identify low-stock products
- Display revenue and sales summaries
- Persist records to a JSON file

## Suggested improvements
- Add product categories and suppliers
- Add date/time to sales
- Export reports to CSV
- Add discounts and tax calculation
- Add SQLite or PostgreSQL storage
- Build a FastAPI backend and React frontend
