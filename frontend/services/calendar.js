import apiClient from './apiClient';

/**
 * Retrieves all calendar events for a given course by the course ID.
 * 
 * @param {string} courseId The ID of the course for which to retrieve calendar events.
 * @returns {Promise} The promise resolving to the response of the request, including calendar events for the course.
 */
export const getCalendarEventsForCourse = async (courseId) => {
  try {
    // Constructing the URL with the courseId
    const url = `/calendar/course/${courseId}`;

    // Sending a GET request to the constructed endpoint
    const response = await apiClient.get(url);
    console.log(`Calendar events retrieval successful for course ${courseId}:`, response.data);

    // Returning the calendar events data specific to the course
    return response.data;
  } catch (error) {
    console.error(`Error retrieving calendar events for course ${courseId}:`, error.response ? error.response.data : error.message);
    throw error.response ? error.response.data : error.message;
  }
};


/**
 * Creates a calendar event.
 * 
 * @param {string} courseId The ID of the course associated with the event.
 * @param {string} startDate The start date of the event.
 * @param {string} endDate The end date of the event.
 * @param {string} eventTitle The title of the event.
 * @param {string} description The description of the event.
 * @returns {Promise} The promise resolving to the response of the request.
 */
export const createCalendarEvent = async (courseId, startDate, endDate, eventTitle, description) => {
    try {
      const data = { courseId, startDate, endDate, eventTitle, description };
  
      // Sending a POST request to the /calendar/create endpoint
      const response = await apiClient.post('/calendar/create', data);
      console.log('Calendar event created successfully:', response.data);
  
      // Returning the response data
      return response.data;
    } catch (error) {
      console.error('Error creating calendar event:', error.response ? error.response.data : error.message);
      throw error.response ? error.response.data : error.message;
    }
};


/**
 * Retrieves all calendar events for a user on a specific date.
 * 
 * @param {string} userId The ID of the user.
 * @param {string} date The specific date for which to retrieve events, in YYYY-MM-DD format.
 * @returns {Promise} The promise resolving to the response of the request, including calendar events for the date.
 */
export const getUserDailyCalendarEvents = async (userId, date) => {
    try {
      // Constructing the URL with the userId and appending the date as a query parameter
      const url = `/calendar/user/daily/${userId}?date=${date}`;
  
      // Sending a GET request to the constructed endpoint
      const response = await apiClient.get(url);
      console.log(`Calendar events retrieval successful for user ${userId} on ${date}:`, response.data);
  
      // Returning the calendar events data specific to the user and date
      return response.data;
    } catch (error) {
      console.error(`Error retrieving calendar events for user ${userId} on ${date}:`, error.response ? error.response.data : error.message);
      throw error.response ? error.response.data : error.message;
    }
};



/**
 * Retrieves all calendar events for a user across all their courses.
 * 
 * @param {string} userId The ID of the user.
 * @returns {Promise} The promise resolving to the response of the request, including all calendar events for the user.
 */
export const getUserCalendarEvents = async (userId) => {
    try {
      // Constructing the URL with the userId
      const url = `/calendar/user/${userId}`;
  
      // Sending a GET request to the constructed endpoint
      const response = await apiClient.get(url);
      console.log(`Calendar events retrieval successful for user ${userId}:`, response.data);
  
      // Returning the calendar events data specific to the user
      return response.data;
    } catch (error) {
      console.error(`Error retrieving calendar events for user ${userId}:`, error.response ? error.response.data : error.message);
      throw error.response ? error.response.data : error.message;
    }
};