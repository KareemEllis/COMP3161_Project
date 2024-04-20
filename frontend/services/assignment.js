import apiClient from './apiClient';

/**
 * Creates a new assignment for a course.
 * 
 * @param {string} courseId The ID of the course for which the assignment is being created.
 * @param {string} assignmentTitle The title of the new assignment.
 * @param {string} dueDate The due date of the assignment in YYYY-MM-DD format.
 * @returns {Promise} The promise resolving to the response of the request.
 */
export const createAssignment = async (courseId, assignmentTitle, dueDate) => {
  try {
    const data = { courseId, assignmentTitle, dueDate };

    // Sending a POST request to the /create_assignment endpoint
    const response = await apiClient.post('/create_assignment', data);
    console.log('Assignment created successfully:', response.data);

    // Returning the response data, including the assignmentId of the newly created assignment
    return response.data;
  } catch (error) {
    console.error('Error creating assignment:', error.response ? error.response.data : error.message);
    throw error;
  }
};



/**
 * Retrieves all assignments for a given course by the course ID.
 * 
 * @param {string} courseId The ID of the course for which to retrieve assignments.
 * @returns {Promise} The promise resolving to the response of the request, including all assignments for the course.
 */
export const getCourseAssignments = async (courseId) => {
    try {
      // Constructing the URL with the courseId
      const url = `/assignment/${courseId}`;
  
      // Sending a GET request to the constructed endpoint
      const response = await apiClient.get(url);
      console.log(`Course assignments retrieval successful for course ${courseId}:`, response.data);
  
      // Returning the assignments data specific to the course
      return response.data;
    } catch (error) {
      console.error(`Error retrieving assignments for course ${courseId}:`, error.response ? error.response.data : error.message);
      throw error;
    }
};



/**
 * Submits an assignment for a student.
 * 
 * @param {string} userId The ID of the student making the submission.
 * @param {string} assignmentId The ID of the assignment being submitted.
 * @returns {Promise} The promise resolving to the response of the request.
 */
export const submitAssignment = async (userId, assignmentId) => {
    try {
      const data = { userId, assignmentId };
  
      // Sending a POST request to the /assignment/submit endpoint
      const response = await apiClient.post('/assignment/submit', data);
      console.log('Assignment submission successful:', response.data);
  
      // Returning the response data, including the submissionId of the newly created assignment submission
      return response.data;
    } catch (error) {
      console.error('Error submitting assignment:', error.response ? error.response.data : error.message);
      throw error;
    }
};



/**
 * Retrieves all submissions for a given assignment by the assignment ID.
 * 
 * @param {string} assignmentId The ID of the assignment for which to retrieve submissions.
 * @returns {Promise} The promise resolving to the response of the request, including all submissions for the assignment.
 */
export const getAssignmentSubmissions = async (assignmentId) => {
    try {
      // Constructing the URL with the assignmentId
      const url = `/assignment_submissions/${assignmentId}`;
  
      // Sending a GET request to the constructed endpoint
      const response = await apiClient.get(url);
      console.log(`Assignment submissions retrieval successful for assignment ${assignmentId}:`, response.data);
  
      // Returning the submissions data specific to the assignment
      return response.data;
    } catch (error) {
      console.error(`Error retrieving submissions for assignment ${assignmentId}:`, error.response ? error.response.data : error.message);
      throw error;
    }
};


/**
 * Assigns a grade to an assignment submission.
 * 
 * @param {string} userId The ID of the course maintainer assigning the grade.
 * @param {string} submissionId The ID of the submission being graded.
 * @param {number|string} grade The grade being assigned to the submission.
 * @returns {Promise} The promise resolving to the response of the request.
 */
export const assignGrade = async (userId, submissionId, grade) => {
    try {
      const data = { userId, submissionId, grade };
  
      // Sending a POST request to the /assign_grade endpoint
      const response = await apiClient.post('/assign_grade', data);
      console.log('Grade assigned successfully:', response.data);
  
      // Returning the response data
      return response.data;
    } catch (error) {
      console.error('Error assigning grade:', error.response ? error.response.data : error.message);
      throw error;
    }
};