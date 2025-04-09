# Finance Tracker with ML Predictions

A full-stack application for tracking finances with machine learning-powered spending predictions.

## Features

- Track income and expenses by category
- View transaction history
- Get spending predictions based on historical data
- Visualize spending patterns
- Receive warnings when approaching predicted spending limits

## Project Structure

- **Backend**: Flask API with SQLite database and scikit-learn for predictions
- **Frontend**: React application with modern UI

## Setup Instructions

### Backend Setup

1. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Initialize the database with sample data:
   ```
   python init_db.py
   ```

3. Start the Flask server:
   ```
   python app.py
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd finance-tracker
   ```

2. Install Node.js dependencies:
   ```
   npm install
   ```

3. Start the React development server:
   ```
   npm start
   ```

4. Open your browser and navigate to `http://localhost:3000`

## API Endpoints

- `GET /api/transactions`: Get all transactions
- `POST /api/transactions`: Add a new transaction
- `GET /api/predict/<category>`: Get spending prediction for a specific category

## Machine Learning Model

The application uses a Linear Regression model from scikit-learn to predict spending patterns. The model:

- Trains on historical transaction data
- Considers temporal features (month, day, day of week)
- Accounts for category and transaction type
- Automatically retrains when new transactions are added
- Falls back to simple averaging when there's not enough data

## Technologies Used

- **Backend**: Flask, SQLite, scikit-learn, pandas, numpy
- **Frontend**: React, Axios, CSS
- **Machine Learning**: scikit-learn, joblib 