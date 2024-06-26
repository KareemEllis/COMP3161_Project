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
    throw error.response ? error.response.data : error.message;
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
      throw error.response ? error.response.data : error.message;
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
      throw error.response ? error.response.data : error.message;
    }
};


/**
 * Fetches the current user's session data from the API.
 *
 * @returns {Promise<Object>} A promise that resolves to the current user's session data.
 * @throws {Error} Throws an error if unable to fetch the user session data.
 */
export const getUserData = async () => {
  try {
    const userDataString = localStorage.getItem('userData');
    if (userDataString) {
      const userData = JSON.parse(userDataString);
      return userData;
    }
    else {
      throw new Error('User data not found');
    }
    
  } catch (error) {
      console.error('Error retrieving user session:', error.response ? error.response.data : error.message);
      throw error.response ? error.response.data : error.message;
  }
};


/**
 * Fetches all users from the API, including their account types.
 *
 * @returns {Promise<Array>} A promise that resolves to an array of user objects, each containing the user's ID, username, name, and account type.
 * @throws {Error} Throws an error if unable to fetch the users from the API.
 */
export const getAllUsers = async () => {
  try {
      const response = await apiClient.get('/users');
      console.log('User retrieval successful:', response.data);

      // Returning the response data which contains an array of users
      return response.data;
  } catch (error) {
      console.error('Error retrieving users:', error.response ? error.response.data : error.message);
      throw error.response ? error.response.data : error.message;
  }
};

/**
 * Fetches details of a specific user by their user ID.
 *
 * @param {number|string} userId - The unique identifier of the user.
 * @returns {Promise<Object>} A promise that resolves to the user's data, including their ID, username, name, and account type.
 * @throws {Error} Throws an error if unable to fetch the user data from the API, including when the user is not found.
 */
export const getUserById = async (userId) => {
  try {
      const response = await apiClient.get(`/user/${userId}`);
      console.log('User retrieval successful:', response.data);

      // Returning the response data which contains the user's information
      return response.data;
  } catch (error) {
      console.error('Error retrieving user data:', error.response ? error.response.data : error.message);
      throw error.response ? error.response.data : error.message;
  }
};