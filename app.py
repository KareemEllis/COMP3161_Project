from dotenv import load_dotenv
import os

from flask import Flask, request, jsonify
import mysql.connector

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

db_host = os.getenv('HOST')
db_username = os.getenv('USERNAME')
db_password = os.getenv('PASSWORD')
db = 'OURVLE'


# Register a new user
@app.route('/api/register', methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        
        userId = data.get('userId')
        password = data.get('password')
        role = data.get('role')

        if not userId or not password or not role:
            raise ValueError("Invalid request. Please provide all required fields")
        
        conn = mysql.connector.connect(
            host=db_host, 
            user=db_username, 
            password=db_password, 
            database=db
        )

        cursor = conn.cursor()

        cursor.execute(f"SELECT * FROM users WHERE userId = {userId}")

        if cursor.fetchone():
            raise ValueError("User already exists")
        
        cursor.execute(f"INSERT INTO users (userId, password, role) VALUES ({userId}, {password}, {role})")

        conn.commit()

        return jsonify(message="User registered successfully"), 201
    
    except ValueError as e:
        return jsonify(error=str(e)), 400
    
    except Exception as e:
        return jsonify(error="An unexpected error occurred"), 500
    
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


# Login a user
@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        userId = data.get('userId')
        password = data.get('password')

        if not userId or not password:
            raise ValueError("Please provide both userId and password")

        conn = mysql.connector.connect(
            host=db_host, 
            user=db_username, 
            password=db_password, 
            database=db
        )
        cursor = conn.cursor()

        cursor.execute(f"SELECT password FROM users WHERE userId = {userId}")
        user = cursor.fetchone()

        if user:
            stored_password = user[0] # Assuming Password is the first column in the table
            
            if password == stored_password: 
                return jsonify({"message": "Login successful", "userId": userId}), 200
            else:
                return jsonify({"error": "Invalid credentials"}), 401
        else:
            return jsonify({"error": "User not found"}), 404

    except ValueError as e:
        return jsonify(error=str(e)), 400
    
    except Exception as e:
        return jsonify(error="Login failed"), 401
    
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


# Create a new course
@app.route('/course', methods=['POST'])
def create_course():
    try:
        data = request.get_json()

        courseId = data['courseId']
        courseName = data['courseName']
        period = data['period']

        if not courseId or not courseName or not period:
            raise ValueError("Please provide all required fields")

        conn = mysql.connector.connect(
            host=db_host, 
            user=db_username, 
            password=db_password, 
            database=db
        )
        cursor = conn.cursor()

        cursor.execute(f"SELECT * FROM courses WHERE courseId = {courseId}")

        if cursor.fetchone():
            raise ValueError("Course already exists")

        # Use parameterized query to prevent SQL injection
        query = "INSERT INTO courses (courseId, courseName, period) VALUES (%s, %s, %s)"
        cursor.execute(query, (courseId, courseName, period))

        conn.commit()

        return jsonify(message="Course created successfully"), 201
    
    except ValueError as e:
        return jsonify(error=str(e)), 400
    
    except Exception as e:
        return jsonify(error="Failed to create course"), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/courses', methods=['GET'])
def get_courses():
    try:
        # Implement logic to retrieve all courses
        return jsonify(courses=[]), 200
    except Exception as e:
        return jsonify(error="Failed to retrieve courses"), 500

@app.route('/student/courses/<student_id>', methods=['GET'])
def get_student_courses(student_id):
    try:
        # Implement logic to retrieve courses for a particular student
        return jsonify(courses=[]), 200
    except Exception as e:
        return jsonify(error="Failed to retrieve student's courses"), 500

@app.route('/lecturer/courses/<lecturer_id>', methods=['GET'])
def get_lecturer_courses(lecturer_id):
    try:
        # Implement logic to retrieve courses taught by a particular lecturer
        return jsonify(courses=[]), 200
    except Exception as e:
        return jsonify(error="Failed to retrieve lecturer's courses"), 500

@app.route('/student/course/register', methods=['POST'])
def register_for_course():
    try:
        # Implement course registration logic here
        return jsonify(message="Registered for course successfully"), 200
    except Exception as e:
        return jsonify(error="Failed to register for course"), 500
    
@app.route('/lecturer/course/register', methods=['POST'])
def register_for_course():
    try:
        # Implement course registration logic here
        return jsonify(message="Registered for course successfully"), 200
    except Exception as e:
        return jsonify(error="Failed to register for course"), 500

@app.route('/course/members/<course_id>', methods=['GET'])
def get_course_members(course_id):
    try:
        # Implement logic to retrieve members of a particular course
        return jsonify(members=[]), 200
    except Exception as e:
        return jsonify(error="Failed to retrieve course members"), 500

@app.route('/course/calendar/<course_id>', methods=['GET', 'POST'])
def calendar_events():
    try:
        if request.method == 'POST':
            # Implement logic to create a calendar event for a course
            return jsonify(message="Calendar event created successfully"), 201
        
        # Implement logic to retrieve all calendar events for a course
        return jsonify(events=[]), 200
    except Exception as e:
        return jsonify(error="Failed to process calendar events"), 500

@app.route('/student/calendar/<student_id>', methods=['GET'])
def student_calendar_events():
    try:
        # Implement logic to retrieve all calendar events for a student on a particular date
        return jsonify(events=[]), 200
    except Exception as e:
        return jsonify(error="Failed to retrieve student's calendar events"), 500
    
@app.route('/forum/<course_id>', methods=['GET', 'POST'])
def forums(course_id):
    try:
        if request.method == 'POST':
            # Implement logic to create a forum for a particular course
            return jsonify(message="Forum created successfully"), 201
        # Implement logic to retrieve all forums for a particular course
        return jsonify(forums=[]), 200
    except Exception as e:
        return jsonify(error="Failed to process forum requests"), 500

@app.route('/forum/thread/<forum_id>', methods=['GET', 'POST'])
def discussion_thread(forum_id):
    try:
        if request.method == 'POST':
            # Implement logic to add a new discussion thread to a forum
            return jsonify(message="Discussion thread added successfully"), 201
        # Implement logic to retrieve all discussion threads for a particular forum
        return jsonify(threads=[]), 200
    except Exception as e:
        return jsonify(error="Failed to process discussion thread requests"), 500

@app.route('/thread/reply/<thread_id>', methods=['POST'])
def reply_to_thread(thread_id):
    try:
        # Implement logic to reply to a thread (replies can have replies)
        return jsonify(message="Reply added successfully"), 201
    except Exception as e:
        return jsonify(error="Failed to add reply to thread"), 500

#######################################################################
#######################################################################
#######################################################################
#######################################################################
#######################################################################

@app.route('/course/content/<course_id>', methods=['GET', 'POST'])
def course_content(course_id):
    try:
        if request.method == 'POST':
            # Implement logic to add course content
            return jsonify(message="Content added successfully"), 201
        # Retrieve all course content for a particular course
        return jsonify(content=[]), 200
    except Exception as e:
        return jsonify(error="Failed to process course content requests"), 500

@app.route('/assignment/submit/<assignment_id>', methods=['POST'])
def submit_assignment(assignment_id):
    try:
        # Implement logic for a student submitting an assignment
        return jsonify(message="Assignment submitted successfully"), 201
    except Exception as e:
        return jsonify(error="Failed to submit assignment"), 500

# @app.route('/assignment/grade', methods=['POST'])
# def grade_assignment():
#     try:
#         # Implement logic for a lecturer grading an assignment
#         return jsonify(message="Grade submitted successfully"), 201
#     except Exception as e:
#         return jsonify(error="Failed to submit grade"), 500


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error="Resource not found"), 404

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify(error="Internal server error"), 500
    

if __name__ == '__main__':
    app.run(port=8080, debug=True)