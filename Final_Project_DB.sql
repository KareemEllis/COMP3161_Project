CREATE DATABASE OURVLE;

USE OURVLE;

CREATE TABLE User (
    UserId INT PRIMARY KEY,
    Username VARCHAR(255) NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Name VARCHAR(255) NOT NULL
);

CREATE TABLE Account (
    AccountId INT PRIMARY KEY AUTO_INCREMENT,
    UserId INT,
    AccType VARCHAR(50),
    FOREIGN KEY (UserId) REFERENCES User(UserId)
);

CREATE TABLE Course (
    CourseId INT PRIMARY KEY,
    CourseName VARCHAR(255) NOT NULL,
    Period VARCHAR(50)
);

CREATE TABLE Section (
    SectionId INT PRIMARY KEY AUTO_INCREMENT,
    SectionTitle VARCHAR(255) NOT NULL,
    CourseId INT,
    FOREIGN KEY (CourseId) REFERENCES Course(CourseId)
);

CREATE TABLE Topic (
    TopicId INT PRIMARY KEY AUTO_INCREMENT,
    TopicTitle VARCHAR(255) NOT NULL,
    SectionId INT,
    FOREIGN KEY (SectionId) REFERENCES Section(SectionId)
);

CREATE TABLE Assignment (
    AssignmentId INT PRIMARY KEY AUTO_INCREMENT,
    AssignmentTitle VARCHAR(255) NOT NULL,
    CourseId INT,
    DueDate DATE,
    FOREIGN KEY (CourseId) REFERENCES Course(CourseId)
);

CREATE TABLE AssignmentSubmission (
    SubmissionId INT PRIMARY KEY AUTO_INCREMENT,
    AssignmentId INT,
    UserId INT,
    SubmissionDate DATE,
    Grade DECIMAL(5,2),
    FOREIGN KEY (AssignmentId) REFERENCES Assignment(AssignmentId),
    FOREIGN KEY (UserId) REFERENCES User(UserId)
);

CREATE TABLE DiscussionForum (
    ForumId INT PRIMARY KEY AUTO_INCREMENT,
    ForumTitle VARCHAR(255) NOT NULL,
    CourseId INT,
    FOREIGN KEY (CourseId) REFERENCES Course(CourseId)
);

CREATE TABLE DiscussionThread (
    ThreadId INT PRIMARY KEY AUTO_INCREMENT,
    ForumId INT,
    ThreadTitle VARCHAR(255) NOT NULL,
    ThreadContent TEXT,
    UserId INT,
    ParentThreadId INT,
    FOREIGN KEY (ForumId) REFERENCES DiscussionForum(ForumId),
    FOREIGN KEY (UserId) REFERENCES User(UserId)
);

CREATE TABLE CalendarEvent (
    EventId INT PRIMARY KEY AUTO_INCREMENT,
    CourseId INT,
    StartDate DATE,
    EndDate DATE,
    EventTitle VARCHAR(255) NOT NULL,
    Description TEXT,
    FOREIGN KEY (CourseId) REFERENCES Course(CourseId)
);

CREATE TABLE SectionItem (
    ItemId INT PRIMARY KEY AUTO_INCREMENT,
    SectionContent TEXT,
    SectionId INT,
    FOREIGN KEY (SectionId) REFERENCES Section(SectionId)
);

CREATE TABLE Membership (
    MemberId INT PRIMARY KEY AUTO_INCREMENT,
    UserId INT,
    CourseId INT,
    FOREIGN KEY (UserId) REFERENCES User(UserId),
    FOREIGN KEY (CourseId) REFERENCES Course(CourseId)
);
