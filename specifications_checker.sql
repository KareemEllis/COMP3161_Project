
-- Total number of students

SELECT COUNT(*) AS num_students
FROM ourvle.account
JOIN ourvle.user ON user.UserId = account.UserId
WHERE account.AccType = 'Student';


-- Total number of Courses

SELECT COUNT(*) AS num_courses
FROM ourvle.course;


-- Check number of members for each course

SELECT CourseId, COUNT(*) AS num_members
FROM ourvle.membership
GROUP BY CourseId;


-- Check if All Students have courses with a maximum of 6 courses

SELECT m.UserId, a.AccType, COUNT(m.CourseId) AS num_courses
FROM ourvle.membership AS m
JOIN ourvle.user AS u ON m.UserId = u.UserId
JOIN ourvle.account AS a ON u.UserId = a.UserId
WHERE a.AccType = 'Student'
GROUP BY m.UserId
ORDER BY num_courses DESC;


-- Check if All Students have courses minimum 3 courses

SELECT m.UserId, a.AccType, COUNT(m.CourseId) AS num_courses
FROM ourvle.membership AS m
JOIN ourvle.user AS u ON m.UserId = u.UserId
JOIN ourvle.account AS a ON u.UserId = a.UserId
WHERE a.AccType = 'Student'
GROUP BY m.UserId
ORDER BY num_courses;


-- Check if All Lecturers/Course Maintainers teach courses at least 1 course

SELECT m.UserId, a.AccType, COUNT(m.CourseId) AS num_courses
FROM ourvle.membership AS m
JOIN ourvle.user AS u ON m.UserId = u.UserId
JOIN ourvle.account AS a ON u.UserId = a.UserId
WHERE a.AccType = 'Course Maintainer'
GROUP BY m.UserId
ORDER BY num_courses;



-- Check if All Lecturers/Course Maintainers teach courses max 5 courses

SELECT m.UserId, a.AccType, COUNT(m.CourseId) AS num_courses
FROM ourvle.membership AS m
JOIN ourvle.user AS u ON m.UserId = u.UserId
JOIN ourvle.account AS a ON u.UserId = a.UserId
WHERE a.AccType = 'Course Maintainer'
GROUP BY m.UserId
ORDER BY num_courses DESC;


