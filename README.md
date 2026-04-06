# Data Cleaning Tool

A comprehensive Streamlit-based web application for data cleaning, transformation, and visualization. This tool provides an intuitive interface for performing common data preprocessing tasks with real-time visual feedback.

## Features

### 📁 Data Loading
- Support for multiple file formats: CSV, Excel, JSON, Parquet
- Automatic data type detection
- File size validation
- Data preview and basic statistics

### 🧹 Data Cleaning
- **Missing Values Handling**: Drop, fill with mean/median/mode/custom values
- **Duplicate Removal**: Identify and remove duplicate rows
- **Outlier Detection**: IQR and Z-score methods with customizable thresholds
- **Data Type Conversion**: Automatic and manual data type optimization

### 🔄 Data Transformation
- **Categorical Encoding**: One-hot encoding and label encoding
- **Feature Scaling**: StandardScaler and MinMaxScaler
- **Feature Engineering**: Log transforms, polynomial features, square root transforms
- **Column Operations**: Rename, drop, and create new columns

### 📊 Data Visualization
- **Interactive Plots**: Distribution plots, scatter plots, box plots, violin plots
- **Correlation Matrix**: Heatmap with correlation coefficients
- **Missing Values Analysis**: Visual representation of missing data patterns
- **Data Overview Dashboard**: Comprehensive data quality overview
- **Custom Plots**: Build custom visualizations with selected variables

### 📋 Data Quality Reports
- Automated data quality assessment
- Missing value analysis with recommendations
- Duplicate detection and reporting
- Outlier analysis and suggestions
- Data type optimization recommendations

## Project Structure

```
data-cleaning-tool/
│
├── app.py                  # Main Streamlit app (entry point)
│
├── config/
│   └── settings.py         # App configurations (constants, paths)
│
├── data/
│   ├── raw/                # Original uploaded files
│   └── processed/          # Cleaned datasets
│
├── modules/
│   ├── data_loader.py      # File reading logic
│   ├── data_cleaning.py    # Missing values, duplicates, outliers
│   ├── data_transform.py   # Encoding, scaling
│   └── visualization.py    # Graphs and plots
│
├── utils/
│   ├── helpers.py          # Common utility functions
│   └── logger.py           # Logging (optional but pro-level)
│
├── ui/
│   ├── sidebar.py          # Sidebar controls
│   └── main_panel.py       # Main dashboard UI
│
├── outputs/
│   ├── plots/              # Saved visualizations
│   └── reports/            # Optional reports
│
├── requirements.txt        # Dependencies
├── README.md               # Project documentation
└── .gitignore
```

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd data-cleaning-tool
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Start the application:**
   ```bash
   streamlit run app.py
   ```

2. **Open your web browser** and navigate to `http://localhost:8501`

3. **Upload your data file** using the sidebar file uploader

4. **Apply cleaning operations** using the various options in the sidebar:
   - Handle missing values
   - Remove duplicates
   - Detect and handle outliers
   - Encode categorical variables
   - Scale numeric features
   - Create new features

5. **Visualize your data** using the built-in plotting tools

6. **Export cleaned data** in your preferred format

## Supported File Formats

### Input Formats
- **CSV** (.csv)
- **Excel** (.xlsx, .xls)
- **JSON** (.json)
- **Parquet** (.parquet)

### Output Formats
- **CSV** (.csv)
- **Excel** (.xlsx)
- **JSON** (.json)

## Key Components

### Data Loader (`modules/data_loader.py`)
- Handles file reading from various formats
- Provides data type inference
- Returns basic dataset information

### Data Cleaner (`modules/data_cleaning.py`)
- Missing value imputation strategies
- Duplicate detection and removal
- Outlier detection using IQR and Z-score methods

### Data Transformer (`modules/data_transform.py`)
- Categorical encoding (one-hot, label)
- Feature scaling (standard, min-max)
- Feature engineering operations

### Visualizer (`modules/visualization.py`)
- Interactive Plotly visualizations
- Statistical plots and charts
- Data quality visualizations

## Configuration

The application can be configured through `config/settings.py`:

- **App settings**: Title, layout, sidebar state
- **Data paths**: Configure input/output directories
- **Visualization settings**: Color palettes, figure sizes
- **Cleaning thresholds**: Missing value limits, outlier thresholds
- **Performance settings**: File size limits, chunk sizes

## Logging

The application includes comprehensive logging functionality:
- File and console logging
- Operation tracking
- Error reporting with tracebacks
- Data processing logs

## Performance Considerations

- **Large file handling**: Automatic sampling for files > 100MB
- **Memory optimization**: Efficient data processing with chunking
- **Caching**: Streamlit's built-in caching for improved performance

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Dependencies

See `requirements.txt` for the complete list of dependencies and their versions:

- **streamlit**: Web application framework
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **matplotlib**: Static plotting
- **seaborn**: Statistical data visualization
- **plotly**: Interactive plotting
- **scikit-learn**: Machine learning utilities
- **openpyxl**: Excel file handling
- **pyarrow**: Parquet file support

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Troubleshooting

### Common Issues

1. **File upload fails**: Check file format and size limits
2. **Memory errors**: Try using smaller datasets or enable sampling
3. **Visualization not loading**: Ensure all dependencies are installed
4. **Export errors**: Check write permissions for output directories

### Getting Help

- Check the logs in the `logs/` directory for detailed error information
- Ensure all dependencies are properly installed
- Verify file permissions for data directories

## Future Enhancements

- [ ] Advanced outlier detection methods
- [ ] Automated data quality scoring
- [ ] Machine learning pipeline integration
- [ ] Database connectivity
- [ ] Real-time data streaming support
- [ ] Collaborative features
- [ ] Advanced statistical tests
- [ ] Time series specific tools

---

**Built with ❤️ using Streamlit and Python**
