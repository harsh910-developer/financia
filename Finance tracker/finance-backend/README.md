# Finance Tracker Backend

A Flask-based backend application for the Finance Tracker project that provides APIs for managing transactions and generating spending predictions.

## Features

- RESTful API endpoints for CRUD operations on transactions
- Machine learning-based spending predictions
- SQLite database for data persistence
- CORS support for frontend integration

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows:
```bash
venv\Scripts\activate
```
- Unix/MacOS:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
python db_init.py
```

## Running the Application

1. Start the Flask development server:
```bash
python app.py
```

The server will start at `http://localhost:5000`

## API Endpoints

- `GET /api/transactions` - Get all transactions
- `POST /api/transactions` - Create a new transaction
- `GET /api/transactions/<id>` - Get a specific transaction
- `PUT /api/transactions/<id>` - Update a transaction
- `DELETE /api/transactions/<id>` - Delete a transaction
- `GET /api/predict/<category>` - Get spending predictions for a category

## Development

- The application uses SQLite for data storage
- Machine learning models are trained using scikit-learn
- CORS is enabled for frontend integration
- Environment variables can be configured using a `.env` file

## License

MIT 