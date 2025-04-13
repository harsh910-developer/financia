const axios = require('axios');

async function testBackend() {
  try {
    // Test registration
    console.log('Testing registration...');
    const registerResponse = await axios.post('http://localhost:5000/api/auth/register', {
      name: 'Test User',
      email: 'test@example.com',
      password: 'password123'
    });
    console.log('Registration successful:', registerResponse.data);
    
    // Test login
    console.log('\nTesting login...');
    const loginResponse = await axios.post('http://localhost:5000/api/auth/login', {
      email: 'test@example.com',
      password: 'password123'
    });
    console.log('Login successful:', loginResponse.data);
    
    // Test transactions with token
    console.log('\nTesting transactions...');
    const token = loginResponse.data.token;
    const transactionsResponse = await axios.get('http://localhost:5000/api/transactions', {
      headers: { Authorization: `Bearer ${token}` }
    });
    console.log('Transactions retrieved:', transactionsResponse.data);
    
    console.log('\nAll tests passed!');
  } catch (error) {
    console.error('Test failed:', error.response?.data || error.message);
  }
}

testBackend(); 