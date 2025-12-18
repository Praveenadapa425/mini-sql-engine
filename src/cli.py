"""
Command-Line Interface for the mini SQL engine.
Provides an interactive REPL for executing SQL queries.
"""

from .parser import SQLParser
from .engine import SQLEngine, format_results
from .exceptions import SQLError

def show_help():
    """Display help information."""
    help_text = """
Mini SQL Engine CLI
==================

Supported Commands:
1. LOAD filename.csv          - Load a CSV file as a table
2. SELECT * FROM table;       - Select all columns from a table
3. SELECT col1, col2 FROM table; - Select specific columns
4. SELECT * FROM table WHERE condition; - Filter rows with WHERE clause
5. SELECT COUNT(*) FROM table; - Count all rows
6. SELECT COUNT(col) FROM table; - Count non-null values in a column
7. help                      - Show this help message
8. exit, quit, q             - Exit the application

WHERE Clause Conditions:
- Operators: =, !=, >, <, >=, <=
- String values should be quoted: WHERE country = 'USA'
- Numeric values: WHERE age > 30

Examples:
- LOAD employees.csv;
- SELECT * FROM employees;
- SELECT name, age FROM employees WHERE age > 30;
- SELECT COUNT(*) FROM employees WHERE country = 'USA';
"""
    print(help_text)

def main():
    """Main CLI loop."""
    print("Mini SQL Engine CLI")
    print("Type 'help' for available commands or 'exit' to quit.")
    print()
    
    # Initialize components
    parser = SQLParser()
    engine = SQLEngine()
    
    while True:
        try:
            # Get user input
            query = input("sql> ").strip()
            
            # Handle empty input
            if not query:
                continue
                
            # Handle exit commands
            if query.lower() in ['exit', 'quit', 'q']:
                print("Goodbye!")
                break
            
            # Handle help command
            if query.lower() == 'help':
                show_help()
                continue
            
            # Parse and execute query
            try:
                parsed_query = parser.parse(query)
                result = engine.execute_query(parsed_query)
                print(format_results(result))
            except SQLError as e:
                print(f"SQL Error: {e}")
            except Exception as e:
                print(f"Error: {e}")
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except EOFError:
            print("\nGoodbye!")
            break
        
        print()  # Empty line for readability

if __name__ == "__main__":
    main()