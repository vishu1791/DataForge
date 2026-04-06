import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from typing import List, Dict, Optional, Tuple

class DataTransformer:
    """Handles data transformation operations."""
    
    @staticmethod
    def encode_categorical(
        df: pd.DataFrame, 
        columns: List[str], 
        method: str = 'onehot'
    ) -> pd.DataFrame:
        """
        Encode categorical variables.
        
        Args:
            df: Input DataFrame
            columns: List of categorical column names
            method: 'onehot' or 'label'
            
        Returns:
            DataFrame with encoded categorical variables
        """
        df_transformed = df.copy()
        
        if method == 'label':
            for col in columns:
                if col in df_transformed.columns:
                    label_encoder = LabelEncoder()
                    df_transformed[col] = label_encoder.fit_transform(df_transformed[col].astype(str))
        
        elif method == 'onehot':
            for col in columns:
                if col in df_transformed.columns:
                    dummies = pd.get_dummies(df_transformed[col], prefix=col, drop_first=False)
                    df_transformed = pd.concat([df_transformed.drop(col, axis=1), dummies], axis=1)
        
        return df_transformed
    
    @staticmethod
    def scale_features(
        df: pd.DataFrame, 
        columns: List[str], 
        method: str = 'standard'
    ) -> Tuple[pd.DataFrame, object]:
        """
        Scale numeric features.
        
        Args:
            df: Input DataFrame
            columns: List of numeric column names to scale
            method: 'standard' or 'minmax'
            
        Returns:
            Tuple of (scaled DataFrame, fitted scaler object)
        """
        df_scaled = df.copy()
        
        if not columns:
            return df_scaled, None
            
        if method == 'standard':
            scaler = StandardScaler()
        elif method == 'minmax':
            scaler = MinMaxScaler()
        else:
            raise ValueError("Method must be 'standard' or 'minmax'")
        
        # Only scale columns that exist and are numeric
        valid_columns = [col for col in columns if col in df_scaled.columns]
        numeric_columns = df_scaled[valid_columns].select_dtypes(include=[np.number]).columns.tolist()
        
        if numeric_columns:
            df_scaled[numeric_columns] = scaler.fit_transform(df_scaled[numeric_columns])
        
        return df_scaled, scaler
    
    @staticmethod
    def create_features(
        df: pd.DataFrame, 
        operations: Dict[str, List[str]]
    ) -> pd.DataFrame:
        """
        Create new features based on existing ones.
        
        Args:
            df: Input DataFrame
            operations: Dictionary with operation types and column lists
                      e.g., {'log': ['col1'], 'sqrt': ['col2'], 'poly': ['col3']}
            
        Returns:
            DataFrame with new features
        """
        df_enhanced = df.copy()
        
        for operation, columns in operations.items():
            for col in columns:
                if col in df_enhanced.columns and col in df_enhanced.select_dtypes(include=[np.number]).columns:
                    if operation == 'log':
                        df_enhanced[f'{col}_log'] = np.log1p(df_enhanced[col])
                    elif operation == 'sqrt':
                        df_enhanced[f'{col}_sqrt'] = np.sqrt(np.abs(df_enhanced[col]))
                    elif operation == 'square':
                        df_enhanced[f'{col}_square'] = df_enhanced[col] ** 2
                    elif operation == 'poly':
                        df_enhanced[f'{col}_poly2'] = df_enhanced[col] ** 2
                        df_enhanced[f'{col}_poly3'] = df_enhanced[col] ** 3
        
        return df_enhanced
    
    @staticmethod
    def convert_data_types(
        df: pd.DataFrame, 
        type_conversions: Dict[str, str]
    ) -> pd.DataFrame:
        """
        Convert data types of specified columns.
        
        Args:
            df: Input DataFrame
            type_conversions: Dictionary mapping column names to target data types
                             e.g., {'col1': 'datetime64', 'col2': 'category'}
            
        Returns:
            DataFrame with converted data types
        """
        df_converted = df.copy()
        
        for col, dtype in type_conversions.items():
            if col in df_converted.columns:
                try:
                    if dtype == 'datetime64':
                        df_converted[col] = pd.to_datetime(df_converted[col])
                    elif dtype == 'category':
                        df_converted[col] = df_converted[col].astype('category')
                    else:
                        df_converted[col] = df_converted[col].astype(dtype)
                except Exception as e:
                    print(f"Could not convert {col} to {dtype}: {str(e)}")
        
        return df_converted
