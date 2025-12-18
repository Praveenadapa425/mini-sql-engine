"""
SQL Parser for the mini SQL engine.
Handles parsing of SELECT, FROM, and WHERE clauses.
"""

import re
from .exceptions import ParseError

class SQLParser:
    def __init__(self):
        pass
    
    def parse(self, query):
        """
        Parse a SQL query string and return a structured representation.
        
        Args:
            query (str): The SQL query to parse
            
        Returns:
            dict: A dictionary containing parsed components
        """
        # Convert to uppercase for easier keyword detection
        query = query.strip()
        
        # Check if it's a LOAD command
        if query.upper().startswith('LOAD '):
            filename = query[5:].strip().strip(';')
            return {
                'command': 'LOAD',
                'filename': filename
            }
        
        # Check if it's a COUNT query
        count_match = re.match(r'SELECT\s+COUNT\s*\(\s*(.*?)\s*\)\s+FROM\s+(\w+)(?:\s+WHERE\s+(.+?))?;?$', 
                              query, re.IGNORECASE)
        if count_match:
            column, table, where_clause = count_match.groups()
            return {
                'command': 'SELECT',
                'select_cols': [{'function': 'COUNT', 'column': column.strip()}],
                'from_table': table.strip(),
                'where_clause': self._parse_where(where_clause) if where_clause else None
            }
        
        # Regular SELECT query
        select_match = re.match(r'SELECT\s+(.+?)\s+FROM\s+(\w+)(?:\s+WHERE\s+(.+?))?;?$', 
                               query, re.IGNORECASE)
        if select_match:
            columns, table, where_clause = select_match.groups()
            
            # Handle SELECT *
            if columns.strip() == '*':
                select_cols = '*'
            else:
                # Split columns by comma and clean up
                select_cols = [col.strip() for col in columns.split(',')]
            
            return {
                'command': 'SELECT',
                'select_cols': select_cols,
                'from_table': table.strip(),
                'where_clause': self._parse_where(where_clause) if where_clause else None
            }
        
        raise ParseError("Unsupported SQL query format")
    
    def _parse_where(self, where_clause):
        """
        Parse a WHERE clause into column, operator, and value.
        
        Args:
            where_clause (str): The WHERE clause to parse
            
        Returns:
            dict: A dictionary with column, operator, and value
        """
        # Define supported operators in order of precedence (longest first)
        operators = ['>=', '<=', '!=', '=', '>', '<']
        
        for op in operators:
            if op in where_clause:
                parts = where_clause.split(op, 1)
                if len(parts) == 2:
                    column = parts[0].strip()
                    value = parts[1].strip()
                    
                    # Handle quoted strings
                    if (value.startswith("'") and value.endswith("'")) or \
                       (value.startswith('"') and value.endswith('"')):
                        value = value[1:-1]  # Remove quotes
                    else:
                        # Try to convert to number if possible
                        try:
                            if '.' in value:
                                value = float(value)
                            else:
                                value = int(value)
                        except ValueError:
                            pass  # Keep as string
                    
                    return {
                        'column': column,
                        'operator': op,
                        'value': value
                    }
        
        raise ParseError("Invalid WHERE clause format")

if __name__ == "__main__":
    # Example usage
    parser = SQLParser()
    
    # Test queries
    queries = [
        "SELECT * FROM employees;",
        "SELECT name, age FROM employees WHERE age > 30;",
        "SELECT COUNT(*) FROM employees;",
        "SELECT COUNT(name) FROM employees WHERE country = 'USA';"
    ]
    
    for query in queries:
        try:
            result = parser.parse(query)
            print(f"Query: {query}")
            print(f"Parsed: {result}")
            print()
        except Exception as e:
            print(f"Error parsing '{query}': {e}")