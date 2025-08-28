// Test script to verify frontend authentication
// Run this in the browser console when on the admin page

console.log('🔍 Testing Frontend Authentication...');

// Check if admin token exists
const adminToken = localStorage.getItem('adminToken');
console.log('Admin Token:', adminToken ? `${adminToken.substring(0, 20)}...` : 'Not found');

// Check axios defaults
console.log('Axios Authorization Header:', axios.defaults.headers.common['Authorization']);

// Test API call
async function testAuth() {
  try {
    console.log('Testing /admin/profile endpoint...');
    const response = await axios.get('/admin/profile');
    console.log('✅ Profile endpoint successful:', response.data);
    
    console.log('Testing /admin/commissions/manual endpoint...');
    const commissionsResponse = await axios.get('/admin/commissions/manual');
    console.log('✅ Commissions endpoint successful:', commissionsResponse.data);
    
  } catch (error) {
    console.error('❌ API call failed:', error.response?.status, error.response?.data);
  }
}

testAuth(); 