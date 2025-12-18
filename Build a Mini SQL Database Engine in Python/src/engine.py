"""
Query Execution Engine for the mini SQL engine.
Handles data loading, filtering, and projection.
"""

import csv
import os
from tabulate import tabulate
from .exceptions import TableNotFoundError, ColumnNotFoundError, FileLoadError

class SQLEngine:
    def __init__(self):
        # In-memory storage for tables
        self.tables = {}
    
    def load_csv(self, filename):
        """
        Load a CSV file into memory as a table.
        
        Args:
            filename (str): Path to the CSV file
            
        Returns:
            str: Name of the loaded table
        """
        if not os.path.exists(filename):
            raise FileLoadError(f"File '{filename}' not found")
        
        # Derive table name from filename (without extension)
        table_name = os.path.splitext(os.path.basename(filename))[0]
        
        # Load CSV data into a list of dictionaries
        with open(filename, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            self.tables[table_name] = list(reader)
        
        return table_name
    
    def execute_query(self, parsed_query):
        """
        Execute a parsed SQL query.
        
        Args:
            parsed_query (dict): The parsed query from SQLParser
            
        Returns:
            list or int: Query results (rows or count)
        """
        if parsed_query['command'] == 'LOAD':
            filename = parsed_query['filename']
            table_name = self.load_csv(filename)
            return f"Table '{table_name}' loaded successfully from '{filename}'"
        
        if parsed_query['command'] == 'SELECT':
            table_name = parsed_query['from_table']
            
            # Check if table exists
            if table_name not in self.tables:
                raise TableNotFoundError(f"Table '{table_name}' not found. Please load it first.")
            
            # Get all rows from the table
            rows = self.tables[table_name][:]
            
            # Apply WHERE filter if present
            if parsed_query['where_clause']:
                rows = self._filter_rows(rows, parsed_query['where_clause'])
            
            # Handle COUNT function
            if isinstance(parsed_query['select_cols'], list) and \
               len(parsed_query['select_cols']) == 1 and \
               isinstance(parsed_query['select_cols'][0], dict) and \
               parsed_query['select_cols'][0].get('function') == 'COUNT':
                
                column = parsed_query['select_cols'][0]['column']
                if column == '*':
                    return len(rows)  # Count all rows
                else:
                    # Count non-null values in specified column
                    count = 0
                    for row in rows:
                        if column in row and row[column] != '':
                            count += 1
                    return count
            
            # Handle regular SELECT projection
            select_cols = parsed_query['select_cols']
            if select_cols == '*':
                # Select all columns
                return rows
            else:
                # Select specific columns
                projected_rows = []
                for row in rows:
                    projected_row = {}
                    for col in select_cols:
                        if col in row:
                            projected_row[col] = row[col]
                        else:
                            raise ColumnNotFoundError(f"Column '{col}' not found in table '{table_name}'")
                    projected_rows.append(projected_row)
                return projected_rows
        
        raise ValueError("Unsupported command")
    
    def _filter_rows(self, rows, where_clause):
        """
        Filter rows based on a WHERE clause.
        
        Args:
            rows (list): List of row dictionaries
            where_clause (dict): Parsed WHERE clause
            
        Returns:
            list: Filtered rows
        """
        column = where_clause['column']
        operator = where_clause['operator']
        value = where_clause['value']
        
        filtered_rows = []
        
        for row in rows:
            # Check if column exists in row
            if column not in row:
                raise ColumnNotFoundError(f"Column '{column}' not found in table")
            
            row_value = row[column]
            
            # Try to convert both values to numbers for comparison
            try:
                # Convert row value to appropriate numeric type
                if '.' in str(row_value):
                    row_value = float(row_value)
                else:
                    row_value = int(row_value)
                
                # Convert comparison value if it's a string
                if isinstance(value, str):
                    if '.' in value:
                        value = float(value)
                    else:
                        value = int(value)
            except (ValueError, TypeError):
                # If conversion fails, keep as strings
                pass
            
            # Perform comparison based on operator
            match = False
            try:
                if operator == '=':
                    match = row_value == value
                elif operator == '!=':
                    match = row_value != value
                elif operator == '>':
                    match = row_value > value
                elif operator == '<':
                    match = row_value < value
                elif operator == '>=':
                    match = row_value >= value
                elif operator == '<=':
                    match = row_value <= value
            except TypeError:
                raise ExecutionError(f"Cannot compare '{row_value}' with '{value}' using operator '{operator}'")
            
            if match:
                filtered_rows.append(row)
        
        return filtered_rows

def format_results(results):
    """
    Format query results for display.
    
    Args:
        results: Query results (list of dicts or integer)
        
    Returns:
        str: Formatted results as string
    """
    if isinstance(results, int):
        # For COUNT queries
        return str(results)
    elif isinstance(results, str):
        # For LOAD commands
        return results
    elif isinstance(results, list):
        if not results:
            return "No results found"
        # For SELECT queries
        headers = list(results[0].keys())
        rows = [list(row.values()) for row in results]
        return tabulate(rows, headers=headers, tablefmt="grid")
    else:
        return str(results)

if __name__ == "__main__":
    # Example usage
    engine = SQLEngine()
    
    # For testing purposes, create a sample data structure
    engine.tables['employees'] = [
        {'id': '1', 'name': 'John', 'age': '30', 'country': 'USA'},
        {'id': '2', 'name': 'Jane', 'age': '25', 'country': 'Canada'},
        {'id': '3', 'name': 'Bob', 'age': '35', 'country': 'USA'},
        {'id': '4', 'name': 'Alice', 'age': '28', 'country': 'UK'}
    ]
    
    # Test data
    test_queries = [
        {'command': 'SELECT', 'select_cols': '*', 'from_table': 'employees', 'where_clause': None},
        {'command': 'SELECT', 'select_cols': ['name', 'age'], 'from_table': 'employees', 'where_clause': {'column': 'age', 'operator': '>', 'value': 30}},
        {'command': 'SELECT', 'select_cols': [{'function': 'COUNT', 'column': '*'}], 'from_table': 'employees', 'where_clause': None}
    ]
    
    for query in test_queries:
        try:
            result = engine.execute_query(query)
            print(format_results(result))
            print()
        except Exception as e:
            print(f"Error executing query: {e}")