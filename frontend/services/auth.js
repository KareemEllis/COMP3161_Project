import apiClient from './apiClient';

/**
 * Register a new user.
 * 
 * @param {string} userId The user's ID.
 * @param {string} username The user's username.
 * @param {string} name The user's full name.
 * @param {string} password The user's password.
 * @param {string} accType The user's account type.
 * @returns {Promise} The promise resolving to the response of the request.
 */
export const registerUser = async (userId, username, name, password, accType) => {
  try {
    // Constructing the data object with the parameters
    const data = { userId, username, name, password, accType };

    // Sending a POST request to the /register endpoint
    const response = await apiClient.post('/register', data);
    console.log('Registration successful:', response.data);

    // Returning the response data
    return response.data;
  } catch (error) {
    console.error('Error registering user:', error.response ? error.response.data : error.message);
    throw error;
  }
};


/**
 * Login a user and store user data in localStorage if successful.
 * 
 * @param {string} userId The user's ID.
 * @param {string} password The user's password.
 * @returns {Promise} The promise resolving to the response of the request.
 */
export const loginUser = async (userId, password) => {
    try {
      const data = { userId, password };
  
      const response = await apiClient.post('/login', data);
      console.log('Login successful:', response.data);
  
      // Assuming the user data is in the response's 'user' property
      if (response.data && response.data.user) {
        // Storing user data in localStorage
        localStorage.setItem('userData', JSON.stringify(response.data.user));
      }
  
      return response.data;
    } catch (error) {
      console.error('Error logging in:', error.response ? error.response.data : error.message);
      throw error;
    }
};


/**
 * Logout the current user and clear user data from localStorage.
 * 
 * @returns {Promise} The promise resolving to the response of the request.
 */
export const logoutUser = async () => {
    try {
      // Sending a GET request to the /logout endpoint
      const response = await apiClient.get('/logout');
      console.log('Logout successful:', response.data);
  
      // Clearing userData from localStorage on successful logout
      localStorage.removeItem('userData');
  
      return response.data;
    } catch (error) {
      console.error('Error logging out:', error.response ? error.response.data : error.message);
      throw error;
    }
};