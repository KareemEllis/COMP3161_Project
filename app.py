from dotenv import load_dotenv
import os

from flask import Flask, request, jsonify, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import mysql.connector
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = 'secret'

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

def get_db_connection():
    # Database connection details
    db_host = os.getenv('HOST')
    db_username = os.getenv('USERNAME')
    db_password = os.getenv('PASSWORD')
    db = 'ourvle'

    return mysql.connector.connect(
        host=db_host, 
        user=db_username, 
        password=db_password, 
        database=db
    )

# User class
class User(UserMixin):
    def __init__(self, id, username, name, accType):
        self.id = id
        self.username = username
        self.name = name
        self.accType = accType


# User Loader
@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM User WHERE UserId = %s', (user_id,))
    user_record = cursor.fetchone()
    if user_record:
        cursor.execute("SELECT * FROM account WHERE UserId = %s", (user_id,))
        account_record = cursor.fetchone()
        conn.close()
        return User(id=user_record['UserId'], username=user_record['Username'], name=user_record['Name'], accType=account_record['AccType'])
    conn.close()
    return None

#####################################################################################################
#####################################################################################################
#####################################################################################################

# Register a new user
@app.route('/register', methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        
        userId = data.get('userId')
        username = data.get('username')
        name = data.get('name')
        password = data.get('password')
        accType = data.get('accType')

        # Check if all required fields are provided
        if not userId or not username or not name or not password or not accType:
            return jsonify({"error":"Invalid request. Please provide all required fields (UserId, Username, Name, Password, AccType)"}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if user already exists
        cursor.execute("SELECT * FROM user WHERE UserId = %s", (userId,))

        if cursor.fetchone():
            return jsonify({"error":"User already exists"}), 400
        
        cursor.execute("INSERT INTO user (UserId, Username, Password, Name) VALUES (%s, %s, %s, %s)", (userId, username, password, name))
        conn.commit()
        cursor.execute("INSERT INTO account (UserId, AccType) VALUES (%s, %s)", (userId, accType))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"message":"User registered successfully"}), 201
    
    except Exception as e:
        print(e)
        return jsonify({"error":"An unexpected error occurred"}), 500


# Login a user
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        userId = data.get('userId')
        password = data.get('password')

        if not userId or not password:
            return jsonify({"error":"Please provide both userId and password"}), 400

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM user WHERE UserId = %s AND Password = %s", (userId, password))
        user_record = cursor.fetchone()

        if user_record:
            cursor.execute("SELECT * FROM account WHERE UserId = %s", (userId,))
            account_record = cursor.fetchone()

            user = User(id=user_record['UserId'], username=user_record['Username'], name=user_record['Name'], accType=account_record['AccType'])
            login_user(user)

            return jsonify({"message": "Login successful"}), 200
        else:
            return jsonify({"error":"User not found"}), 404

    except Exception as e:
        print(e)
        return jsonify({"error":"login Failed"}), 500

# Logout route
@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout successful"}), 200

@app.route('/get-session', methods=['GET'])
@login_required
def get_user_session():
    return jsonify({"userId": current_user.id, "username": current_user.username, "name": current_user.name, "accType": current_user.accType}), 200

# Create a new course
@app.route('/course', methods=['POST'])
@login_required
def create_course():
    try:
        if current_user.accType != 'Admin':
            return jsonify({"error":"Unauthorized. Must be an Admin."}), 401
        
        data = request.get_json()

        courseId = data['courseId']
        courseName = data['courseName']
        period = data['period']

        if not courseId or not courseName or not period:
            return jsonify({"error":"Please provide all required fields. (courseId, courseName, period)"}), 400

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM course WHERE CourseId = %s", (courseId,))

        if cursor.fetchone():
            return jsonify({"error":"Course ID already exists"}), 400

        cursor.execute("INSERT INTO course (CourseId, CourseName, Period) VALUES (%s, %s, %s)", (courseId, courseName, period))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify(message="Course created successfully"), 201
    except Exception as e:
        print(e)
        return jsonify({"error":"Failed to Create Course"}), 500
            

# Get all courses
@app.route('/course', methods=['GET'])
def get_courses():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute('SELECT * FROM Course')
        courses = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(courses), 200
    except Exception as e:
        return jsonify({"error":"Failed to get all courses"}), 500


# Get all courses for student with student_id
@app.route('/course/student/<student_id>', methods=['GET'])
def get_student_courses(student_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT Course.CourseId, Course.CourseName, Course.Period
        FROM User
        INNER JOIN Account ON User.UserId = Account.UserId
        INNER JOIN Membership ON Account.UserId = Membership.UserId
        INNER JOIN Course ON Membership.CourseId = Course.CourseId
        WHERE User.UserId = %s AND Account.AccType = 'Student'
        """
        
        cursor.execute(query, (student_id,))
        courses = cursor.fetchall()

        cursor.close()
        conn.close()
        
        return jsonify(courses), 200
    except Exception as e:
        return jsonify(error="Failed to retrieve student's courses"), 500


# Get all courses for course maintainer with student_id
@app.route('/course/maintainer/<maintainer_id>', methods=['GET'])
def get_maintainer_courses(maintainer_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT Course.CourseId, Course.CourseName, Course.Period
        FROM User
        INNER JOIN Account ON User.UserId = Account.UserId
        INNER JOIN Membership ON Account.UserId = Membership.UserId
        INNER JOIN Course ON Membership.CourseId = Course.CourseId
        WHERE User.UserId = %s AND Account.AccType = 'Course Maintainer'
        """
        
        cursor.execute(query, (maintainer_id,))
        courses = cursor.fetchall()

        cursor.close()
        conn.close()
        
        return jsonify(courses), 200
    except Exception as e:
        return jsonify(error="Failed to retrieve maintainer's courses"), 500

# Register user for course
@app.route('/course/register', methods=['POST'])
def register_course():
    try:
        data = request.json
        user_id = data['userId']
        course_id = data['courseId']

        if not course_id:
            return jsonify({"error": "Please provide a course ID"}), 400

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT AccType FROM Account WHERE UserId = %s', (user_id,))
        user_info = cursor.fetchone()

        if not user_info:
            return jsonify({"error": "User not found"}), 404
        
        accType = user_info['AccType']

        if accType == 'Admin':
            return jsonify({"error": "Admins cannot register for courses"}), 403
        
        if accType == 'Course Maintainer':
            cursor.execute("""
                SELECT Membership.* FROM Membership
                JOIN Account ON Membership.UserId = Account.UserId
                WHERE Membership.CourseId = %s AND Account.AccType = 'Course Maintainer'
            """, (course_id,))
            if cursor.fetchone():
                return jsonify({"error": "A Course Maintainer is already assigned to this course"}), 400
        
        cursor.execute('INSERT INTO Membership (UserId, CourseId) VALUES (%s, %s)', (user_id, course_id))
        conn.commit()
            
        return jsonify(message="Registered for course successfully"), 201
    except Exception as e:
        return jsonify(error="Failed to register for course"), 500
    
# Get all members for a course
@app.route('/members/<course_id>', methods=['GET'])
def get_course_members(course_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Check if the course exists
        cursor.execute("SELECT * FROM Course WHERE CourseId = %s", (course_id,))
        course = cursor.fetchone()
        
        if not course:
            return jsonify({"error": "Course not found"}), 404
        
        query = """
        SELECT User.UserId, User.Username, User.Name, Account.AccType
        FROM Membership
        INNER JOIN User ON Membership.UserId = User.UserId
        INNER JOIN Account ON User.UserId = Account.UserId
        WHERE Membership.CourseId = %s
        """
        
        cursor.execute(query, (course_id,))
        members = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        if members:
            return jsonify({"courseId": course_id, "members": members}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": "Failed to retrieve course members"}), 500

# Get all calendar events for a course
@app.route('/calendar/<course_id>', methods=['GET'])
def calendar_events(course_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Check if the course exists
        cursor.execute("SELECT CourseId FROM Course WHERE CourseId = %s", (course_id,))
        if cursor.fetchone() is None:
            return jsonify({"error": "Course not found"}), 404
        
        # Fetch all calendar events for the course
        query = """
            SELECT EventId, CourseId, StartDate, EndDate, EventTitle, Description
            FROM CalendarEvent
            WHERE CourseId = %s
            ORDER BY StartDate
        """
        cursor.execute(query, (course_id,))
        
        events = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({"courseId": course_id, "calendarEvents": events}), 200
    except Exception as e:
        print(e)
        return jsonify(error="Failed to create calendar event"), 500
    

# Create calendar event
@app.route('/calendar/create', methods=['POST'])
def create_calendar_event():
    try:
        data = request.json
        course_id = data.get('courseId')
        start_date = data.get('startDate')
        end_date = data.get('endDate')
        event_title = data.get('eventTitle')
        description = data.get('description')

        # Validate input
        if not all([course_id, start_date, end_date, event_title, description]):
            return jsonify({"error": "Missing required fields (courseId, startDate, endDate, eventTitle, description)"}), 400
    
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Check if the course exists
        cursor.execute("SELECT * FROM Course WHERE CourseId = %s", (course_id,))
        course = cursor.fetchone()

        if not course:
            return jsonify({"error": "Course not found"}), 404
        
        query = """
            INSERT INTO CalendarEvent (CourseId, StartDate, EndDate, EventTitle, Description)
            VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(query, (course_id, start_date, end_date, event_title, description))
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return jsonify({"message": "Calendar event created successfully"}), 201
    except Exception as e:
        return jsonify(error="Failed to create calendar event"), 500

# Get all calendar events for a student on a specific date
# url eg: /student_daily_calendar_events/123?date=2024-04-18
@app.route('/student_daily_calendar_events/<user_id>', methods=['GET'])
def get_student_daily_calendar_events(user_id):
    # Get the date from query parameters
    event_date = request.args.get('date')
    
    # Validate the provided date format
    try:
        event_date = datetime.strptime(event_date, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({"error": "Invalid date format. Please use YYYY-MM-DD."}), 400
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Verify the user is a student
        cursor.execute("SELECT AccType FROM Account WHERE UserId = %s", (user_id,))
        acc_type = cursor.fetchone()
        if not acc_type or acc_type['AccType'] != 'Student':
            return jsonify({"error": "The user ID does not belong to a student"}), 404
        
        # Find courses the student is a member of and fetch calendar events for those courses on the specified date
        query = """
        SELECT CalendarEvent.EventId, CalendarEvent.CourseId, CalendarEvent.StartDate, CalendarEvent.EndDate, 
               CalendarEvent.EventTitle, CalendarEvent.Description
        FROM Membership
        INNER JOIN CalendarEvent ON Membership.CourseId = CalendarEvent.CourseId
        WHERE Membership.UserId = %s AND DATE(CalendarEvent.StartDate) <= %s AND DATE(CalendarEvent.EndDate) >= %s
        ORDER BY CalendarEvent.StartDate
        """
        
        cursor.execute(query, (user_id, event_date, event_date))
        events = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({"userId": user_id, "date": str(event_date), "calendarEvents": events}), 200
    except Exception as e:
        print(e)  # It's good practice to log the error for debugging purposes
        return jsonify({"error": "Failed to retrieve calendar events for the student on the specified date"}), 500

# Get all calendar events for a student
@app.route('/calendar/student/<user_id>', methods=['GET'])
def student_calendar_events(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Verify the user is a student
        cursor.execute("SELECT AccType FROM Account WHERE UserId = %s", (user_id,))
        acc_type = cursor.fetchone()
        if not acc_type or acc_type['AccType'] != 'Student':
            return jsonify({"error": "The user ID does not belong to a student"}), 404
        
        # Find courses the student is a member of
        cursor.execute("""
            SELECT CourseId FROM Membership
            WHERE UserId = %s
        """, (user_id,))
        courses = cursor.fetchall()
        
        # Fetch calendar events for those courses
        events = []
        for course in courses:
            cursor.execute("""
                SELECT EventId, CourseId, StartDate, EndDate, EventTitle, Description
                FROM CalendarEvent
                WHERE CourseId = %s
                ORDER BY StartDate
            """, (course['CourseId'],))
            events.extend(cursor.fetchall())
        
        cursor.close()
        conn.close()
        
        return jsonify({"userId": user_id, "calendarEvents": events}), 200
    except Exception as e:
        print(e)  # It's good practice to log the error for debugging purposes
        return jsonify({"error": "Failed to retrieve calendar events for the student"}), 500
    
# Create a new discussion forum
@app.route('/create_forum', methods=['POST'])
def create_discussion_forum():
    data = request.json
    course_id = data.get('courseId')
    forum_title = data.get('forumTitle')

    # Validate input
    if not course_id or not forum_title:
        return jsonify({"error": "Missing required fields (courseId, forumTitle)"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Check if the course exists
        cursor.execute("SELECT CourseId FROM Course WHERE CourseId = %s", (course_id,))
        if cursor.fetchone() is None:
            return jsonify({"error": "Course not found"}), 404
        
        # Insert discussion forum
        cursor.execute("""
            INSERT INTO DiscussionForum (ForumTitle, CourseId)
            VALUES (%s, %s)
        """, (forum_title, course_id))
        conn.commit()
        
        # Retrieve the last inserted forum id
        forum_id = cursor.lastrowid
        
        cursor.close()
        conn.close()
        
        return jsonify({"message": "Discussion forum created successfully", "forumId": forum_id}), 201
    
    except Exception as e:
        print(e)
        return jsonify({"error": "Failed to create discussion forum"}), 500


# Get all discussion forums for a course
@app.route('/forum/<course_id>', methods=['GET'])
def get_discussion_forums(course_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Check if the course exists
        cursor.execute("SELECT CourseId FROM Course WHERE CourseId = %s", (course_id,))
        if cursor.fetchone() is None:
            return jsonify({"error": "Course not found"}), 404
        
        # Fetch all discussion forums for the course
        cursor.execute("""
            SELECT ForumId, ForumTitle, CourseId
            FROM DiscussionForum
            WHERE CourseId = %s
        """, (course_id,))
        
        forums = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({"courseId": course_id, "discussionForums": forums}), 200
    except Exception as e:
        print(e)  # It's good practice to log the error for debugging purposes
        return jsonify({"error": "Failed to retrieve discussion forums for the course"}), 500


# Create a new discussion thread
@app.route('/create_thread', methods=['POST'])
def create_thread():
    data = request.json
    user_id = data.get('userId')
    forum_id = data.get('forumId')
    thread_title = data.get('threadTitle', '')
    thread_content = data.get('threadContent', '')
    parent_thread_id = data.get('parentThreadId', None)  # Optional, for replies

    if not all([user_id, forum_id, thread_content]) or (parent_thread_id is None and not thread_title):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Check if the user is a member of the course associated with the forum
        cursor.execute("""
            SELECT Membership.UserId FROM Membership
            JOIN DiscussionForum ON Membership.CourseId = DiscussionForum.CourseId
            WHERE DiscussionForum.ForumId = %s AND Membership.UserId = %s
        """, (forum_id, user_id))
        
        if cursor.fetchone() is None:
            return jsonify({"error": "User is not a member of the course associated with this forum"}), 403
        
        # Insert the discussion thread or reply
        cursor.execute("""
            INSERT INTO DiscussionThread (ForumId, ThreadTitle, ThreadContent, UserId, ParentThreadId)
            VALUES (%s, %s, %s, %s, %s)
        """, (forum_id, thread_title, thread_content, user_id, parent_thread_id))
        conn.commit()
        
        thread_id = cursor.lastrowid
        
        cursor.close()
        conn.close()
        
        return jsonify({"message": "Discussion thread added successfully", "threadId": thread_id}), 201
    
    except Exception as e:
        print(e)  # It's good practice to log the error for debugging purposes
        return jsonify({"error": "Failed to add discussion thread"}), 500
    

# Get all (top-level) threads for a discussion forum
@app.route('/forum_threads/<forum_id>', methods=['GET'])
def get_forum_threads(forum_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Fetch all threads for the forum
        cursor.execute("""
            SELECT ThreadId, ThreadTitle, ThreadContent, UserId, ParentThreadId
            FROM DiscussionThread
            WHERE ForumId = %s AND ParentThreadId IS NULL
            ORDER BY ThreadId ASC
        """, (forum_id,))
        
        threads = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({"forumId": forum_id, "threads": threads}), 200
    except Exception as e:
        print(e)  # It's good practice to log the error for debugging purposes
        return jsonify({"error": "Failed to retrieve forum threads"}), 500
    

# Get all replies for a discussion thread
@app.route('/thread_replies/<thread_id>', methods=['GET'])
def get_thread_replies(thread_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Fetch all replies for the thread
        cursor.execute("""
            SELECT ThreadId, ThreadTitle, ThreadContent, UserId, ParentThreadId
            FROM DiscussionThread
            WHERE ParentThreadId = %s
            ORDER BY ThreadId ASC
        """, (thread_id,))
        
        replies = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({"threadId": thread_id, "replies": replies}), 200
    except Exception as e:
        print(e)  # It's good practice to log the error for debugging purposes
        return jsonify({"error": "Failed to retrieve thread replies"}), 500    


# Create a new section
@app.route('/create_section', methods=['POST'])
def create_section():
    data = request.json
    user_id = data.get('userId')
    course_id = data.get('courseId')
    section_title = data.get('sectionTitle')

    # Validate input
    if not all([user_id, course_id, section_title]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Check if the user is a Course Maintainer
        cursor.execute("SELECT AccType FROM Account WHERE UserId = %s", (user_id,))
        acc_type = cursor.fetchone()
        if not acc_type or acc_type['AccType'] != 'Course Maintainer':
            return jsonify({"error": "Only Course Maintainers can add sections"}), 401
        
        # Check if the course exists
        cursor.execute("SELECT CourseId FROM Course WHERE CourseId = %s", (course_id,))
        if cursor.fetchone() is None:
            return jsonify({"error": "Course not found"}), 404
        
        # Insert the section
        cursor.execute("""
            INSERT INTO Section (SectionTitle, CourseId)
            VALUES (%s, %s)
        """, (section_title, course_id))
        conn.commit()
        
        section_id = cursor.lastrowid
        
        cursor.close()
        conn.close()
        
        return jsonify({"message": "Section created successfully", "sectionId": section_id}), 201
    
    except Exception as e:
        print(e)
        return jsonify({"error": "Failed to create section"}), 500


# Get all sections for a course
@app.route('/section/<course_id>', methods=['GET'])
def get_course_sections(course_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Check if the course exists
        cursor.execute("SELECT CourseId FROM Course WHERE CourseId = %s", (course_id,))
        if cursor.fetchone() is None:
            return jsonify({"error": "Course not found"}), 404
        
        # Fetch all sections for the course
        cursor.execute("""
            SELECT SectionId, SectionTitle, CourseId
            FROM Section
            WHERE CourseId = %s
            ORDER BY SectionId ASC
        """, (course_id,))
        
        sections = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({"courseId": course_id, "sections": sections}), 200
    except Exception as e:
        print(e)  # It's good practice to log the error for debugging purposes
        return jsonify({"error": "Failed to retrieve course sections"}), 500


# Create a new section item
@app.route('/create_section_item', methods=['POST'])
def create_section_item():
    data = request.json
    section_id = data.get('sectionId')
    section_content = data.get('sectionContent')

    # Validate input
    if not all([section_id, section_content]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Verify the section exists
        cursor.execute("SELECT SectionId FROM Section WHERE SectionId = %s", (section_id,))
        if cursor.fetchone() is None:
            return jsonify({"error": "Section not found"}), 404
        
        # Insert the section item
        cursor.execute("""
            INSERT INTO SectionItem (SectionContent, SectionId)
            VALUES (%s, %s)
        """, (section_content, section_id))
        conn.commit()
        
        item_id = cursor.lastrowid
        
        cursor.close()
        conn.close()
        
        return jsonify({"message": "Section item created successfully", "itemId": item_id}), 201
    
    except Exception as e:
        print(e)  # It's good practice to log the error for debugging purposes
        return jsonify({"error": "Failed to create section item"}), 500


# Get all items for a section
@app.route('/section_items/<section_id>', methods=['GET'])
def get_section_items(section_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Check if the section exists
        cursor.execute("SELECT SectionId FROM Section WHERE SectionId = %s", (section_id,))
        if cursor.fetchone() is None:
            return jsonify({"error": "Section not found"}), 404
        
        # Fetch all items for the section
        cursor.execute("""
            SELECT ItemId, SectionContent, SectionId
            FROM SectionItem
            WHERE SectionId = %s
            ORDER BY ItemId ASC
        """, (section_id,))
        
        items = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({"sectionId": section_id, "sectionItems": items}), 200
    except Exception as e:
        print(e)  # It's good practice to log the error for debugging purposes
        return jsonify({"error": "Failed to retrieve section items"}), 500


# Create a new topic
@app.route('/create_topic', methods=['POST'])
def create_topic():
    data = request.json
    section_id = data.get('sectionId')
    topic_title = data.get('topicTitle')

    # Validate input
    if not all([section_id, topic_title]):
        return jsonify({"error": "Missing required fields (sectionId, topicTitle)"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Verify the section exists
        cursor.execute("SELECT SectionId FROM Section WHERE SectionId = %s", (section_id,))
        if cursor.fetchone() is None:
            return jsonify({"error": "Section not found"}), 404
        
        # Insert the topic
        cursor.execute("""
            INSERT INTO Topic (TopicTitle, SectionId)
            VALUES (%s, %s)
        """, (topic_title, section_id))
        conn.commit()
        
        topic_id = cursor.lastrowid
        
        cursor.close()
        conn.close()
        
        return jsonify({"message": "Topic created successfully", "topicId": topic_id}), 201
    
    except Exception as e:
        print(e)  # It's good practice to log the error for debugging purposes
        return jsonify({"error": "Failed to create topic"}), 500


# Get all topics for a section
@app.route('/topic/<section_id>', methods=['GET'])
def get_section_topics(section_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Check if the section exists
        cursor.execute("SELECT SectionId FROM Section WHERE SectionId = %s", (section_id,))
        if cursor.fetchone() is None:
            return jsonify({"error": "Section not found"}), 404
        
        # Fetch all topics for the section
        cursor.execute("""
            SELECT TopicId, TopicTitle, SectionId
            FROM Topic
            WHERE SectionId = %s
            ORDER BY TopicId ASC
        """, (section_id,))
        
        topics = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({"sectionId": section_id, "topics": topics}), 200
    except Exception as e:
        print(e)  # It's good practice to log the error for debugging purposes
        return jsonify({"error": "Failed to retrieve section topics"}), 500


# Get all course content
@app.route('/course/content/<course_id>', methods=['GET'])
def get_course_content(course_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Fetch sections for the course
        cursor.execute("""
            SELECT SectionId, SectionTitle
            FROM Section
            WHERE CourseId = %s
        """, (course_id,))
        sections = cursor.fetchall()

        # For each section, fetch related section items and topics
        for section in sections:
            # Fetch section items
            cursor.execute("""
                SELECT ItemId, SectionContent
                FROM SectionItem
                WHERE SectionId = %s
            """, (section['SectionId'],))
            section_items = cursor.fetchall()
            section['SectionItems'] = section_items
            
            # Fetch topics
            cursor.execute("""
                SELECT TopicId, TopicTitle
                FROM Topic
                WHERE SectionId = %s
            """, (section['SectionId'],))
            topics = cursor.fetchall()
            section['Topics'] = topics
        
        cursor.close()
        conn.close()
        
        return jsonify({"courseId": course_id, "sections": sections}), 200
    except Exception as e:
        print(e)  # It's good practice to log the error for debugging purposes
        return jsonify({"error": "Failed to retrieve course content"}), 500


################################################
# Error handlers

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error="Resource not found"), 404

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify(error="Internal server error"), 500
    

if __name__ == '__main__':
    app.run(port=8080, debug=True)