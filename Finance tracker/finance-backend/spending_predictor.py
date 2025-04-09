import sqlite3
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def prepare_features(df):
    """Prepare features for the model."""
    # Create month number feature
    df['month_num'] = df['date'].dt.month
    
    # Create one-hot encoding for categories
    encoder = OneHotEncoder(sparse_output=False)
    category_encoded = encoder.fit_transform(df[['category']])
    category_df = pd.DataFrame(
        category_encoded,
        columns=encoder.get_feature_names_out(['category'])
    )
    
    # Combine features
    features = pd.concat([
        df[['month_num']],
        category_df
    ], axis=1)
    
    return features, encoder

def train_model():
    """Train a linear regression model on spending data."""
    try:
        # Connect to database
        conn = sqlite3.connect('transactions.db')
        
        # Get all transactions
        query = """
        SELECT 
            type,
            amount,
            category,
            date
        FROM transactions
        WHERE type = 'expense'
        ORDER BY date
        """
        
        df = pd.read_sql_query(query, conn)
        
        if len(df) < 2:
            print("Not enough data to train the model. Need at least 2 transactions.")
            return None, None
        
        # Convert date strings to datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # Prepare features
        X, encoder = prepare_features(df)
        y = df['amount']
        
        # Split data into train and test sets
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train the model
        model = LinearRegression()
        model.fit(X_train, y_train)
        
        # Calculate and print model performance
        train_score = model.score(X_train, y_train)
        test_score = model.score(X_test, y_test)
        
        print("\n=== Model Performance ===")
        print(f"Training R² Score: {train_score:.2f}")
        print(f"Testing R² Score: {test_score:.2f}")
        
        # Make predictions for current month
        current_month = datetime.now().month
        current_year = datetime.now().year
        
        # Get unique categories
        categories = df['category'].unique()
        
        print("\n=== Predictions for Current Month ===")
        print(f"Month: {current_month} ({datetime.now().strftime('%B')} {current_year})")
        
        for category in categories:
            # Create feature vector for prediction
            pred_features = pd.DataFrame({
                'month_num': [current_month]
            })
            
            # Add one-hot encoded category
            category_encoded = encoder.transform([[category]])
            category_df = pd.DataFrame(
                category_encoded,
                columns=encoder.get_feature_names_out(['category'])
            )
            
            pred_features = pd.concat([pred_features, category_df], axis=1)
            
            # Make prediction
            prediction = model.predict(pred_features)[0]
            
            print(f"\nCategory: {category}")
            print(f"Predicted spending: ${prediction:.2f}")
        
        return model, encoder
        
    except sqlite3.OperationalError as e:
        print(f"Database error: {e}")
        if "no such table" in str(e):
            print("The transactions table does not exist. Please run db_init.py first.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()
    
    return None, None

if __name__ == '__main__':
    model, encoder = train_model() 