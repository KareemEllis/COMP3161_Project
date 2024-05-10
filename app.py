from dotenv import load_dotenv
import os

from flask import Flask, request, jsonify, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_cors import CORS
import mysql.connector
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)
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


def getAccountType(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT AccType FROM Account WHERE UserId = %s", (user_id,))
    acc_type = cursor.fetchone()
    cursor.close()
    conn.close()
    return acc_type['AccType']

#####################################################################################################
#####################################################################################################
#####################################################################################################

@app.route('/users', methods=['GET'])
def get_all_users():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Execute the query to fetch all users with their account type
        cursor.execute("""
            SELECT User.UserId, User.Username, User.Name, Account.AccType
            FROM User
            JOIN Account ON User.UserId = Account.UserId
        """)
        
        users = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify(users), 200
    except Exception as e:
        print(e)  # It's good practice to log the error for debugging purposes
        return jsonify({"error": "Failed to retrieve users"}), 500


@app.route('/user/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Fetch the user by userId, including their account type
        cursor.execute("""
            SELECT User.UserId, User.Username, User.Name, Account.AccType
            FROM User
            JOIN Account ON User.UserId = Account.UserId
            WHERE User.UserId = %s
        """, (user_id,))
        
        user = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if user:
            return jsonify(user), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        print(e)  # It's good practice to log the error for debugging purposes
        return jsonify({"error": "Failed to retrieve user data"}), 500


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
            return jsonify({"message":"Invalid request. Please provide all required fields (UserId, Username, Name, Password, AccType)"}), 400
        
        if accType not in ['Admin', 'Course Maintainer', 'Student']:
            return jsonify({"message":"Invalid account type. Must be one of 'Admin', 'Course Maintainer', 'Student'"}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if user already exists
        cursor.execute("SELECT * FROM user WHERE UserId = %s", (userId,))

        if cursor.fetchone():
            return jsonify({"message":"User already exists"}), 400
        
        cursor.execute("INSERT INTO user (UserId, Username, Password, Name) VALUES (%s, %s, %s, %s)", (userId, username, password, name))
        conn.commit()
        cursor.execute("INSERT INTO account (UserId, AccType) VALUES (%s, %s)", (userId, accType))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"message":"User registered successfully"}), 201
    
    except Exception as e:
        print(e)
        return jsonify({"message":"An unexpected error occurred"}), 500


# Login a user
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        userId = data.get('userId')
        password = data.get('password')

        if not userId or not password:
            return jsonify({"message":"Please provide both userId and password"}), 400

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM user WHERE UserId = %s AND Password = %s", (userId, password))
        user_record = cursor.fetchone()

        if user_record:
            cursor.execute("SELECT * FROM account WHERE UserId = %s", (userId,))
            account_record = cursor.fetchone()

            user = User(id=user_record['UserId'], username=user_record['Username'], name=user_record['Name'], accType=account_record['AccType'])
            login_user(user)

            return jsonify({
                "message": "Login successful", 
                "user": {
                    "userId": current_user.id, 
                    "username": current_user.username, 
                    "name": current_user.name, 
                    "accType": current_user.accType
                }
            }), 200
        else:
            return jsonify({"message":"User not found"}), 404

    except Exception as e:
        print(e)
        return jsonify({"message":"login Failed"}), 500

# Logout route
@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return jsonify({"message": "Logout successful"}), 200

@app.route('/get-session', methods=['GET'])
def get_user_session():
    # if not current_user.is_authenticated:
    #     return jsonify({"message": "Not logged in"}), 401
    return jsonify({
        "userId": current_user.id, 
        "username": current_user.username, 
        "name": current_user.name, 
        "accType": current_user.accType
    }), 200

# Create a new course
@app.route('/course', methods=['POST'])
def create_course():
    try:
        data = request.get_json()

        userId = data['userId']
        courseId = data['courseId']
        courseName = data['courseName']
        period = data['period']

        print(userId)

        accType = getAccountType(userId)

        if accType != 'Admin':
            return jsonify({"message":"Unauthorized. Must be an Admin."}), 401

        if not courseId or not courseName or not period:
            return jsonify({"message":"Please provide all required fields. (courseId, courseName, period)"}), 400

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM course WHERE CourseId = %s", (courseId,))

        if cursor.fetchone():
            return jsonify({"message":"Course ID already exists"}), 400

        cursor.execute("INSERT INTO course (CourseId, CourseName, Period) VALUES (%s, %s, %s)", (courseId, courseName, period))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify(message="Course created successfully"), 201
    except Exception as e:
        print(e)
        return jsonify({"message":"Failed to Create Course"}), 500
            

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
        print(e)
        return jsonify({"message":"Failed to get all courses"}), 500

@app.route('/course/<course_id>', methods=['GET'])
def get_course_by_id(course_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Fetch the course by courseId
        cursor.execute("""
            SELECT CourseId, CourseName, Period
            FROM Course
            WHERE CourseId = %s
        """, (course_id,))
        
        course = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if course:
            return jsonify(course), 200
        else:
            return jsonify({"message": "Course not found"}), 404
    except Exception as e:
        print(e)
        return jsonify({"message": "Failed to retrieve course"}), 500
    
# Get all courses for student with student_id
@app.route('/course/student/<student_id>', methods=['GET'])
def get_student_courses(student_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        accType = getAccountType(student_id)

        if accType != 'Student':
            return jsonify({"message": "User not a Student."}), 401
        
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
        print(e)
        return jsonify(message="Failed to retrieve student's courses"), 500


# Get all courses for course maintainer with student_id
@app.route('/course/maintainer/<maintainer_id>', methods=['GET'])
def get_maintainer_courses(maintainer_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        accType = getAccountType(maintainer_id)

        if accType != 'Course Maintainer':
            return jsonify({"message": "User not a Course Maintainer."}), 401
        
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
        print(e)
        return jsonify(message="Failed to retrieve maintainer's courses"), 500

# Register user for course
@app.route('/course/register', methods=['POST'])
def register_course():
    try:
        data = request.json
        user_id = data['userId']
        course_id = data['courseId']

        if not course_id:
            return jsonify({"message": "Please provide a course ID"}), 400

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        accType = getAccountType(user_id)

        if accType == 'Admin':
            return jsonify({"message": "Admins cannot register for courses"}), 403
        
        if accType == 'Course Maintainer':
            cursor.execute("""
                SELECT Membership.* FROM Membership
                JOIN Account ON Membership.UserId = Account.UserId
                WHERE Membership.CourseId = %s AND Account.AccType = 'Course Maintainer'
            """, (course_id,))
            if cursor.fetchone():
                return jsonify({"message": "A Course Maintainer is already assigned to this course"}), 400
        
        cursor.execute('INSERT INTO Membership (UserId, CourseId) VALUES (%s, %s)', (user_id, course_id))
        conn.commit()
            
        return jsonify(message="Registered for course successfully"), 201
    except Exception as e:
        print(e)
        return jsonify(message="Failed to register for course"), 500
    
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
            return jsonify({"message": "Course not found"}), 404
        
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
        return jsonify({"message": "Failed to retrieve course members"}), 500

# Get course member by member_id
@app.route('/course_member/<member_id>', methods=['GET'])
def get_course_member_by_id(member_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Fetch the course member by memberId, including the member's user data
        cursor.execute("""
            SELECT Membership.MemberId, Membership.UserId, Membership.CourseId, 
                   User.Username, User.Name
            FROM Membership
            JOIN User ON Membership.UserId = User.UserId
            WHERE Membership.MemberId = %s
        """, (member_id,))
        
        member = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if member:
            return jsonify(member), 200
        else:
            return jsonify({"message": "Course member not found"}), 404
    except Exception as e:
        print(e)  # It's good practice to log the error for debugging purposes
        return jsonify({"message": "Failed to retrieve course member"}), 500
    

# Get all calendar events for a course
@app.route('/calendar/course/<course_id>', methods=['GET'])
def calendar_events(course_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Check if the course exists
        cursor.execute("SELECT CourseId FROM Course WHERE CourseId = %s", (course_id,))
        if cursor.fetchone() is None:
            return jsonify({"message": "Course not found"}), 404
        
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
        return jsonify(message="Failed to create calendar event"), 500
    

# Get calendar event by event_id
@app.route('/calendar/<event_id>', methods=['GET'])
def get_calendar_event_by_id(event_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Fetch the calendar event by eventId
        cursor.execute("""
            SELECT EventId, CourseId, StartDate, EndDate, EventTitle, Description
            FROM CalendarEvent
            WHERE EventId = %s
        """, (event_id,))
        
        event = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if event:
            return jsonify(event), 200
        else:
            return jsonify({"message": "Calendar event not found"}), 404
    except Exception as e:
        print(e)  # It's good practice to log the error for debugging purposes
        return jsonify({"message": "Failed to retrieve calendar event"}), 500
    

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
            return jsonify({"message": "Missing required fields (courseId, startDate, endDate, eventTitle, description)"}), 400
    
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Check if the course exists
        cursor.execute("SELECT * FROM Course WHERE CourseId = %s", (course_id,))
        course = cursor.fetchone()

        if not course:
            return jsonify({"message": "Course not found"}), 404
        
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
        print(e)
        return jsonify(message="Failed to create calendar event"), 500

# Get all calendar events for a student on a specific date
# url eg: /student_daily_calendar_events/123?date=2024-04-18
@app.route('/calendar/user/daily/<user_id>', methods=['GET'])
def get_daily_calendar_events(user_id):
    # Get the date from query parameters
    event_date = request.args.get('date')
    
    # Validate the provided date format
    try:
        event_date = datetime.strptime(event_date, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({"message": "Invalid date format. Please use YYYY-MM-DD."}), 400
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Verify the user is a student
        acc_type = getAccountType(user_id)

        if acc_type == 'Admin':
            return jsonify({"message": "User must be a Student or Course Maintainer"}), 404
        
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
        print(e)
        return jsonify({"message": "Failed to retrieve calendar events for the user on the specified date"}), 500

# Get all calendar events for a user
@app.route('/calendar/user/<user_id>', methods=['GET'])
def user_calendar_events(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Verify the user is a user
        acc_type = getAccountType(user_id)
        if acc_type == 'Admin':
            return jsonify({"message": "User must be a Student or Course Maintainer"}), 404
        
        # Find courses the user is a member of
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
        print(e)
        return jsonify({"message": "Failed to retrieve calendar events for the user"}), 500
    
# Create a new discussion forum
@app.route('/create_forum', methods=['POST'])
def create_discussion_forum():
    data = request.json
    course_id = data.get('courseId')
    forum_title = data.get('forumTitle')

    # Validate input
    if not course_id or not forum_title:
        return jsonify({"message": "Missing required fields (courseId, forumTitle)"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Check if the course exists
        cursor.execute("SELECT CourseId FROM Course WHERE CourseId = %s", (course_id,))
        if cursor.fetchone() is None:
            return jsonify({"message": "Course not found"}), 404
        
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
        return jsonify({"message": "Failed to create discussion forum"}), 500


# Get all discussion forums for a course
@app.route('/forum/<course_id>', methods=['GET'])
def get_discussion_forums(course_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Check if the course exists
        cursor.execute("SELECT CourseId FROM Course WHERE CourseId = %s", (course_id,))
        if cursor.fetchone() is None:
            return jsonify({"message": "Course not found"}), 404
        
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
        print(e)
        return jsonify({"message": "Failed to retrieve discussion forums for the course"}), 500


@app.route('/get-forum/<forum_id>', methods=['GET'])
def get_forum_by_id(forum_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Fetch the forum by forumId
        cursor.execute("""
            SELECT ForumId, ForumTitle, CourseId
            FROM DiscussionForum
            WHERE ForumId = %s
        """, (forum_id,))
        
        forum = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if forum:
            return jsonify(forum), 200
        else:
            return jsonify({"error": "Forum not found"}), 404
    except Exception as e:
        print(e)  # It's good practice to log the error for debugging purposes
        return jsonify({"error": "Failed to retrieve forum"}), 500
    

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
        return jsonify({"message": "Missing required fields"}), 400

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
            return jsonify({"message": "User is not a member of the course associated with this forum"}), 403
        
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
        print(e)
        return jsonify({"message": "Failed to add discussion thread"}), 500
    

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
            WHERE ForumId = %s
            ORDER BY ThreadId ASC
        """, (forum_id,))
        
        threads = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({"forumId": forum_id, "threads": threads}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Failed to retrieve forum threads"}), 500
    

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
        
        return jsonify({"ThreadId": thread_id, "replies": replies}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Failed to retrieve thread replies"}), 500    


# Create a new section
@app.route('/create_section', methods=['POST'])
def create_section():
    data = request.json
    user_id = data.get('userId')
    course_id = data.get('courseId')
    section_title = data.get('sectionTitle')

    # Validate input
    if not all([user_id, course_id, section_title]):
        return jsonify({"message": "Missing required fields"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Check if the user is a Course Maintainer
        acc_type = getAccountType(user_id)
        print(acc_type)
        if acc_type != 'Course Maintainer':
            return jsonify({"message": "Only Course Maintainers can add sections"}), 401
        
        # Check if the course exists
        cursor.execute("SELECT CourseId FROM Course WHERE CourseId = %s", (course_id,))
        if cursor.fetchone() is None:
            return jsonify({"message": "Course not found"}), 404
        
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
        return jsonify({"message": "Failed to create section"}), 500


# Get all sections for a course
@app.route('/section/<course_id>', methods=['GET'])
def get_course_sections(course_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Check if the course exists
        cursor.execute("SELECT CourseId FROM Course WHERE CourseId = %s", (course_id,))
        if cursor.fetchone() is None:
            return jsonify({"message": "Course not found"}), 404
        
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
        print(e)
        return jsonify({"message": "Failed to retrieve course sections"}), 500


# Create a new section item
@app.route('/create_section_item', methods=['POST'])
def create_section_item():
    data = request.json
    section_id = data.get('sectionId')
    section_content = data.get('sectionContent')

    # Validate input
    if not all([section_id, section_content]):
        return jsonify({"message": "Missing required fields"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Verify the section exists
        cursor.execute("SELECT SectionId FROM Section WHERE SectionId = %s", (section_id,))
        if cursor.fetchone() is None:
            return jsonify({"message": "Section not found"}), 404
        
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
        print(e)
        return jsonify({"message": "Failed to create section item"}), 500


# Get all items for a section
@app.route('/section_items/<section_id>', methods=['GET'])
def get_section_items(section_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Check if the section exists
        cursor.execute("SELECT SectionId FROM Section WHERE SectionId = %s", (section_id,))
        if cursor.fetchone() is None:
            return jsonify({"message": "Section not found"}), 404
        
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
        print(e)
        return jsonify({"message": "Failed to retrieve section items"}), 500


# Create a new topic
@app.route('/create_topic', methods=['POST'])
def create_topic():
    data = request.json
    section_id = data.get('sectionId')
    topic_title = data.get('topicTitle')

    # Validate input
    if not all([section_id, topic_title]):
        return jsonify({"message": "Missing required fields (sectionId, topicTitle)"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Verify the section exists
        cursor.execute("SELECT SectionId FROM Section WHERE SectionId = %s", (section_id,))
        if cursor.fetchone() is None:
            return jsonify({"message": "Section not found"}), 404
        
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
        print(e)
        return jsonify({"message": "Failed to create topic"}), 500


# Get all topics for a section
@app.route('/topic/<section_id>', methods=['GET'])
def get_section_topics(section_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Check if the section exists
        cursor.execute("SELECT SectionId FROM Section WHERE SectionId = %s", (section_id,))
        if cursor.fetchone() is None:
            return jsonify({"message": "Section not found"}), 404
        
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
        print(e)
        return jsonify({"message": "Failed to retrieve section topics"}), 500


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
        print(e)
        return jsonify({"message": "Failed to retrieve course content"}), 500


# Create a new assignment
@app.route('/create_assignment', methods=['POST'])
def create_assignment():
    data = request.json
    course_id = data.get('courseId')
    assignment_title = data.get('assignmentTitle')
    due_date = data.get('dueDate')

    # Validate input
    if not all([course_id, assignment_title, due_date]):
        return jsonify({"message": "Missing required fields"}), 400

    # Validate due_date format
    try:
        due_date = datetime.strptime(due_date, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({"message": "Invalid dueDate format. Use YYYY-MM-DD."}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Check if the course exists
        cursor.execute("SELECT CourseId FROM Course WHERE CourseId = %s", (course_id,))
        if cursor.fetchone() is None:
            return jsonify({"message": "Course not found"}), 404
        
        # Insert the assignment
        cursor.execute("""
            INSERT INTO Assignment (AssignmentTitle, CourseId, DueDate)
            VALUES (%s, %s, %s)
        """, (assignment_title, course_id, due_date))
        conn.commit()
        
        assignment_id = cursor.lastrowid
        
        cursor.close()
        conn.close()
        
        return jsonify({"message": "Assignment created successfully", "assignmentId": assignment_id}), 201
    
    except Exception as e:
        print(e)
        return jsonify({"message": "Failed to create assignment"}), 500
    

# Get all assignments for a course
@app.route('/assignment/course/<course_id>', methods=['GET'])
def get_course_assignments(course_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Check if the course exists
        cursor.execute("SELECT CourseId FROM Course WHERE CourseId = %s", (course_id,))
        if cursor.fetchone() is None:
            return jsonify({"message": "Course not found"}), 404
        
        # Fetch all assignments for the course
        cursor.execute("""
            SELECT AssignmentId, AssignmentTitle, CourseId, DueDate
            FROM Assignment
            WHERE CourseId = %s
            ORDER BY DueDate ASC
        """, (course_id,))
        
        assignments = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({"courseId": course_id, "assignments": assignments}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Failed to retrieve assignments for the course"}), 500
    

# Get assignment by assignment_id
@app.route('/assignment/<assignment_id>', methods=['GET'])
def get_assignment_by_id(assignment_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Fetch the assignment by assignmentId
        cursor.execute("""
            SELECT AssignmentId, AssignmentTitle, CourseId, DueDate
            FROM Assignment
            WHERE AssignmentId = %s
        """, (assignment_id,))
        
        assignment = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if assignment:
            return jsonify(assignment), 200
        else:
            return jsonify({"message": "Assignment not found"}), 404
    except Exception as e:
        print(e)
        return jsonify({"message": "Failed to retrieve assignment"}), 500
    

# Create a new assignment submission
@app.route('/assignment/submit', methods=['POST'])
def make_assignment_submission():
    data = request.json
    user_id = data.get('userId')
    assignment_id = data.get('assignmentId')
    submission_date = datetime.now().strftime('%Y-%m-%d')  # Use current date for submission date

    # Validate input
    if not all([user_id, assignment_id]):
        return jsonify({"message": "Missing required fields"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Check if the user is a student
        acc_type = getAccountType(user_id)
        if acc_type != 'Student':
            return jsonify({"message": "Only students can make submissions"}), 403
        
        # Check if the assignment exists
        cursor.execute("SELECT AssignmentId FROM Assignment WHERE AssignmentId = %s", (assignment_id,))
        if cursor.fetchone() is None:
            return jsonify({"message": "Assignment not found"}), 404
        
        # Insert the assignment submission
        cursor.execute("""
            INSERT INTO AssignmentSubmission (AssignmentId, UserId, SubmissionDate, Grade)
            VALUES (%s, %s, %s, NULL)
        """, (assignment_id, user_id, submission_date))
        conn.commit()
        
        submission_id = cursor.lastrowid
        
        cursor.close()
        conn.close()
        
        return jsonify({"message": "Assignment submission successful", "submissionId": submission_id}), 201
    
    except Exception as e:
        print(e)
        return jsonify({"message": "Failed to make assignment submission"}), 500


@app.route('/assignment_submissions/<assignment_id>', methods=['GET'])
def get_assignment_submissions(assignment_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Fetch all submissions for the assignment, including the user's data
        cursor.execute("""
            SELECT AssignmentSubmission.SubmissionId, AssignmentSubmission.AssignmentId, 
                   AssignmentSubmission.UserId, AssignmentSubmission.SubmissionDate, 
                   AssignmentSubmission.Grade, User.Username, User.Name
            FROM AssignmentSubmission
            JOIN User ON AssignmentSubmission.UserId = User.UserId
            WHERE AssignmentSubmission.AssignmentId = %s
            ORDER BY AssignmentSubmission.SubmissionDate ASC
        """, (assignment_id,))
        
        submissions_with_user = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify(submissions_with_user), 200
    except Exception as e:
        print(e)  # It's good practice to log the error for debugging purposes
        return jsonify({"error": "Failed to retrieve assignment submissions with user data"}), 500


@app.route('/assignment_submissions/submission/<submission_id>', methods=['GET'])
def get_assignment_submission_by_id(submission_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Fetch the assignment submission by submissionId, along with user and assignment details
        cursor.execute("""
            SELECT AssignmentSubmission.SubmissionId, AssignmentSubmission.AssignmentId, 
                   AssignmentSubmission.UserId, AssignmentSubmission.SubmissionDate, 
                   AssignmentSubmission.Grade, User.Username, User.Name, 
                   Assignment.AssignmentTitle, Assignment.DueDate
            FROM AssignmentSubmission
            JOIN User ON AssignmentSubmission.UserId = User.UserId
            JOIN Assignment ON AssignmentSubmission.AssignmentId = Assignment.AssignmentId
            WHERE AssignmentSubmission.SubmissionId = %s
        """, (submission_id,))
        
        submission = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if submission:
            return jsonify(submission), 200
        else:
            return jsonify({"message": "Assignment submission not found"}), 404
    except Exception as e:
        print(e)
        return jsonify({"message": "Failed to retrieve assignment submission"}), 500
    

# Get a user's submission for a specific assignment
@app.route('/user_assignment_submission/<assignment_id>/<user_id>', methods=['GET'])
def get_user_assignment_submission_with_user_data(assignment_id, user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Fetch the user's submission for the specified assignment, including the user's data
        cursor.execute("""
            SELECT AssignmentSubmission.SubmissionId, AssignmentSubmission.AssignmentId, 
                   AssignmentSubmission.UserId, AssignmentSubmission.SubmissionDate, 
                   AssignmentSubmission.Grade, User.Username, User.Name
            FROM AssignmentSubmission
            JOIN User ON AssignmentSubmission.UserId = User.UserId
            WHERE AssignmentSubmission.AssignmentId = %s AND AssignmentSubmission.UserId = %s
        """, (assignment_id, user_id))
        
        submission_with_user_data = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if submission_with_user_data:
            return jsonify(submission_with_user_data), 200
        else:
            return jsonify({"error": "Submission not found"}), 404
    except Exception as e:
        print(e)  # It's good practice to log the error for debugging purposes
        return jsonify({"error": "Failed to retrieve user's assignment submission with user data"}), 500


# Get all assignments for a student
@app.route('/student_assignments/<int:student_id>', methods=['GET'])
def get_student_assignments(student_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Check if the ID belongs to a student
        cursor.execute("""
            SELECT UserId FROM Account WHERE UserId = %s AND AccType = 'Student'
        """, (student_id,))
        if cursor.fetchone() is None:
            return jsonify({"error": "The provided ID does not belong to a student"}), 404

        # Get all courses the student is a member of
        cursor.execute("""
            SELECT Course.CourseId, Course.CourseName
            FROM Membership
            JOIN Course ON Membership.CourseId = Course.CourseId
            WHERE Membership.UserId = %s
        """, (student_id,))
        courses = cursor.fetchall()

        # For each course, fetch all assignments
        for course in courses:
            cursor.execute("""
                SELECT AssignmentId, AssignmentTitle, DueDate
                FROM Assignment
                WHERE CourseId = %s
            """, (course['CourseId'],))
            assignments = cursor.fetchall()
            course['Assignments'] = assignments

        cursor.close()
        conn.close()
        return jsonify({"studentId": student_id, "courses": courses}), 200
    except Exception as e:
        print(e)  # It's good practice to log the error for debugging purposes
        return jsonify({"error": "Failed to retrieve assignments for the student"}), 500


# Assign a grade to an assignment submission
@app.route('/assign_grade', methods=['POST'])
def assign_grade():
    data = request.json
    user_id = data.get('userId')
    submission_id = data.get('submissionId')
    grade = data.get('grade')

    # Validate input
    if not submission_id or grade is None:
        return jsonify({"message": "Missing required fields (submissionId, grade)"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        acc_type = getAccountType(user_id)
        if acc_type != 'Course Maintainer':
            return jsonify({"message": "Only Course Maintainers can assign grades"}), 403
        
        # Check if the submission exists
        cursor.execute("SELECT SubmissionId FROM AssignmentSubmission WHERE SubmissionId = %s", (submission_id,))
        if cursor.fetchone() is None:
            return jsonify({"message": "Submission not found"}), 404
        
        # Update the submission with the grade
        cursor.execute("""
            UPDATE AssignmentSubmission
            SET Grade = %s
            WHERE SubmissionId = %s
        """, (grade, submission_id))
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return jsonify({"message": "Grade assigned successfully"}), 200
    
    except Exception as e:
        print(e)
        return jsonify({"message": "Failed to assign grade"}), 500


# Get all courses with 50 or more students
@app.route('/courses_with_many_students', methods=['GET'])
def get_courses_with_many_students():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Execute the query
        cursor.execute("""
            SELECT Course.CourseId, Course.CourseName, COUNT(Membership.UserId) AS StudentCount
            FROM Course
            JOIN Membership ON Course.CourseId = Membership.CourseId
            GROUP BY Course.CourseId
            HAVING COUNT(Membership.UserId) >= 50
        """)
        
        courses = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify(courses), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Failed to retrieve courses with 50 or more students"}), 500


# Get all students enrolled in 5 or more courses
@app.route('/students_with_many_courses', methods=['GET'])
def get_students_with_many_courses():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Execute the query
        cursor.execute("""
            SELECT User.UserId, User.Username, User.Name, COUNT(Membership.CourseId) AS CourseCount
            FROM User
            JOIN Account ON User.UserId = Account.UserId
            JOIN Membership ON User.UserId = Membership.UserId
            WHERE Account.AccType = 'Student'
            GROUP BY User.UserId
            HAVING COUNT(Membership.CourseId) >= 5
        """)
        
        students = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify(students), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Failed to retrieve students enrolled in 5 or more courses"}), 500


# Get all course maintainers teaching 3 or more courses
@app.route('/maintainers_with_many_courses', methods=['GET'])
def get_maintainers_with_many_courses():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Execute the query
        cursor.execute("""
            SELECT User.UserId, User.Username, User.Name, COUNT(Membership.CourseId) AS CourseCount
            FROM User
            JOIN Account ON User.UserId = Account.UserId
            JOIN Membership ON User.UserId = Membership.UserId
            WHERE Account.AccType = 'Course Maintainer'
            GROUP BY User.UserId
            HAVING COUNT(Membership.CourseId) >= 3
        """)
        
        maintainers = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify(maintainers), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Failed to retrieve Course Maintainers teaching 3 or more courses"}), 500


# Get the 10 most enrolled courses
@app.route('/top_enrolled_courses', methods=['GET'])
def get_top_enrolled_courses():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Execute the query
        cursor.execute("""
            SELECT Course.CourseId, Course.CourseName, COUNT(Membership.UserId) AS EnrollmentCount
            FROM Course
            JOIN Membership ON Course.CourseId = Membership.CourseId
            GROUP BY Course.CourseId
            ORDER BY EnrollmentCount DESC
            LIMIT 10
        """)
        
        top_courses = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify(top_courses), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Failed to retrieve the 10 most enrolled courses"}), 500


# Get the top 10 students with the highest overall averages
@app.route('/top_students_by_average', methods=['GET'])
def get_top_students_by_average():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Execute the query to calculate the average grades and fetch the top 10 students
        cursor.execute("""
            SELECT User.UserId, User.Username, User.Name, AVG(AssignmentSubmission.Grade) AS AverageGrade
            FROM User
            JOIN AssignmentSubmission ON User.UserId = AssignmentSubmission.UserId
            WHERE AssignmentSubmission.Grade IS NOT NULL
            GROUP BY User.UserId
            ORDER BY AverageGrade DESC
            LIMIT 10
        """)
        
        top_students = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify(top_students), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Failed to retrieve the top 10 students with the highest overall averages"}), 500
    

################################################
# Error handlers

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(message="Resource not found"), 404

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify(message="Internal server error"), 500
    

if __name__ == '__main__':
    app.run(port=8080, debug=True)