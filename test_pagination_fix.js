// Test script to verify pagination fix
console.log('🧪 Testing Pagination Fix');

// Simulate the filters state
let filters = {
  search: '',
  status: '',
  email_verified: '',
  date_from: '',
  date_to: '',
  sort_by: 'created_at',
  sort_order: 'desc',
  page: 1
};

// Test the handleFilterChange function
function handleFilterChange(key, value) {
  console.log(`🔄 Changing ${key} from ${filters[key]} to ${value}`);
  
  filters = {
    ...filters,
    [key]: value,
    // Only reset page to 1 for non-page changes
    page: key === 'page' ? value : 1
  };
  
  console.log('✅ New filters:', filters);
}

// Test the handlePageChange function
function handlePageChange(newPage) {
  console.log(`🔄 Changing page from ${filters.page} to ${newPage}`);
  
  filters = {
    ...filters,
    page: newPage
  };
  
  console.log('✅ New filters:', filters);
}

// Test cases
console.log('\n🧪 Test 1: Change search (should reset page to 1)');
handleFilterChange('search', 'test@example.com');

console.log('\n🧪 Test 2: Change page (should set page to 2)');
handlePageChange(2);

console.log('\n🧪 Test 3: Change status (should reset page to 1)');
handleFilterChange('status', 'active');

console.log('\n🧪 Test 4: Change page again (should set page to 3)');
handlePageChange(3);

console.log('\n🎉 Pagination fix test completed!');
console.log('Expected behavior:');
console.log('- Non-page changes reset page to 1');
console.log('- Page changes set the exact page number');
console.log('- All other filters are preserved'); 