from random import randint
import random
from faker import Faker
from textwrap import dedent

fake = Faker()
file = open("insert_queries.sql", 'w')

student_ids = []
admin_ids = []
course_maintenance_ids = []
member_ids = []
membership_data = []

lecturers_ids = []

courses_ids = []
course_codes = []
course_names = []

section_ids = []
topic_ids = []

user_ids = []
account_ids = []
account_dict = {}
user_dict = {}
usernames = []
passwords = []

# num_users = 100000
num_users = 1000
num_courses = 20
min_num_members = 10

def generateUsers():
    file.write(dedent("""
    INSERT INTO User
                    VALUES"""))

    for i in range(num_users):
        
        username = fake.user_name()
        password = fake.password(length=10)
        
        user_id = randint(100, 9999999)

        while user_id in user_ids:
            user_id = randint(100, 9999999)
        
        # Check if username is unique
        while username in usernames:
            username = fake.user_name()
        
        # Check if password is unique
        while password in passwords:
            password = fake.password(length=20)
        
        # Add username and password to the lists
        usernames.append(username)
        passwords.append(password)
        
        first_name = fake.first_name()
        last_name = fake.last_name()
        
        full_name = first_name + ' ' + last_name
        
        user_dict[user_id] = (first_name, last_name)
        user_ids.append(user_id)
        
        if (i == num_users-1):
            file.write(f"""
                    ('{user_id}', '{username}', '{password}', '{full_name}');\n
                """)
        else:
            file.write(f"""
                    ('{user_id}', '{username}', '{password}', '{full_name}'),
                """)

def generateAccounts():
    account_types = ['Course Maintainer', 'Student', 'Admin']
    
    file.write(dedent("""
    INSERT INTO Account
                    VALUES"""))
    
    for i, user_id in enumerate(user_dict.keys()):
        account_id = randint(100, 9999999)
        
        while account_id in account_ids:  # Check if account_id is unique
            account_id = randint(100, 9999999)
        
        account_ids.append(account_id)  # Add account_id to the list
        
        # account_type = random.choice(account_types)
        account_type = random.choices(account_types, weights=[1, 3, 1])[0]
        
        account_dict[account_id] = (account_type, user_id)
        
        if (i == len(user_dict.keys())-1):
            file.write(f"""
                   ('{account_id}', '{user_id}', '{account_type}');\n
                """)
        else:
            file.write(f"""
                   ('{account_id}', '{user_id}', '{account_type}'),""")
    
    # print(account_dict)
    


def generateStudents():

    file.write(dedent("""
    INSERT INTO Student
                    VALUES"""))
    
    # get the acc types
    for i, item in enumerate(account_dict.items()):
        
        if item[1][0] == 'Student':
            account_id = item[0]
            user_id = item[1][1]
        
            if (i == len(user_dict.keys())-1):
                file.write(f"""
                        ('{account_id}', '{item[1][0]}');\n
                    """);
            else:
                file.write(f"""
                        ('{account_id}', '{item[1][0]}'),""");
                
            student_ids.append(account_id)
        
    print(len(student_ids))
    

def generateAdmins():

    file.write(dedent("""
    INSERT INTO Admin
                    VALUES"""))
    
    # get the acc types
    for i, item in enumerate(account_dict.items()):
        
        if item[1][0] == 'Admin':
            account_id = item[0]
            user_id = item[1][1]
        
            if (i == len(user_dict.keys())-1):
                file.write(f"""
                        ('{account_id}', '{item[1][0]}');\n
                    """);
            else:
                file.write(f"""
                        ('{account_id}', '{item[1][0]}'),""");
                
            admin_ids.append(account_id)
        
    print(len(admin_ids))


def generateCourseMaintainers():

    file.write(dedent("""
    INSERT INTO CourseMaintainer
                    VALUES"""))
    
    # get the acc types
    for i, item in enumerate(account_dict.items()):
        
        if item[1][0] == 'Course Maintainer':
            account_id = item[0]
            user_id = item[1][1]
        
            if (i == len(user_dict.keys())-1):
                file.write(f"""
                        ('{account_id}', '{item[1][0]}');\n
                    """);
            else:
                file.write(f"""
                        ('{account_id}', '{item[1][0]}'),""");
                
            course_maintenance_ids.append(account_id)
        
    print(len(course_maintenance_ids))


# Need to add Period
def generateCourses():

    course_lists = ['Mathematics', 'Ecology', 'Computer Science', 'Biology', 'Chemistry',
               'Physics', 'Literature', 'History', 'Psychology', 'Sociology',
               'Anthropology', 'Economics', 'Political Science', 'Philosophy',
               'Art History', 'Geography', 'Environmental Science', 'Statistics',
               'Cultural Studies', 'Engineering', 'Medicine', 'Law', 'Business Administration',
               'Marketing', 'Finance', 'Accounting', 'Digital Media', 'Graphic Design',
               'Film Studies', 'Music Theory', 'Creative Writing', 'Journalism',
               'Public Relations', 'Health Sciences', 'Nutrition', 'Foreign Languages',
               'Education', 'Astronomy', 'Religious Studies', 'Archaeology', 'Oceanography',
               'Political Economy', 'Industrial Design', 'Human Resource Management',
               'Data Science', 'Robotics', 'Game Development', 'Cybersecurity', 'Ethics', 'Social Work']

    
    prefix_list = ['Introduction to', 'Advanced', 'Beginner', 'Intermediate']
    prefix_list = ['Introduction to', 'Advanced', 'Intermediate', 'Fundamentals of', 'Principles of']
    suffix_list = ['I', 'II', 'III']
    
    periods = ['Fall', 'Spring', 'Summer']
    
    file.write(dedent("""
    INSERT INTO Course
                    VALUES"""))
    
    for i in range(num_courses):
        
        # Course IDs should be unique
        
        # Course IDs
        
        course_id = randint(100, 9999999)
        
        if course_id not in courses_ids:
            courses_ids.append(str(course_id))
        else:
            while course_id in courses_ids:
                course_id = randint(100, 9999999)
            courses_ids.append(str(course_id))
            
        # Generate random course names and codes and periods
        
        course = random.choice(course_lists)
        course_code = str(course[:3].upper()) + str(randint(100,999))
        
        period = random.choices(periods, weights=[2, 2, 1])[0]
        
        course_name = random.choice(prefix_list) + ' '  + course + ' ' + random.choice(suffix_list)
        
        # Course names and codes should be unique
        # If they are not unique, generate new ones
        # until they are unique
        
        # Course Names
        
        if course_name not in course_names:
            course_names.append(course_name)
        else:
            while course_name in course_names:
                course_name = random.choice(prefix_list) + ' '  + course + ' ' + random.choice(suffix_list)
            course_names.append(course_name)
        
        # Course Codes
        
        if course_code not in course_codes:
            course_codes.append(course_code)
        else:
            while course_code in course_codes:
                course_code = str(course[:3].upper()) + str(randint(100,999))
            course_codes.append(course_code)
        
        
        if (i == num_courses-1):
            file.write(f"""
                       ('{course_id}', '{course_name}'. '{course_code}', '{period}'); \n
                       """)
                    
        else:
           file.write(f"""
                       ('{course_id}', '{course_name}', '{course_code}', '{period}',)
                       """);
           

def generateMembership():
    
    
    file.write(dedent("""
    INSERT INTO Membership
                    VALUES"""))
    
    
    membership_data = []
    unassigned_accounts = []
    assigned_accounts = []
    
    course_counts = {course_id: 0 for course_id in courses_ids}
    course_maintainer_counts = {account_id: 0 for account_id, (account_type, user_id) in account_dict.items() if account_type == 'Course Maintainer'}
    student_counts = {account_id: 0 for account_id, (account_type, user_id) in account_dict.items() if account_type == 'Student'}
    admin_counts = {account_id: 0 for account_id, (account_type, user_id) in account_dict.items() if account_type == 'Admin'}
    
    account_course_assignments = {account_id: 0 for account_id in account_ids}  # Track course assignments for each account
    


    # Loop through courses to generate initial memberships
    for i, course_id in enumerate(courses_ids):
        num_members = random.randint(min_num_members, len(account_ids))
        selected_accs = random.sample(account_ids, min(num_members, len(account_ids)))

        # Assign members to courses
        for account_id in selected_accs:
            # Check if account is a student or a course maintainer
            if account_dict[account_id][0] == 'Student':
                if student_counts[account_id] >= 6:
                    continue
                student_counts[account_id] += 1
                
            elif account_dict[account_id][0] == 'Course Maintainer':
                if course_maintainer_counts[account_id] >= 5:
                    continue
                course_maintainer_counts[account_id] += 1
                
            elif account_dict[account_id][0] == 'Admin':
                if admin_counts[account_id] >= 3:
                    continue
                admin_counts[account_id] += 1

            # Check if course has reached maximum members
            if course_counts[course_id] >= 10:
                continue

            # Generate member ID
            member_id = randint(100, 9999999)
            while member_id in member_ids:
                member_id = randint(100, 9999999) 
            member_ids.append(member_id)

            # Append membership data
            membership_data.append({'member_id': member_id, 'course_id': course_id, 'account_id': account_id, 'account_type': account_dict[account_id][0]})
            course_counts[course_id] += 1
            
            # Write to file
            if (i == len(courses_ids) - 1) and (account_id == selected_accs[-1]):
                file.write(f"""('{member_id}', '{account_dict[account_id][1]}', '{course_id}', '{account_dict[account_id][0]}');\n""")
            else:
                file.write(f"""('{member_id}', '{account_dict[account_id][1]}', '{course_id}', '{account_dict[account_id][0]}'),\n""")
            
            # Track course assignment count for the account
            account_course_assignments[account_id] += 1
            

    # Check and add accounts with less than 3 assignments to unassigned_accounts
    for account_id, assignment_count in account_course_assignments.items():
        if assignment_count < 3:
            unassigned_accounts.append(account_id)
        else:
            assigned_accounts.append(account_id)
            
    # print('Assigned accounts and Number:', assigned_accounts, len(assigned_accounts))
    # print('Unassigned accounts and Number:', unassigned_accounts, len(unassigned_accounts))
    
    assignRemainingAccounts(unassigned_accounts, courses_ids, account_dict, member_ids, account_course_assignments)

            

def assignRemainingAccounts(unassigned_accounts, courses_ids, account_dict, member_ids, account_course_assignments):
    
    
    # Track the counts for each account ID
    # Get previous course assignments counts for unassigned accounts
    account_counts = {account_id: account_course_assignments[account_id] for account_id in unassigned_accounts}
    
    print('Previous course assignments: \n', account_counts)

    # Assign courses to unassigned account IDs until all accounts are assigned
    for account_id in unassigned_accounts:
        
        num_courses = 0
        
        # Number of courses for Students and Course Maintainers 
        if account_dict[account_id][0] == 'Student':
            num_courses = random.randint(3, 6)
        elif account_dict[account_id][0] == 'Course Maintainer':
            num_courses = random.randint(1, 5)
        else: # Admins
            num_courses = random.randint(1, 3)
        
        while account_counts[account_id] < num_courses:
        
            # Choose a random course
            course_id = random.choice(courses_ids)
            
            
            # Generate a random member ID
            member_id = random.randint(100, 9999999)
            while member_id in member_ids:
                member_id = random.randint(100, 9999999)
            member_ids.append(member_id)
            
            # Check if exact data is already in membership_data
            data = {'member_id': member_id, 'course_id': course_id, 'account_id': account_id, 'account_type': account_dict[account_id][0]}
            if data in membership_data:
                continue
            membership_data.append(data)
            
            # Write the assigned membership information to the file
            file.write(f"('{member_id}', '{account_dict[account_id][1]}', '{course_id}', '{account_dict[account_id][0]}'),\n")
            
            # Increment the course count for the account
            account_counts[account_id] += 1
            
            
            
    print('Newly assigned accounts:', account_counts)
    
    

def generateSections():
    # [SectionId,SectionTitle,CourseId]
    
    # example data:
    # 2, Section 2, 1
    
    file.write(dedent("""
    INSERT INTO Section
                    VALUES"""))
    
    for index , course_id in enumerate(courses_ids):
        
        num_sections = random.randint(1, 10)
        
        for i in range(num_sections):
            
            section_id = randint(100, 9999999)
            section_title = f'Section {i+1}'
            
            while section_id in section_ids:
                section_id = randint(100, 9999999)
            section_ids.append(section_id)
            
            
            if (index == num_courses-1) and (i == num_sections-1):
                file.write(f"""
                        ('{section_id}', '{section_title}'. '{course_id}'); \n
                        """)
                        
            else:
                file.write(f"""
                            ('{section_id}', '{section_title}'. '{course_id}'),
                            """);
                
def generateTopics():
    
    # [TopicId,TopicTitle,SectionId]
    # example data:
    # [2, Topic 1, 7]
    
    file.write(dedent("""
    INSERT INTO Topic
                    VALUES"""))
    
    for section_id in section_ids:
        
        num_topics = random.randint(1, 10)
        
        for i in range(num_topics):
            
            topic_id = randint(100, 9999999)
            
            while topic_id in topic_ids:
                topic_id = randint(100, 9999999)
            topic_ids.append(topic_id)
            
            topic_title = f'Topic {i+1}'
            
            if (section_id == section_ids[-1]) and (i == num_topics-1):
                file.write(f"""
                        ('{topic_id}', '{topic_title}', '{section_id}'); \n
                        """)
            else:
                file.write(f"""
                        ('{topic_id}', '{topic_title}', '{section_id}'),
                        """)
    
def generateSectionItems():
    
    # [ItemId,SectionContent,SectionId]
    
    # example data:
    # [2, 'Lorem Ipsum', 7]
    
    file.write(dedent("""
    INSERT INTO SectionItem
                    VALUES"""))
    
    
    for section_id in section_ids:
        
        num_items = random.randint(1, 10)
        
        for i in range(num_items):
            
            item_id = randint(100, 9999999)
            
            while item_id in topic_ids:
                item_id = randint(100, 9999999)
            
            section_content = fake.text()
            
            if (section_id == section_ids[-1]) and (i == num_items-1):
                file.write(f"""
                        ('{item_id}', '{section_content}', '{section_id}'); \n
                        """)
            else:
                file.write(f"""
                        ('{item_id}', '{section_content}', '{section_id}'),
                        """)
    


# Run the functions

generateUsers()
generateAccounts()


generateStudents()
generateAdmins()
generateCourseMaintainers()

generateCourses()
generateSections()
generateTopics()

generateSectionItems()

generateMembership()

file.close()


