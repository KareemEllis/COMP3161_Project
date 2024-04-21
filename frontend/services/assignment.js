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
    throw error.response ? error.response.data : error.message;
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
      const url = `/assignment/course/${courseId}`;
  
      // Sending a GET request to the constructed endpoint
      const response = await apiClient.get(url);
      console.log(`Course assignments retrieval successful for course ${courseId}:`, response.data);
  
      // Returning the assignments data specific to the course
      return response.data;
    } catch (error) {
      console.error(`Error retrieving assignments for course ${courseId}:`, error.response ? error.response.data : error.message);
      throw error.response ? error.response.data : error.message;
    }
};


/**
 * Fetches assignment information by its assignment ID.
 *
 * @param {number|string} assignmentId - The unique identifier for the assignment.
 * @returns {Promise<Object>} A promise that resolves to the assignment's data.
 * @throws {Error} Throws an error if the request to the API fails or if the assignment is not found.
 */
export const getAssignmentById = async (assignmentId) => {
  try {
      // Assuming `apiClient` is already set up to include baseURL and any necessary configurations
      const response = await apiClient.get(`/assignment/${assignmentId}`);
      console.log('Assignment retrieval successful:', response.data);

      // Returning the response data which contains the assignment information
      return response.data;
  } catch (error) {
      console.error('Error retrieving assignment:', error.response ? error.response.data : error.message);
      // Rethrow the error with a custom message or use the API's error message
      throw error.response ? error.response.data : error.message;
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
      throw error.response ? error.response.data : error.message;
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
      throw error.response ? error.response.data : error.message;
    }
};


/**
 * Fetches details of an assignment submission by its submission ID.
 *
 * @param {number|string} submissionId - The unique identifier for the assignment submission.
 * @returns {Promise<Object>} A promise that resolves to the detailed data of the assignment submission, including user and assignment details.
 * @throws {Error} Throws an error if the request to the API fails or if the assignment submission is not found.
 */
export const getAssignmentSubmissionById = async (submissionId) => {
  try {
      // Assuming `apiClient` is an instance of Axios or a similar library configured with your API's base URL and headers
      const response = await apiClient.get(`/assignment_submissions/submission/${submissionId}`);
      console.log('Assignment submission retrieval successful:', response.data);

      // Returning the response data which contains the assignment submission information
      return response.data;
  } catch (error) {
      console.error('Error retrieving assignment submission:', error.response ? error.response.data : error.message);
      // Rethrow the error with a custom message or use the API's error message
      throw error.response ? error.response.data : error.message;
  }
};



/**
 * Fetches all assignments for a student by the student's ID.
 *
 * @param {number} studentId - The unique identifier of the student.
 * @returns {Promise<Object>} A promise that resolves to the data containing all courses and their respective assignments for the specified student.
 * @throws {Error} Throws an error if the request to the API fails, if the student ID does not belong to a student, or if there's any other issue fetching the assignments.
 */
export const getStudentAssignments = async (studentId) => {
  try {
      // Assuming `apiClient` is an instance of Axios or a similar library configured with your API's base URL and headers
      const response = await apiClient.get(`/student_assignments/${studentId}`);
      console.log('Student assignments retrieval successful:', response.data);

      // Returning the response data which contains the student assignments
      return response.data;
  } catch (error) {
      console.error('Error retrieving student assignments:', error.response ? error.response.data : error.message);
      // Rethrow the error with a custom message or use the API's error message
      throw error.response ? error.response.data : error.message;
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
      throw error.response ? error.response.data : error.message;
    }
};