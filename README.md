# Mini SQL Database Engine

A simplified, in-memory SQL query engine implemented in Python. This project demonstrates fundamental database concepts by implementing a basic SQL parser and execution engine.

This lightweight database engine allows you to load CSV files as tables and perform SQL-like queries on them directly in memory, without requiring a traditional database server.

## Features

- Load CSV files as database tables
- SELECT queries with column projection (\* or specific columns)
- WHERE clause filtering with comparison operators (=, !=, >, <, >=, <=)
- COUNT() aggregate function for row counting
- Interactive command-line interface (CLI)

## Supported SQL Grammar

### Data Loading
```
LOAD filename.csv;
```

### SELECT Queries
```
-- Select all columns
SELECT * FROM table_name;

-- Select specific columns
SELECT column1, column2 FROM table_name;

-- Select with WHERE clause
SELECT * FROM table_name WHERE condition;

-- Count all rows
SELECT COUNT(*) FROM table_name;

-- Count non-null values in a column
SELECT COUNT(column_name) FROM table_name;
```

### WHERE Clause Conditions
Supported operators:
- Equal: `=`
- Not equal: `!=`
- Greater than: `>`
- Less than: `<`
- Greater than or equal: `>=`
- Less than or equal: `<=`

String values must be quoted:
```
WHERE country = 'India'
```

Numeric comparisons:
```
WHERE age > 30
```

### Additional Notes
- Table names are derived from the CSV filename (without extension)
- All data is stored in memory and will be lost when the program exits
- Column names are case-sensitive and must match exactly as they appear in the CSV header

## Installation

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the CLI application:
```
python -m src.cli
```

Or alternatively:
```
cd src
python cli.py
```

### Example Session

```
sql> LOAD sample_data/employees.csv;
Table 'employees' loaded successfully from 'sample_data/employees.csv'
```
sql> SELECT * FROM employees;
+----+------------------+-----+---------+--------------+--------+
| id | name             | age | country | department   | salary |
+====+==================+=====+=========+==============+========+
| 1  | Praveen Adapa    | 38  | India   | Engineering  | 75000  |
+----+------------------+-----+---------+--------------+--------+
| 2  | Datta mani       | 25  | India   | Marketing    | 65000  |
+----+------------------+-----+---------+--------------+--------+
| 3  | Naruto Uzimaki   | 36  | Japan   | Engineering  | 80000  |
+----+------------------+-----+---------+--------------+--------+
| 4  | Swamy Reddy      | 35  | India   | Sales        | 70000  |
+----+------------------+-----+---------+--------------+--------+
| 5  | sasuke uchiha    | 42  | USA     | Management   | 95000  |
+----+------------------+-----+---------+--------------+--------+
| 6  | Rock Lee         | 31  | Canada  | Engineering  | 72000  |
+----+------------------+-----+---------+--------------+--------+
| 7  | Might Guy        | 29  | UK      | Marketing    | 68000  |
+----+------------------+-----+---------+--------------+--------+
| 8  | Baruto Uzumaki   | 38  | Japan   | Sales        | 77000  |
+----+------------------+-----+---------+--------------+--------+
| 9  | Kakashi Hatake   | 45  | Japan   | Engineering  | 85000  |
+----+------------------+-----+---------+--------------+--------+

sql> SELECT name, age FROM employees WHERE age > 30;
+------------------+-----+
| name             | age |
+==================+=====+
| Praveen Adapa    | 38  |
+------------------+-----+
| Naruto Uzimaki   | 36  |
+------------------+-----+
| Swamy Reddy      | 35  |
+------------------+-----+
| sasuke uchiha    | 42  |
+------------------+-----+
| Baruto Uzumaki   | 38  |
+------------------+-----+
| Kakashi Hatake   | 45  |
+------------------+-----+

sql> SELECT COUNT(*) FROM employees;
9

sql> SELECT COUNT(*) FROM employees WHERE country = 'USA';
1
```

## Project Structure

```
.
├── sample_data/
│   ├── employees.csv
│   └── products.csv
├── src/
│   ├── __init__.py
│   ├── cli.py
│   ├── engine.py
│   ├── exceptions.py
│   └── parser.py
├── .gitignore
├── README.md
└── requirements.txt
```

## Dependencies

- Python 3.7+
- tabulate (>=0.8.0): For formatted table output

## License

This project is open source and available under the MIT License.
