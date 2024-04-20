import apiClient from './apiClient';

/**
 * Creates a new course.
 * 
 * @param {string} userId The user's ID attempting to create the course.
 * @param {string} courseId The unique ID for the new course.
 * @param {string} courseName The name of the new course.
 * @param {string} period The period or term for the course.
 * @returns {Promise} The promise resolving to the response of the request.
 */
export const createCourse = async (userId, courseId, courseName, period) => {
  try {
    // Constructing the data object with the parameters
    const data = { userId, courseId, courseName, period };

    // Sending a POST request to the /course endpoint
    const response = await apiClient.post('/course', data);
    console.log('Course creation successful:', response.data);

    // Returning the response data
    return response.data;
  } catch (error) {
    console.error('Error creating course:', error.response ? error.response.data : error.message);
    throw error;
  }
};


/**
 * Retrieves all courses.
 * 
 * @returns {Promise} The promise resolving to the array of courses.
 */
export const getAllCourses = async () => {
    try {
      // Sending a GET request to the /course endpoint
      const response = await apiClient.get('/course');
      console.log('Courses retrieval successful:', response.data);
  
      // Returning the courses data
      return response.data;
    } catch (error) {
      console.error('Error retrieving courses:', error.response ? error.response.data : error.message);
      throw error;
    }
};


/**
 * Retrieves all courses for a given student by their student ID.
 * 
 * @param {string} studentId The student's ID.
 * @returns {Promise} The promise resolving to the array of courses for the student.
 */
export const getStudentCourses = async (studentId) => {
    try {
      // Dynamically constructing the URL with the studentId
      const url = `/course/student/${studentId}`;
  
      // Sending a GET request to the constructed endpoint
      const response = await apiClient.get(url);
      console.log(`Courses retrieval successful for student ${studentId}:`, response.data);
  
      // Returning the courses data specific to the student
      return response.data;
    } catch (error) {
      console.error(`Error retrieving courses for student ${studentId}:`, error.response ? error.response.data : error.message);
      throw error;
    }
};



/**
 * Retrieves all courses for a given course maintainer by their ID.
 * 
 * @param {string} maintainerId The course maintainer's ID.
 * @returns {Promise} The promise resolving to the array of courses for the maintainer.
 */
export const getMaintainerCourses = async (maintainerId) => {
    try {
      // Constructing the URL with the maintainerId
      const url = `/course/maintainer/${maintainerId}`;
  
      // Sending a GET request to the constructed endpoint
      const response = await apiClient.get(url);
      console.log(`Courses retrieval successful for maintainer ${maintainerId}:`, response.data);
  
      // Returning the courses data specific to the maintainer
      return response.data;
    } catch (error) {
      console.error(`Error retrieving courses for maintainer ${maintainerId}:`, error.response ? error.response.data : error.message);
      throw error;
    }
};



/**
 * Registers a user for a course.
 * 
 * @param {string} userId The ID of the user registering for the course.
 * @param {string} courseId The ID of the course to register for.
 * @returns {Promise} The promise resolving to the response of the request.
 */
export const registerForCourse = async (userId, courseId) => {
    try {
      // Constructing the data object with the userId and courseId
      const data = { userId, courseId };
  
      // Sending a POST request to the /course/register endpoint
      const response = await apiClient.post('/course/register', data);
      console.log('Registration for course successful:', response.data);
  
      // Returning the response data
      return response.data;
    } catch (error) {
      console.error('Error registering for course:', error.response ? error.response.data : error.message);
      throw error;
    }
};



/**
 * Retrieves all members for a given course by the course ID.
 * 
 * @param {string} courseId The ID of the course to retrieve members for.
 * @returns {Promise} The promise resolving to the response of the request, including course members.
 */
export const getCourseMembers = async (courseId) => {
    try {
      // Dynamically constructing the URL with the courseId
      const url = `/members/${courseId}`;
  
      // Sending a GET request to the constructed endpoint
      const response = await apiClient.get(url);
      console.log(`Members retrieval successful for course ${courseId}:`, response.data);
  
      // Returning the members data specific to the course
      return response.data;
    } catch (error) {
      console.error(`Error retrieving members for course ${courseId}:`, error.response ? error.response.data : error.message);
      throw error;
    }
};