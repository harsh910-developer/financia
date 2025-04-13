const helmet = require('helmet');
const cors = require('cors');
const xss = require('xss-clean');
const hpp = require('hpp');

// Configure CORS options
const corsOptions = {
    origin: process.env.FRONTEND_URL || ['http://localhost:3000', 'http://localhost:3001'],
    methods: ['GET', 'POST', 'PUT', 'DELETE'],
    allowedHeaders: ['Content-Type', 'Authorization'],
    credentials: true,
    maxAge: 86400 // 24 hours
};

// Configure security middleware
const securityMiddleware = [
    // Set security HTTP headers
    helmet(),
    
    // Enable CORS with custom options
    cors(corsOptions),
    
    // Data sanitization against XSS attacks
    xss(),
    
    // Prevent parameter pollution
    hpp(),
    
    // Custom security headers
    (req, res, next) => {
        res.setHeader('X-Content-Type-Options', 'nosniff');
        res.setHeader('X-Frame-Options', 'DENY');
        res.setHeader('X-XSS-Protection', '1; mode=block');
        next();
    }
];

module.exports = securityMiddleware; 