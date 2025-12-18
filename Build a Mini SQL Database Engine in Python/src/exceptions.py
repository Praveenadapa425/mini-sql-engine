"""
Custom exceptions for the Mini SQL Engine.
"""

class SQLError(Exception):
    """Base exception for SQL-related errors."""
    pass

class ParseError(SQLError):
    """Exception raised for errors in SQL parsing."""
    pass

class ExecutionError(SQLError):
    """Exception raised for errors in query execution."""
    pass

class TableNotFoundError(ExecutionError):
    """Exception raised when a table is not found."""
    pass

class ColumnNotFoundError(ExecutionError):
    """Exception raised when a column is not found."""
    pass

class FileLoadError(ExecutionError):
    """Exception raised when a file cannot be loaded."""
    pass