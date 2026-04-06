"""
Logging utilities for the data cleaning tool.
"""

import logging
import os
from datetime import datetime
from typing import Optional
from config.settings import LOGGING_CONFIG

class DataCleaningLogger:
    """Custom logger for the data cleaning application."""
    
    def __init__(self, name: str = "data_cleaning_tool"):
        self.logger = logging.getLogger(name)
        self.setup_logger()
    
    def setup_logger(self):
        """Setup logger with file and console handlers."""
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # Set logging level
        self.logger.setLevel(getattr(logging, LOGGING_CONFIG["level"]))
        
        # Create formatter
        formatter = logging.Formatter(LOGGING_CONFIG["format"])
        
        # File handler
        os.makedirs(os.path.dirname(LOGGING_CONFIG["file_path"]), exist_ok=True)
        file_handler = logging.FileHandler(LOGGING_CONFIG["file_path"])
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
    
    def info(self, message: str, extra_data: Optional[dict] = None):
        """Log info message."""
        if extra_data:
            message = f"{message} | Extra: {extra_data}"
        self.logger.info(message)
    
    def warning(self, message: str, extra_data: Optional[dict] = None):
        """Log warning message."""
        if extra_data:
            message = f"{message} | Extra: {extra_data}"
        self.logger.warning(message)
    
    def error(self, message: str, extra_data: Optional[dict] = None):
        """Log error message."""
        if extra_data:
            message = f"{message} | Extra: {extra_data}"
        self.logger.error(message)
    
    def debug(self, message: str, extra_data: Optional[dict] = None):
        """Log debug message."""
        if extra_data:
            message = f"{message} | Extra: {extra_data}"
        self.logger.debug(message)
    
    def log_data_operation(self, operation: str, details: dict):
        """Log data cleaning operations."""
        message = f"Data Operation: {operation}"
        self.info(message, details)
    
    def log_file_operation(self, operation: str, file_path: str, details: Optional[dict] = None):
        """Log file operations."""
        message = f"File Operation: {operation} | File: {file_path}"
        if details:
            message += f" | Details: {details}"
        self.info(message)
    
    def log_error_with_traceback(self, operation: str, error: Exception):
        """Log error with full traceback."""
        import traceback
        error_details = {
            "operation": operation,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "traceback": traceback.format_exc()
        }
        self.error(f"Error in {operation}", error_details)

# Create a global logger instance
app_logger = DataCleaningLogger()

def get_logger() -> DataCleaningLogger:
    """Get the application logger instance."""
    return app_logger

def log_data_info(df, operation: str = "Data Processing"):
    """Log basic information about a DataFrame."""
    try:
        info = {
            "operation": operation,
            "shape": df.shape,
            "columns": list(df.columns),
            "dtypes": df.dtypes.value_counts().to_dict(),
            "missing_values": df.isnull().sum().sum(),
            "memory_usage_mb": df.memory_usage(deep=True).sum() / (1024 * 1024)
        }
        app_logger.info(f"DataFrame Info for {operation}", info)
    except Exception as e:
        app_logger.error(f"Failed to log DataFrame info: {str(e)}")

def log_cleaning_step(step_name: str, before_shape: tuple, after_shape: tuple, details: dict = None):
    """Log a data cleaning step with before/after comparison."""
    log_data = {
        "step": step_name,
        "before_shape": before_shape,
        "after_shape": after_shape,
        "rows_removed": before_shape[0] - after_shape[0],
        "columns_changed": before_shape[1] - after_shape[1]
    }
    
    if details:
        log_data.update(details)
    
    app_logger.log_data_operation(step_name, log_data)
