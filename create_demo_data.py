"""
Create sample messy datasets for demo purposes.
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def create_messy_customer_data():
    """Create a realistic messy customer dataset."""
    np.random.seed(42)
    random.seed(42)
    
    # Base customer data
    n_customers = 1000
    
    data = {
        'customer_id': range(1, n_customers + 1),
        'first_name': [f'Customer_{i}' for i in range(n_customers)],
        'last_name': [f'Surname_{i}' for i in range(n_customers)],
        'email': [f'customer{i}@email.com' for i in range(n_customers)],
        'age': np.random.normal(35, 12, n_customers),
        'income': np.random.lognormal(10.5, 0.5, n_customers),
        'signup_date': [datetime(2020, 1, 1) + timedelta(days=random.randint(0, 1460)) for _ in range(n_customers)],
        'city': np.random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 
                                'Philadelphia', 'San Antonio', 'San Diego'], n_customers),
        'state': np.random.choice(['NY', 'CA', 'IL', 'TX', 'AZ', 'PA', 'TX', 'CA'], n_customers),
        'country': np.random.choice(['USA', 'USA', 'USA', 'USA', 'Canada', 'USA', 'USA', 'USA'], n_customers),
        'subscription_type': np.random.choice(['Basic', 'Premium', 'Enterprise', 'Basic', 'Premium'], n_customers),
        'monthly_spend': np.random.exponential(50, n_customers),
        'customer_satisfaction': np.random.uniform(1, 5, n_customers),
        'last_purchase_date': [datetime(2023, 1, 1) + timedelta(days=random.randint(0, 365)) for _ in range(n_customers)],
        'total_purchases': np.random.poisson(5, n_customers),
        'is_active': np.random.choice([True, False, True, True], n_customers),
        'credit_score': np.random.normal(650, 100, n_customers)
    }
    
    df = pd.DataFrame(data)
    
    # Introduce messiness
    
    # 1. Missing values (15% overall)
    missing_cols = ['age', 'income', 'email', 'city', 'customer_satisfaction', 'credit_score']
    for col in missing_cols:
        missing_mask = np.random.random(len(df)) < 0.15
        df.loc[missing_mask, col] = np.nan
    
    # 2. Duplicates (5% of data)
    duplicate_indices = np.random.choice(len(df), int(len(df) * 0.05), replace=False)
    duplicates = df.iloc[duplicate_indices].copy()
    df = pd.concat([df, duplicates], ignore_index=True)
    
    # 3. Outliers in numeric columns
    # Age outliers (very young or very old)
    age_outliers = np.random.choice(len(df), 10, replace=False)
    df.loc[age_outliers, 'age'] = np.random.choice([5, 120], 10)
    
    # Income outliers (extremely high)
    income_outliers = np.random.choice(len(df), 5, replace=False)
    df.loc[income_outliers, 'income'] = np.random.uniform(500000, 1000000, 5)
    
    # Credit score outliers (impossible values)
    credit_outliers = np.random.choice(len(df), 8, replace=False)
    df.loc[credit_outliers, 'credit_score'] = np.random.choice([-50, 900, 1500], 8)
    
    # 4. Inconsistent categorical values
    # City inconsistencies
    city_mapping = {
        'New York': ['NYC', 'New York City', 'new york'],
        'Los Angeles': ['LA', 'L.A.', 'los angeles'],
        'Chicago': ['CHI', 'chicago'],
        'Houston': ['HOU', 'houston']
    }
    
    for correct_city, variations in city_mapping.items():
        mask = df['city'] == correct_city
        indices_to_change = np.random.choice(df[mask].index, min(20, len(df[mask])), replace=False)
        for idx in indices_to_change:
            df.loc[idx, 'city'] = random.choice(variations)
    
    # 5. Data type issues
    # Some numeric values as strings
    string_mask = np.random.random(len(df)) < 0.05
    df.loc[string_mask, 'monthly_spend'] = ['$' + str(int(val)) if pd.notna(val) else val 
                                           for val in df.loc[string_mask, 'monthly_spend']]
    
    # 6. Inconsistent email formats
    email_mask = np.random.random(len(df)) < 0.1
    df.loc[email_mask, 'email'] = [email.upper() if pd.notna(email) else email 
                                   for email in df.loc[email_mask, 'email']]
    
    # 7. Invalid dates
    invalid_date_mask = np.random.random(len(df)) < 0.02
    df.loc[invalid_date_mask, 'signup_date'] = 'Invalid Date'
    
    return df

def create_messy_sales_data():
    """Create a messy sales dataset."""
    np.random.seed(123)
    random.seed(123)
    
    n_sales = 2000
    
    data = {
        'sale_id': range(1, n_sales + 1),
        'product_id': np.random.choice(['P001', 'P002', 'P003', 'P004', 'P005'], n_sales),
        'product_name': np.random.choice(['Laptop', 'Phone', 'Tablet', 'Monitor', 'Keyboard'], n_sales),
        'category': np.random.choice(['Electronics', 'Accessories', 'Electronics', 'Electronics', 'Accessories'], n_sales),
        'price': np.random.uniform(50, 2000, n_sales),
        'quantity': np.random.poisson(2, n_sales),
        'discount': np.random.uniform(0, 0.3, n_sales),
        'sale_date': [datetime(2023, 1, 1) + timedelta(days=random.randint(0, 365)) for _ in range(n_sales)],
        'customer_id': np.random.choice(range(1, 501), n_sales),
        'sales_rep': np.random.choice(['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'], n_sales),
        'region': np.random.choice(['North', 'South', 'East', 'West'], n_sales),
        'shipping_method': np.random.choice(['Standard', 'Express', 'Overnight', 'Standard'], n_sales),
        'customer_rating': np.random.uniform(1, 5, n_sales)
    }
    
    df = pd.DataFrame(data)
    
    # Introduce messiness
    
    # Missing values
    missing_cols = ['discount', 'customer_rating', 'sales_rep']
    for col in missing_cols:
        missing_mask = np.random.random(len(df)) < 0.1
        df.loc[missing_mask, col] = np.nan
    
    # Duplicates
    duplicate_indices = np.random.choice(len(df), int(len(df) * 0.03), replace=False)
    duplicates = df.iloc[duplicate_indices].copy()
    df = pd.concat([df, duplicates], ignore_index=True)
    
    # Outliers
    price_outliers = np.random.choice(len(df), 15, replace=False)
    df.loc[price_outliers, 'price'] = np.random.uniform(5000, 10000, 15)
    
    # Negative quantities (returns)
    negative_mask = np.random.random(len(df)) < 0.05
    df.loc[negative_mask, 'quantity'] = -df.loc[negative_mask, 'quantity']
    
    # Inconsistent categories
    category_mapping = {
        'Electronics': ['electronics', 'ELECTRONICS'],
        'Accessories': ['accessories', 'ACCESSORIES']
    }
    
    for correct_cat, variations in category_mapping.items():
        mask = df['category'] == correct_cat
        indices_to_change = np.random.choice(df[mask].index, min(15, len(df[mask])), replace=False)
        for idx in indices_to_change:
            df.loc[idx, 'category'] = random.choice(variations)
    
    return df

def main():
    """Create and save demo datasets."""
    print("🎯 Creating demo datasets for presentation...")
    
    # Create customer data
    print("📊 Creating customer dataset...")
    customer_df = create_messy_customer_data()
    customer_df.to_csv('demo_messy_customers.csv', index=False)
    print(f"✅ Customer dataset saved: {customer_df.shape}")
    
    # Create sales data
    print("💰 Creating sales dataset...")
    sales_df = create_messy_sales_data()
    sales_df.to_csv('demo_messy_sales.csv', index=False)
    print(f"✅ Sales dataset saved: {sales_df.shape}")
    
    # Show data quality summary
    print("\n📋 Data Quality Summary:")
    print("\nCustomer Dataset:")
    print(f"  - Total rows: {len(customer_df):,}")
    print(f"  - Missing values: {customer_df.isnull().sum().sum():,}")
    print(f"  - Duplicates: {customer_df.duplicated().sum():,}")
    print(f"  - Numeric columns: {len(customer_df.select_dtypes(include='number').columns)}")
    print(f"  - Categorical columns: {len(customer_df.select_dtypes(include='object').columns)}")
    
    print("\nSales Dataset:")
    print(f"  - Total rows: {len(sales_df):,}")
    print(f"  - Missing values: {sales_df.isnull().sum().sum():,}")
    print(f"  - Duplicates: {sales_df.duplicated().sum():,}")
    print(f"  - Numeric columns: {len(sales_df.select_dtypes(include='number').columns)}")
    print(f"  - Categorical columns: {len(sales_df.select_dtypes(include='object').columns)}")
    
    print("\n🎉 Demo datasets ready for presentation!")
    print("\n📝 Demo Tips:")
    print("1. Start with the customer dataset (more relatable)")
    print("2. Show the data quality issues first")
    print("3. Demonstrate cleaning step by step")
    print("4. Highlight the before/after improvements")
    print("5. Use the visualizations to tell a story")

if __name__ == "__main__":
    main()
