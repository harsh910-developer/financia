# Finance Tracker

A full-stack application for tracking personal finances, managing transactions, and visualizing spending patterns.

## Features

- User authentication (register/login)
- Transaction management (add, view, delete)
- Financial insights and statistics
- Responsive design for mobile and desktop
- Real-time data updates

## Tech Stack

- **Frontend**: React.js, Material-UI, Chart.js
- **Backend**: Node.js, Express.js
- **Database**: SQLite with Sequelize ORM
- **Authentication**: JWT (JSON Web Tokens)

## Project Structure

```
Finance tracker/
├── backend-node/         # Node.js backend
│   ├── src/
│   │   ├── config/      # Database and app configuration
│   │   ├── middleware/  # Custom middleware
│   │   ├── models/      # Database models
│   │   ├── routes/      # API routes
│   │   └── app.js       # Main application file
│   ├── .env             # Environment variables
│   └── package.json     # Backend dependencies
│
└── finance-tracker-frontend/  # React frontend
    ├── public/           # Static files
    ├── src/
    │   ├── components/  # React components
    │   ├── context/     # React context
    │   ├── utils/       # Utility functions
    │   └── App.js       # Main application file
    └── package.json     # Frontend dependencies
```

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
   ```
   cd backend-node
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Create a .env file with the following variables:
   ```
   PORT=5001
   JWT_SECRET=your_secret_key
   ```

4. Start the development server:
   ```
   npm run dev
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd finance-tracker-frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm start
   ```

4. The application will be available at http://localhost:3001

## API Endpoints

- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login user
- `GET /api/transactions` - Get all transactions for the current user
- `POST /api/transactions` - Create a new transaction
- `GET /api/transactions/stats` - Get transaction statistics

## License

MIT 