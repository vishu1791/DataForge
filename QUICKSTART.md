# Quick Start Guide

## 🚀 Get Started in 3 Easy Steps

### Step 1: Setup the Environment
```bash
# Run the setup script
python setup.py
```

This will:
- Install all required dependencies
- Create necessary directories
- Test all imports

### Step 2: Test the Application
```bash
# Run the test script to verify everything works
python test_app.py
```

This will:
- Test all modules
- Create sample data for testing
- Verify functionality

### Step 3: Launch the Web App
```bash
# Start the Streamlit application
streamlit run app.py
```

Then open your browser and go to: **http://localhost:8501**

## 📊 What You Can Do

### 1. Upload Data
- Supported formats: CSV, Excel, JSON, Parquet
- Maximum file size: 100MB

### 2. Clean Data
- Handle missing values (drop, fill with mean/median/mode)
- Remove duplicates
- Detect and handle outliers
- Fix data types

### 3. Transform Data
- Encode categorical variables (one-hot, label encoding)
- Scale numeric features (standard, min-max scaling)
- Create new features (log, polynomial transforms)

### 4. Visualize Data
- Distribution plots (histogram, box, violin)
- Correlation matrix
- Missing values heatmap
- Custom scatter plots
- Data overview dashboard

### 5. Export Results
- Download cleaned data in CSV, Excel, or JSON format
- Save plots and reports

## 🔧 Troubleshooting

### Common Issues

1. **"ModuleNotFoundError"**
   ```bash
   pip install -r requirements.txt
   ```

2. **"Streamlit not found"**
   ```bash
   pip install streamlit
   ```

3. **"Seaborn style error"**
   - The app handles this automatically
   - Will fall back to default matplotlib style

4. **Memory issues with large files**
   - Use files under 100MB
   - The app will automatically sample large datasets

### Need Help?
- Check the console output for error messages
- Look at the logs in the `logs/` directory
- Review the full documentation in `README.md`

## 📁 Sample Data

The test script creates sample data with:
- 1000 rows
- Mixed data types (numeric, categorical)
- Missing values
- Duplicates
- Outliers

Perfect for testing all features!

## 🎯 Pro Tips

1. **Start with the sample data** to understand the workflow
2. **Use the Data Quality Report** to identify issues quickly
3. **Experiment with different cleaning strategies** on the same data
4. **Save your plots** before applying transformations to compare before/after
5. **Check the correlation matrix** after encoding categorical variables

## 📞 Support

If you encounter any issues:
1. Check the error messages in the terminal
2. Review the logs in `logs/app.log`
3. Make sure all dependencies are installed correctly
4. Try with a smaller dataset first

Happy data cleaning! 🧹✨
