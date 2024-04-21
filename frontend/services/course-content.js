import apiClient from './apiClient';

/**
 * Creates a new section in a course.
 * 
 * @param {string} userId The ID of the user creating the section.
 * @param {string} courseId The ID of the course for which the section is being created.
 * @param {string} sectionTitle The title of the new section.
 * @returns {Promise} The promise resolving to the response of the request.
 */
export const createSection = async (userId, courseId, sectionTitle) => {
  try {
    const data = { userId, courseId, sectionTitle };

    // Sending a POST request to the /create_section endpoint
    const response = await apiClient.post('/create_section', data);
    console.log('Section created successfully:', response.data);

    // Returning the response data, including the sectionId of the newly created section
    return response.data;
  } catch (error) {
    console.error('Error creating section:', error.response ? error.response.data : error.message);
    throw error.response ? error.response.data : error.message;
  }
};



/**
 * Retrieves all sections for a given course by the course ID.
 * 
 * @param {string} courseId The ID of the course for which to retrieve sections.
 * @returns {Promise} The promise resolving to the response of the request, including all sections for the course.
 */
export const getCourseSections = async (courseId) => {
    try {
      // Constructing the URL with the courseId
      const url = `/section/${courseId}`;
  
      // Sending a GET request to the constructed endpoint
      const response = await apiClient.get(url);
      console.log(`Course sections retrieval successful for course ${courseId}:`, response.data);
  
      // Returning the sections data specific to the course
      return response.data;
    } catch (error) {
      console.error(`Error retrieving sections for course ${courseId}:`, error.response ? error.response.data : error.message);
      throw error.response ? error.response.data : error.message;
    }
};



/**
 * Creates a new section item.
 * 
 * @param {string} sectionId The ID of the section for which the item is being created.
 * @param {string} sectionContent The content of the new section item.
 * @returns {Promise} The promise resolving to the response of the request.
 */
export const createSectionItem = async (sectionId, sectionContent) => {
    try {
      const data = { sectionId, sectionContent };
  
      // Sending a POST request to the /create_section_item endpoint
      const response = await apiClient.post('/create_section_item', data);
      console.log('Section item created successfully:', response.data);
  
      // Returning the response data, including the itemId of the newly created section item
      return response.data;
    } catch (error) {
      console.error('Error creating section item:', error.response ? error.response.data : error.message);
      throw error.response ? error.response.data : error.message;
    }
};



/**
 * Retrieves all items for a given section by the section ID.
 * 
 * @param {string} sectionId The ID of the section for which to retrieve items.
 * @returns {Promise} The promise resolving to the response of the request, including all items for the section.
 */
export const getSectionItems = async (sectionId) => {
    try {
      // Constructing the URL with the sectionId
      const url = `/section_items/${sectionId}`;
  
      // Sending a GET request to the constructed endpoint
      const response = await apiClient.get(url);
      console.log(`Section items retrieval successful for section ${sectionId}:`, response.data);
  
      // Returning the section items data specific to the section
      return response.data;
    } catch (error) {
      console.error(`Error retrieving items for section ${sectionId}:`, error.response ? error.response.data : error.message);
      throw error.response ? error.response.data : error.message;
    }
};



/**
 * Creates a new topic in a section.
 * 
 * @param {string} sectionId The ID of the section for which the topic is being created.
 * @param {string} topicTitle The title of the new topic.
 * @returns {Promise} The promise resolving to the response of the request.
 */
export const createTopic = async (sectionId, topicTitle) => {
    try {
      const data = { sectionId, topicTitle };
  
      // Sending a POST request to the /create_topic endpoint
      const response = await apiClient.post('/create_topic', data);
      console.log('Topic created successfully:', response.data);
  
      // Returning the response data, including the topicId of the newly created topic
      return response.data;
    } catch (error) {
      console.error('Error creating topic:', error.response ? error.response.data : error.message);
      throw error.response ? error.response.data : error.message;
    }
};



/**
 * Retrieves all topics for a given section by the section ID.
 * 
 * @param {string} sectionId The ID of the section for which to retrieve topics.
 * @returns {Promise} The promise resolving to the response of the request, including all topics for the section.
 */
export const getSectionTopics = async (sectionId) => {
    try {
      // Constructing the URL with the sectionId
      const url = `/topic/${sectionId}`;
  
      // Sending a GET request to the constructed endpoint
      const response = await apiClient.get(url);
      console.log(`Section topics retrieval successful for section ${sectionId}:`, response.data);
  
      // Returning the topics data specific to the section
      return response.data;
    } catch (error) {
      console.error(`Error retrieving topics for section ${sectionId}:`, error.response ? error.response.data : error.message);
      throw error.response ? error.response.data : error.message;
    }
};



/**
 * Retrieves all content for a given course, including sections, section items, and topics, by the course ID.
 * 
 * @param {string} courseId The ID of the course for which to retrieve content.
 * @returns {Promise} The promise resolving to the response of the request, including all content for the course.
 */
export const getCourseContent = async (courseId) => {
    try {
      // Constructing the URL with the courseId
      const url = `/course/content/${courseId}`;
  
      // Sending a GET request to the constructed endpoint
      const response = await apiClient.get(url);
      console.log(`Course content retrieval successful for course ${courseId}:`, response.data);
  
      // Returning the course content data specific to the course
      return response.data;
    } catch (error) {
      console.error(`Error retrieving content for course ${courseId}:`, error.response ? error.response.data : error.message);
      throw error.response ? error.response.data : error.message;
    }
};