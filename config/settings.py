"""
Application configuration settings.
"""

APP_CONFIG = {
    "app_title": "Data Cleaning & Visualization Tool",
    "app_icon": "🧹",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Data paths
DATA_PATHS = {
    "raw_data": "data/raw",
    "processed_data": "data/processed",
    "plots": "outputs/plots",
    "reports": "outputs/reports"
}

# Supported file formats
SUPPORTED_FORMATS = {
    "input": ["csv", "xlsx", "xls", "json", "parquet"],
    "output": ["csv", "xlsx", "json"]
}

# Visualization settings
VIZ_CONFIG = {
    "default_color_palette": "husl",
    "figure_size": (10, 6),
    "dpi": 300,
    "plot_style": "seaborn-v0_8"
}

# Data cleaning thresholds
CLEANING_THRESHOLDS = {
    "missing_value_threshold": 0.2,  # Drop columns with >20% missing values
    "outlier_iqr_threshold": 1.5,
    "outlier_zscore_threshold": 3.0,
    "max_unique_values_categorical": 50  # Max unique values for categorical encoding
}

# Logging configuration
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file_path": "logs/app.log"
}

# Performance settings
PERFORMANCE_CONFIG = {
    "max_file_size_mb": 100,  # Maximum file size in MB
    "sample_size_large_files": 10000,  # Sample size for large datasets
    "chunk_size": 10000  # Chunk size for processing large files
}
