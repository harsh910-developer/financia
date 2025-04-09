import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta
import joblib
import os

class SpendingPredictor:
    def __init__(self):
        self.model = LinearRegression()
        self.scaler = StandardScaler()
        self.is_trained = False
        self.model_path = 'models/spending_model.joblib'
        self.scaler_path = 'models/scaler.joblib'
        
        # Create models directory if it doesn't exist
        os.makedirs('models', exist_ok=True)
        
        # Try to load existing model
        self.load_model()
    
    def prepare_data(self, transactions):
        """
        Convert transaction data to a format suitable for machine learning
        """
        # Convert transactions to DataFrame
        df = pd.DataFrame(transactions)
        
        # Convert date strings to datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # Extract features
        df['month'] = df['date'].dt.month
        df['day'] = df['date'].dt.day
        df['day_of_week'] = df['date'].dt.dayofweek
        
        # Create dummy variables for categories
        category_dummies = pd.get_dummies(df['category'], prefix='category')
        df = pd.concat([df, category_dummies], axis=1)
        
        # Create dummy variables for transaction type
        type_dummies = pd.get_dummies(df['type'], prefix='type')
        df = pd.concat([df, type_dummies], axis=1)
        
        # Select features for training
        feature_columns = ['month', 'day', 'day_of_week'] + \
                         [col for col in category_dummies.columns] + \
                         [col for col in type_dummies.columns]
        
        return df[feature_columns], df['amount']
    
    def train(self, transactions):
        """
        Train the model on historical transaction data
        """
        if len(transactions) < 10:
            raise ValueError("Need more transaction history for meaningful predictions")
        
        # Prepare data
        X, y = self.prepare_data(transactions)
        
        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        self.model.fit(X_train_scaled, y_train)
        
        # Calculate and print model performance
        train_score = self.model.score(X_train_scaled, y_train)
        test_score = self.model.score(X_test_scaled, y_test)
        print(f"Model R² score - Training: {train_score:.3f}, Testing: {test_score:.3f}")
        
        self.is_trained = True
        self.save_model()
    
    def predict(self, transaction_date, category, transaction_type):
        """
        Predict spending amount for a given date, category, and transaction type
        """
        if not self.is_trained:
            raise ValueError("Model needs to be trained first")
        
        # Create a DataFrame with the prediction input
        date = pd.to_datetime(transaction_date)
        input_data = pd.DataFrame({
            'month': [date.month],
            'day': [date.day],
            'day_of_week': [date.dayofweek]
        })
        
        # Add category dummy variables
        for cat in self.model.feature_names_in_:
            if cat.startswith('category_'):
                input_data[cat] = 1 if cat == f'category_{category}' else 0
        
        # Add transaction type dummy variables
        for type_ in self.model.feature_names_in_:
            if type_.startswith('type_'):
                input_data[type_] = 1 if type_ == f'type_{transaction_type}' else 0
        
        # Scale features
        input_scaled = self.scaler.transform(input_data)
        
        # Make prediction
        prediction = self.model.predict(input_scaled)[0]
        
        return max(0, round(prediction, 2))  # Ensure non-negative prediction
    
    def save_model(self):
        """
        Save the trained model and scaler to disk
        """
        if self.is_trained:
            joblib.dump(self.model, self.model_path)
            joblib.dump(self.scaler, self.scaler_path)
            print("Model and scaler saved successfully")
    
    def load_model(self):
        """
        Load the trained model and scaler from disk
        """
        try:
            self.model = joblib.load(self.model_path)
            self.scaler = joblib.load(self.scaler_path)
            self.is_trained = True
            print("Model and scaler loaded successfully")
        except:
            print("No saved model found. A new model will be trained.")
            self.is_trained = False 