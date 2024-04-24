import apiClient from './apiClient';

/**
 * Retrieves all courses that have 50 or more students.
 * 
 * @returns {Promise} The promise resolving to the response of the request, including details of the courses.
 */
export const getCoursesWithManyStudents = async () => {
  try {
    // Sending a GET request to the /courses_with_many_students endpoint
    const response = await apiClient.get('/courses_with_many_students');
    console.log(`Retrieved courses with 50 or more students:`, response.data);

    // Returning the courses data
    return response.data;
  } catch (error) {
    console.error(`Error retrieving courses with 50 or more students:`, error.response ? error.response.data : error.message);
    throw error.response ? error.response.data : error.message;
  }
};


/**
 * Retrieves all students enrolled in 5 or more courses.
 * 
 * @returns {Promise} The promise resolving to the response of the request, including details of the students.
 */
export const getStudentsWithManyCourses = async () => {
    try {
      // Sending a GET request to the /students_with_many_courses endpoint
      const response = await apiClient.get('/students_with_many_courses');
      console.log(`Retrieved students enrolled in 5 or more courses:`, response.data);
  
      // Returning the students data
      return response.data;
    } catch (error) {
      console.error(`Error retrieving students with many courses:`, error.response ? error.response.data : error.message);
      throw error.response ? error.response.data : error.message;
    }
};


/**
 * Retrieves all course maintainers teaching 3 or more courses.
 * 
 * @returns {Promise} The promise resolving to the response of the request, including details of the course maintainers.
 */
export const getMaintainersWithManyCourses = async () => {
    try {
      // Sending a GET request to the /maintainers_with_many_courses endpoint
      const response = await apiClient.get('/maintainers_with_many_courses');
      console.log(`Retrieved course maintainers teaching 3 or more courses:`, response.data);
  
      // Returning the course maintainers' data
      return response.data;
    } catch (error) {
      console.error(`Error retrieving course maintainers with many courses:`, error.response ? error.response.data : error.message);
      throw error.response ? error.response.data : error.message;
    }
};



/**
 * Retrieves the 10 most enrolled courses.
 * 
 * @returns {Promise} The promise resolving to the response of the request, including details of the top 10 courses by enrollment.
 */
export const getTopEnrolledCourses = async () => {
    try {
      // Sending a GET request to the /top_enrolled_courses endpoint
      const response = await apiClient.get('/top_enrolled_courses');
      console.log(`Retrieved the 10 most enrolled courses:`, response.data);
  
      // Returning the top courses data
      return response.data;
    } catch (error) {
      console.error(`Error retrieving the top enrolled courses:`, error.response ? error.response.data : error.message);
      throw error.response ? error.response.data : error.message;
    }
};


/**
 * Retrieves the top 10 students with the highest overall average grades.
 * 
 * @returns {Promise} The promise resolving to the response of the request, including details of the top students.
 */
export const getTopStudentsByAverage = async () => {
    try {
      // Sending a GET request to the /top_students_by_average endpoint
      const response = await apiClient.get('/top_students_by_average');
      console.log(`Retrieved the top 10 students by average grade:`, response.data);
  
      // Returning the top students' data
      return response.data;
    } catch (error) {
      console.error(`Error retrieving the top students by average grade:`, error.response ? error.response.data : error.message);
      throw error.response ? error.response.data : error.message;
    }
};