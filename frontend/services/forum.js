import apiClient from './apiClient';

/**
 * Creates a new discussion forum for a course.
 * 
 * @param {string} courseId The ID of the course for which the forum is being created.
 * @param {string} forumTitle The title of the new forum.
 * @returns {Promise} The promise resolving to the response of the request.
 */
export const createDiscussionForum = async (courseId, forumTitle) => {
  try {
    const data = { courseId, forumTitle };

    // Sending a POST request to the /create_forum endpoint
    const response = await apiClient.post('/create_forum', data);
    console.log('Discussion forum created successfully:', response.data);

    // Returning the response data, including the forumId of the newly created forum
    return response.data;
  } catch (error) {
    console.error('Error creating discussion forum:', error.response ? error.response.data : error.message);
    throw error.response ? error.response.data : error.message;
  }
};



/**
 * Retrieves all discussion forums for a given course by the course ID.
 * 
 * @param {string} courseId The ID of the course for which to retrieve discussion forums.
 * @returns {Promise} The promise resolving to the response of the request, including all discussion forums for the course.
 */
export const getDiscussionForumsForCourse = async (courseId) => {
    try {
      // Constructing the URL with the courseId
      const url = `/forum/${courseId}`;
  
      // Sending a GET request to the constructed endpoint
      const response = await apiClient.get(url);
      console.log(`Discussion forums retrieval successful for course ${courseId}:`, response.data);
  
      // Returning the discussion forums data specific to the course
      return response.data;
    } catch (error) {
      console.error(`Error retrieving discussion forums for course ${courseId}:`, error.response ? error.response.data : error.message);
      throw error.response ? error.response.data : error.message;
    }
};


/**
 * Fetches forum details by its forum ID.
 *
 * @param {number|string} forumId - The unique identifier of the forum.
 * @returns {Promise<Object>} A promise that resolves to the forum's details, including its ID, title, and associated course ID.
 * @throws {Error} Throws an error if unable to fetch the forum details from the API, including when the forum is not found.
 */
export const getForumById = async (forumId) => {
  try {
      const response = await apiClient.get(`/get-forum/${forumId}`);
      console.log('Forum retrieval successful:', response.data);

      // Returning the response data which contains the forum details
      return response.data;
  } catch (error) {
      console.error('Error retrieving forum:', error.response ? error.response.data : error.message);
      throw error.response ? error.response.data : error.message;
  }
};



/**
 * Creates a new discussion thread or reply in a forum.
 * 
 * @param {string} userId The ID of the user creating the thread or reply.
 * @param {string} forumId The ID of the forum where the thread or reply is being created.
 * @param {string} threadTitle The title of the thread (required for top-level threads).
 * @param {string} threadContent The content of the thread or reply.
 * @param {string|null} parentThreadId The ID of the parent thread (if this is a reply).
 * @returns {Promise} The promise resolving to the response of the request.
 */
export const createDiscussionThread = async (userId, forumId, threadTitle, threadContent, parentThreadId = null) => {
    try {
      const data = { userId, forumId, threadTitle, threadContent, parentThreadId };
  
      // Sending a POST request to the /create_thread endpoint
      const response = await apiClient.post('/create_thread', data);
      console.log('Discussion thread created successfully:', response.data);
  
      // Returning the response data, including the threadId of the newly created thread or reply
      return response.data;
    } catch (error) {
      console.error('Error creating discussion thread:', error.response ? error.response.data : error.message);
      throw error.response ? error.response.data : error.message;
    }
};



/**
 * Retrieves all top-level threads for a given discussion forum by the forum ID.
 * 
 * @param {string} forumId The ID of the forum for which to retrieve top-level threads.
 * @returns {Promise} The promise resolving to the response of the request, including all top-level threads for the forum.
 */
export const getForumThreads = async (forumId) => {
    try {
      // Constructing the URL with the forumId
      const url = `/forum_threads/${forumId}`;
  
      // Sending a GET request to the constructed endpoint
      const response = await apiClient.get(url);
      //console.log(`Forum threads retrieval successful for forum ${forumId}:`, response.data);
  
      // Returning the top-level threads data specific to the forum
      return response.data;
    } catch (error) {
      console.error(`Error retrieving forum threads for forum ${forumId}:`, error.response ? error.response.data : error.message);
      throw error.response ? error.response.data : error.message;
    }
};


/**
 * Retrieves all replies for a given discussion thread by the thread ID.
 * 
 * @param {string} threadId The ID of the thread for which to retrieve replies.
 * @returns {Promise} The promise resolving to the response of the request, including all replies for the thread.
 */
export const getThreadReplies = async (threadId) => {
    try {
      // Constructing the URL with the threadId
      const url = `/thread_replies/${threadId}`;
  
      // Sending a GET request to the constructed endpoint
      const response = await apiClient.get(url);
      //console.log(`Thread replies retrieval successful for thread ${threadId}:`, response.data);
  
      // Returning the replies data specific to the thread
      return response.data;
    } catch (error) {
      console.error(`Error retrieving replies for thread ${threadId}:`, error.response ? error.response.data : error.message);
      throw error.response ? error.response.data : error.message;
    }
};