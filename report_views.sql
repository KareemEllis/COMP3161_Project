-- All courses that have 50 or more students

CREATE VIEW Course_Student_Count AS
SELECT Course.CourseId, Course.CourseName, COUNT(Membership.UserId) AS StudentCount
FROM Course
JOIN Membership ON Course.CourseId = Membership.CourseId
GROUP BY Course.CourseId, Course.CourseName
HAVING COUNT(Membership.UserId) >= 50;


-- All students that do 5 or more courses


CREATE VIEW Student_Course_Count AS
SELECT User.UserId, User.Username, User.Name, COUNT(Membership.CourseId) AS CourseCount
FROM User
JOIN Account ON User.UserId = Account.UserId
JOIN Membership ON User.UserId = Membership.UserId
WHERE Account.AccType = 'Student'
GROUP BY User.UserId, User.Username, User.Name
HAVING COUNT(Membership.CourseId) >= 5;


-- All course maintainers that teach 3 or more courses

CREATE VIEW Course_Maintainer_Course_Count AS
SELECT User.UserId, User.Username, User.Name, Account.AccType, COUNT(Membership.CourseId) AS CourseCount
FROM User
JOIN Account ON User.UserId = Account.UserId
JOIN Membership ON User.UserId = Membership.UserId
WHERE Account.AccType = 'Course Maintainer'
GROUP BY User.UserId, User.Username, User.Name
HAVING COUNT(Membership.CourseId) >= 3;


-- The 10 most enrolled courses

CREATE VIEW Top_Enrolled_Courses AS
SELECT Course.CourseId, Course.CourseName, COUNT(Membership.UserId) AS EnrollmentCount
FROM Course
JOIN Membership ON Course.CourseId = Membership.CourseId
GROUP BY Course.CourseId, Course.CourseName
ORDER BY EnrollmentCount DESC
LIMIT 10;


-- The top 10 students with the highest overall averages.

CREATE VIEW Top_Users_Average_Grade AS
SELECT User.UserId, User.Username, User.Name, AVG(AssignmentSubmission.Grade) AS AverageGrade
FROM User
JOIN AssignmentSubmission ON User.UserId = AssignmentSubmission.UserId
WHERE AssignmentSubmission.Grade IS NOT NULL
GROUP BY User.UserId, User.Username, User.Name
ORDER BY AverageGrade DESC
LIMIT 10;
