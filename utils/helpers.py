"""
Helper utility functions.
"""

import pandas as pd
import numpy as np
import os
import re
from typing import List, Dict, Any, Optional
import logging

def setup_logging():
    """Setup logging configuration."""
    from config.settings import LOGGING_CONFIG
    
    os.makedirs(os.path.dirname(LOGGING_CONFIG["file_path"]), exist_ok=True)
    
    logging.basicConfig(
        level=getattr(logging, LOGGING_CONFIG["level"]),
        format=LOGGING_CONFIG["format"],
        handlers=[
            logging.FileHandler(LOGGING_CONFIG["file_path"]),
            logging.StreamHandler()
        ]
    )

def validate_file_format(filename: str, supported_formats: List[str]) -> bool:
    """
    Validate if file format is supported.
    
    Args:
        filename: Name of the file
        supported_formats: List of supported file extensions
        
    Returns:
        True if format is supported, False otherwise
    """
    file_extension = filename.split('.')[-1].lower()
    return file_extension in supported_formats

def get_file_size_mb(file_path: str) -> float:
    """
    Get file size in MB.
    
    Args:
        file_path: Path to the file
        
    Returns:
        File size in MB
    """
    size_bytes = os.path.getsize(file_path)
    return size_bytes / (1024 * 1024)

def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean column names by removing special characters and spaces.
    
    Args:
        df: Input DataFrame
        
    Returns:
        DataFrame with cleaned column names
    """
    df_cleaned = df.copy()
    
    # Clean column names
    cleaned_columns = []
    for col in df_cleaned.columns:
        # Convert to string and lowercase
        col_str = str(col).lower()
        
        # Replace spaces and special characters with underscores
        col_str = re.sub(r'[^\w\s]', '', col_str)  # Remove special characters
        col_str = re.sub(r'\s+', '_', col_str)     # Replace spaces with underscores
        
        # Remove multiple underscores
        col_str = re.sub(r'_+', '_', col_str)
        
        # Remove leading/trailing underscores
        col_str = col_str.strip('_')
        
        cleaned_columns.append(col_str)
    
    df_cleaned.columns = cleaned_columns
    
    return df_cleaned

def detect_column_types(df: pd.DataFrame) -> Dict[str, str]:
    """
    Detect and classify column types.
    
    Args:
        df: Input DataFrame
        
    Returns:
        Dictionary mapping column names to their detected types
    """
    column_types = {}
    
    for col in df.columns:
        if df[col].dtype in ['int64', 'float64']:
            # Check if it's actually categorical
            unique_ratio = df[col].nunique() / len(df)
            if unique_ratio < 0.05 and df[col].nunique() < 20:
                column_types[col] = 'categorical_numeric'
            else:
                column_types[col] = 'numeric'
        elif df[col].dtype == 'object':
            # Check if it's datetime
            try:
                pd.to_datetime(df[col].dropna().head())
                column_types[col] = 'datetime'
            except:
                # Check if it's categorical
                unique_ratio = df[col].nunique() / len(df)
                if unique_ratio < 0.05:
                    column_types[col] = 'categorical'
                else:
                    column_types[col] = 'text'
        elif df[col].dtype == 'bool':
            column_types[col] = 'boolean'
        elif 'datetime' in str(df[col].dtype):
            column_types[col] = 'datetime'
        else:
            column_types[col] = 'unknown'
    
    return column_types

def create_data_summary(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Create a comprehensive data summary.
    
    Args:
        df: Input DataFrame
        
    Returns:
        Dictionary containing data summary statistics
    """
    summary = {
        'basic_info': {
            'shape': df.shape,
            'memory_usage_mb': df.memory_usage(deep=True).sum() / (1024 * 1024),
            'column_count': len(df.columns),
            'row_count': len(df)
        },
        'data_types': df.dtypes.value_counts().to_dict(),
        'missing_values': {
            'total_missing': df.isnull().sum().sum(),
            'missing_percentage': (df.isnull().sum().sum() / (df.shape[0] * df.shape[1])) * 100,
            'columns_with_missing': df.columns[df.isnull().any()].tolist()
        },
        'duplicates': {
            'duplicate_rows': df.duplicated().sum(),
            'duplicate_percentage': (df.duplicated().sum() / len(df)) * 100
        },
        'numeric_summary': {},
        'categorical_summary': {}
    }
    
    # Numeric columns summary
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if not numeric_cols.empty:
        summary['numeric_summary'] = {
            'count': len(numeric_cols),
            'columns': numeric_cols.tolist(),
            'statistics': df[numeric_cols].describe().to_dict()
        }
    
    # Categorical columns summary
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns
    if not categorical_cols.empty:
        cat_summary = {}
        for col in categorical_cols:
            cat_summary[col] = {
                'unique_count': df[col].nunique(),
                'most_frequent': df[col].mode().iloc[0] if not df[col].mode().empty else None,
                'frequency': df[col].value_counts().iloc[0] if not df[col].empty else 0
            }
        summary['categorical_summary'] = {
            'count': len(categorical_cols),
            'columns': categorical_cols.tolist(),
            'details': cat_summary
        }
    
    return summary

def safe_division(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    Safely perform division to avoid division by zero.
    
    Args:
        numerator: Numerator value
        denominator: Denominator value
        default: Default value if denominator is zero
        
    Returns:
        Result of division or default value
    """
    try:
        if denominator == 0:
            return default
        return numerator / denominator
    except:
        return default

def format_bytes(bytes_value: int) -> str:
    """
    Format bytes into human-readable string.
    
    Args:
        bytes_value: Value in bytes
        
    Returns:
        Formatted string (e.g., "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} PB"

def truncate_string(text: str, max_length: int = 50) -> str:
    """
    Truncate string to specified length.
    
    Args:
        text: Input string
        max_length: Maximum length
        
    Returns:
        Truncated string with ellipsis if needed
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."

def validate_dataframe(df: pd.DataFrame) -> List[str]:
    """
    Validate DataFrame and return list of issues.
    
    Args:
        df: Input DataFrame
        
    Returns:
        List of validation issues
    """
    issues = []
    
    if df.empty:
        issues.append("DataFrame is empty")
        return issues
    
    # Check for completely empty columns
    empty_cols = df.columns[df.isnull().all()].tolist()
    if empty_cols:
        issues.append(f"Completely empty columns: {empty_cols}")
    
    # Check for columns with all same values
    constant_cols = []
    for col in df.columns:
        if df[col].nunique() == 1:
            constant_cols.append(col)
    if constant_cols:
        issues.append(f"Columns with constant values: {constant_cols}")
    
    # Check for potential ID columns (high cardinality)
    high_cardinality_cols = []
    for col in df.columns:
        if df[col].nunique() == len(df) and df[col].dtype == 'object':
            high_cardinality_cols.append(col)
    if high_cardinality_cols:
        issues.append(f"Potential ID columns (high cardinality): {high_cardinality_cols}")
    
    return issues
