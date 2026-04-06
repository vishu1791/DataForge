import pandas as pd
from typing import Optional, Union
import os

class DataLoader:
    """Handles loading of various data file formats."""
    
    SUPPORTED_FORMATS = ['csv', 'xlsx', 'xls', 'json', 'parquet']
    
    @staticmethod
    def load_file(file_path: str, file_format: Optional[str] = None) -> pd.DataFrame:
        """
        Load data from various file formats.
        
        Args:
            file_path: Path to the data file
            file_format: Format of the file (if not provided, inferred from extension)
            
        Returns:
            pandas DataFrame with loaded data
        """
        if file_format is None:
            file_format = file_path.split('.')[-1].lower()
        
        if file_format not in DataLoader.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported format: {file_format}")
        
        try:
            if file_format == 'csv':
                # Try multiple encodings to handle different file formats
                encodings = ['utf-8', 'latin1', 'cp1252', 'iso-8859-1', 'utf-16']
                for encoding in encodings:
                    try:
                        return pd.read_csv(file_path, encoding=encoding)
                    except UnicodeDecodeError:
                        continue
                    except Exception as e:
                        # If it's not an encoding error, raise it
                        raise
                # If all encodings fail, try with error handling
                return pd.read_csv(file_path, encoding='utf-8', errors='ignore')
            elif file_format in ['xlsx', 'xls']:
                return pd.read_excel(file_path)
            elif file_format == 'json':
                return pd.read_json(file_path)
            elif file_format == 'parquet':
                return pd.read_parquet(file_path)
        except Exception as e:
            raise ValueError(f"Error loading file: {str(e)}")
    
    @staticmethod
    def load_uploaded_file(uploaded_file, file_format: Optional[str] = None) -> pd.DataFrame:
        """
        Load data directly from Streamlit uploaded file object.
        
        Args:
            uploaded_file: Streamlit file uploader object
            file_format: Format of the file (if not provided, inferred from filename)
            
        Returns:
            pandas DataFrame with loaded data
        """
        if file_format is None:
            file_format = uploaded_file.name.split('.')[-1].lower()
        
        if file_format not in DataLoader.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported format: {file_format}")
        
        try:
            if file_format == 'csv':
                # Try multiple encodings for uploaded files
                encodings = ['utf-8', 'latin1', 'cp1252', 'iso-8859-1', 'utf-16']
                for encoding in encodings:
                    try:
                        uploaded_file.seek(0)  # Reset file pointer
                        return pd.read_csv(uploaded_file, encoding=encoding)
                    except UnicodeDecodeError:
                        continue
                    except Exception as e:
                        # If it's not an encoding error, raise it
                        raise
                # If all encodings fail, try with error handling
                uploaded_file.seek(0)
                return pd.read_csv(uploaded_file, encoding='utf-8', errors='ignore')
            elif file_format in ['xlsx', 'xls']:
                uploaded_file.seek(0)
                return pd.read_excel(uploaded_file)
            elif file_format == 'json':
                uploaded_file.seek(0)
                return pd.read_json(uploaded_file)
            elif file_format == 'parquet':
                uploaded_file.seek(0)
                return pd.read_parquet(uploaded_file)
        except Exception as e:
            raise ValueError(f"Error loading uploaded file: {str(e)}")
    
    @staticmethod
    def get_file_info(df: pd.DataFrame) -> dict:
        """Get basic information about the loaded dataset."""
        return {
            'shape': df.shape,
            'columns': list(df.columns),
            'dtypes': df.dtypes.to_dict(),
            'memory_usage': df.memory_usage(deep=True).sum(),
            'null_values': df.isnull().sum().to_dict()
        }
