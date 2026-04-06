import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple

class DataCleaner:
    """Handles data cleaning operations."""
    
    @staticmethod
    def handle_missing_values(
        df: pd.DataFrame, 
        strategy: str = 'drop', 
        fill_value: Optional[str] = None,
        columns: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Handle missing values in the dataset.
        
        Args:
            df: Input DataFrame
            strategy: 'drop', 'fill_mean', 'fill_median', 'fill_mode', 'fill_value'
            fill_value: Custom value to fill when strategy is 'fill_value'
            columns: Specific columns to treat (if None, treat all)
            
        Returns:
            DataFrame with missing values handled
        """
        df_cleaned = df.copy()
        
        # If specific columns are provided, only work on those
        if columns:
            target_cols = [col for col in columns if col in df_cleaned.columns]
        else:
            target_cols = df_cleaned.columns.tolist()
        
        if strategy == 'drop':
            # Drop rows with missing values in target columns
            df_cleaned = df_cleaned.dropna(subset=target_cols)
        elif strategy == 'fill_mean':
            # Fill with mean for numeric columns only
            numeric_cols = df_cleaned[target_cols].select_dtypes(include=[np.number]).columns
            if not numeric_cols.empty:
                df_cleaned[numeric_cols] = df_cleaned[numeric_cols].fillna(df_cleaned[numeric_cols].mean())
        elif strategy == 'fill_median':
            # Fill with median for numeric columns only
            numeric_cols = df_cleaned[target_cols].select_dtypes(include=[np.number]).columns
            if not numeric_cols.empty:
                df_cleaned[numeric_cols] = df_cleaned[numeric_cols].fillna(df_cleaned[numeric_cols].median())
        elif strategy == 'fill_mode':
            # Fill with mode for each column (works for both numeric and categorical)
            for col in target_cols:
                if col in df_cleaned.columns:
                    mode_vals = df_cleaned[col].mode()
                    if not mode_vals.empty:
                        df_cleaned[col] = df_cleaned[col].fillna(mode_vals[0])
        elif strategy == 'fill_value' and fill_value is not None:
            # Fill with specified value for target columns
            df_cleaned[target_cols] = df_cleaned[target_cols].fillna(fill_value)
        
        return df_cleaned
    
    @staticmethod
    def remove_duplicates(df: pd.DataFrame, subset: Optional[List[str]] = None) -> pd.DataFrame:
        """Remove duplicate rows from the dataset."""
        df_cleaned = df.copy()
        return df_cleaned.drop_duplicates(subset=subset, keep='first')
    
    @staticmethod
    def detect_outliers(
        df: pd.DataFrame, 
        method: str = 'iqr', 
        threshold: float = 1.5
    ) -> Dict[str, List[int]]:
        """
        Detect outliers in numeric columns.
        
        Args:
            df: Input DataFrame
            method: 'iqr' or 'zscore'
            threshold: Threshold for outlier detection
            
        Returns:
            Dictionary mapping column names to lists of outlier indices
        """
        outliers = {}
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            try:
                # Skip if column has no valid data
                if df[col].dropna().empty:
                    continue
                    
                if method == 'iqr':
                    Q1 = df[col].quantile(0.25)
                    Q3 = df[col].quantile(0.75)
                    IQR = Q3 - Q1
                    
                    # Skip if IQR is zero (all values are the same)
                    if IQR == 0:
                        continue
                        
                    lower_bound = Q1 - threshold * IQR
                    upper_bound = Q3 + threshold * IQR
                    outlier_mask = (df[col] < lower_bound) | (df[col] > upper_bound)
                    outlier_indices = df[outlier_mask].index.tolist()
                    
                elif method == 'zscore':
                    # Skip if standard deviation is zero
                    if df[col].std() == 0:
                        continue
                        
                    z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
                    outlier_indices = df[z_scores > threshold].index.tolist()
                
                # Only add column if outliers were found
                if outlier_indices:
                    outliers[col] = outlier_indices
                    
            except Exception as e:
                # Skip column if error occurs
                print(f"Warning: Could not detect outliers in column {col}: {e}")
                continue
        
        return outliers
    
    @staticmethod
    def remove_outliers(
        df: pd.DataFrame, 
        outliers: Dict[str, List[int]], 
        method: str = 'remove'
    ) -> pd.DataFrame:
        """
        Remove or cap outliers.
        
        Args:
            df: Input DataFrame
            outliers: Dictionary of outlier indices from detect_outliers
            method: 'remove' or 'cap'
            
        Returns:
            DataFrame with outliers handled
        """
        df_cleaned = df.copy()
        
        if method == 'remove':
            # Collect all unique outlier indices
            all_outlier_indices = set()
            for indices in outliers.values():
                all_outlier_indices.update(indices)
            
            # Remove outliers if any were found
            if all_outlier_indices:
                df_cleaned = df_cleaned.drop(list(all_outlier_indices))
                
        elif method == 'cap':
            # Cap outliers to IQR bounds for each column
            for col, indices in outliers.items():
                if col in df_cleaned.select_dtypes(include=[np.number]).columns:
                    try:
                        Q1 = df_cleaned[col].quantile(0.25)
                        Q3 = df_cleaned[col].quantile(0.75)
                        IQR = Q3 - Q1
                        
                        # Skip if IQR is zero
                        if IQR == 0:
                            continue
                            
                        lower_bound = Q1 - 1.5 * IQR
                        upper_bound = Q3 + 1.5 * IQR
                        
                        # Cap values to bounds
                        df_cleaned[col] = df_cleaned[col].clip(lower=lower_bound, upper=upper_bound)
                        
                    except Exception as e:
                        print(f"Warning: Could not cap outliers in column {col}: {e}")
                        continue
        
        return df_cleaned
