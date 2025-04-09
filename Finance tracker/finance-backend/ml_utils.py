import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LinearRegression
from typing import List, Dict, Any
import sqlite3
from datetime import datetime
import os

class SpendingPredictor:
    def __init__(self):
        self.model = None
        self.encoder = None
        self.is_trained = False
        self.db_file = 'transactions.db'
        
        # Try to load the model if it exists
        self._load_model()
    
    def _load_model(self):
        """Load the model if it exists, otherwise train a new one"""
        try:
            # Check if we have enough data to train a model
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM transactions WHERE type = "expense"')
            count = cursor.fetchone()[0]
            conn.close()
            
            if count >= 10:  # Minimum number of transactions needed
                self._train_model()
            else:
                print("Not enough transaction data to train the model. Need at least 10 expense transactions.")
        except Exception as e:
            print(f"Error loading model: {e}")
    
    def _train_model(self):
        """Train the model on the database data"""
        try:
            # Connect to database
            conn = sqlite3.connect(self.db_file)
            
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
                return
            
            # Convert date strings to datetime
            df['date'] = pd.to_datetime(df['date'])
            
            # Prepare features
            X, encoder = self._prepare_features(df)
            y = df['amount']
            
            # Split data into train and test sets
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Train the model
            model = LinearRegression()
            model.fit(X_train, y_train)
            
            # Store the model and encoder
            self.model = model
            self.encoder = encoder
            self.is_trained = True
            
            print("Model trained successfully")
            
        except Exception as e:
            print(f"Error training model: {e}")
        finally:
            if 'conn' in locals():
                conn.close()
    
    def _prepare_features(self, df):
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
    
    def predict_category_spending(self, category, month=None):
        """
        Predict spending for a specific category in a specific month
        
        Args:
            category: The category to predict for
            month: The month to predict for (1-12). If None, uses current month.
            
        Returns:
            float: Predicted spending amount
        """
        if not self.is_trained:
            self._train_model()
            if not self.is_trained:
                return 0.0
        
        try:
            # Use current month if not specified
            if month is None:
                month = datetime.now().month
            
            # Create feature vector for prediction
            pred_features = pd.DataFrame({
                'month_num': [month]
            })
            
            # Add one-hot encoded category
            category_encoded = self.encoder.transform([[category]])
            category_df = pd.DataFrame(
                category_encoded,
                columns=self.encoder.get_feature_names_out(['category'])
            )
            
            pred_features = pd.concat([pred_features, category_df], axis=1)
            
            # Make prediction
            prediction = self.model.predict(pred_features)[0]
            
            # Ensure prediction is non-negative
            return max(0, prediction)
            
        except Exception as e:
            print(f"Error making prediction: {e}")
            return 0.0
    
    def get_current_month_spending(self, category):
        """
        Get the current month's spending for a specific category
        
        Args:
            category: The category to get spending for
            
        Returns:
            float: Current month's spending
        """
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Get current month and year
            now = datetime.now()
            current_month = now.month
            current_year = now.year
            
            # Query for current month's spending
            query = """
            SELECT SUM(amount)
            FROM transactions
            WHERE type = 'expense'
            AND category = ?
            AND strftime('%m', date) = ?
            AND strftime('%Y', date) = ?
            """
            
            cursor.execute(query, (category, f"{current_month:02d}", str(current_year)))
            result = cursor.fetchone()[0]
            
            conn.close()
            
            return result if result is not None else 0.0
            
        except Exception as e:
            print(f"Error getting current spending: {e}")
            return 0.0
    
    def get_historical_monthly_totals(self, category, num_months=3):
        """
        Get historical monthly totals for a category
        
        Args:
            category: The category to get history for
            num_months: Number of past months to include
            
        Returns:
            list: List of monthly totals
        """
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Get current month and year
            now = datetime.now()
            
            # Query for historical monthly totals
            query = """
            SELECT strftime('%Y-%m', date) as month, SUM(amount) as total
            FROM transactions
            WHERE type = 'expense'
            AND category = ?
            GROUP BY month
            ORDER BY month DESC
            LIMIT ?
            """
            
            cursor.execute(query, (category, num_months))
            results = cursor.fetchall()
            
            conn.close()
            
            # Extract just the totals
            totals = [row[1] for row in results]
            
            # Pad with zeros if we don't have enough months
            while len(totals) < num_months:
                totals.append(0.0)
                
            return totals
            
        except Exception as e:
            print(f"Error getting historical totals: {e}")
            return [0.0] * num_months 