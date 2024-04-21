'use client'
import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

import {
  Box, Container, Flex, Grid, Heading, Text, VStack, Table, Thead, Tbody, Tr, Th, Td, List, ListItem, ListIcon, useColorModeValue, Badge, Button,
} from '@chakra-ui/react';
import { CalendarIcon } from '@chakra-ui/icons';

import { getUserData } from '@/services/auth';
import { getStudentCourses } from '@/services/course';
import { getStudentAssignments } from '@/services/assignment';
import { getUserCalendarEvents } from '@/services/calendar';

const Dashboard = () => {
  const [courses, setCourses] = useState([]);
  const [assignments, setAssignments] = useState([]);
  const [calendarEvents, setCalendarEvents] = useState([]);
  const [userData, setUserData] = useState(null);

  const router = useRouter();

  useEffect(() => {
    const fetchUserDataAndContent = async () => {
      try {
        const userData = await getUserData();
        console.log('User data found:', userData);
        setUserData(userData);

        const coursesData = await getStudentCourses(userData.userId);
        setCourses(coursesData);

        const assignmentsData = await getStudentAssignments(userData.userId);
        setAssignments(assignmentsData.courses);

        const calendarEventsData = await getUserCalendarEvents(userData.userId);
        setCalendarEvents(calendarEventsData.calendarEvents);

      } catch (error) {
        console.error('Error fetching data:', error);
        // Handle error, e.g., show an error message or redirect to an error page
      }
    };

    fetchUserDataAndContent();
  }, [router]);

  return (
    <Container maxW={'5xl'} mt={5} mb={5}>
      <VStack spacing={8} align="stretch" p={5}>
        <Flex justifyContent="space-between" alignItems="center" direction={'column'}>
          <Heading mb={4}>Welcome, {userData?.name}</Heading>
          <Badge colorScheme="accent" variant="subtle">{userData?.accType}</Badge>
        </Flex>
        
        <Box>
          <Heading size="md" mb={4}>Your Courses</Heading>
          <Grid templateColumns={{sm: 'repeat(1, 1fr)', md: 'repeat(2, 1fr)', lg: 'repeat(3, 1fr)'}} gap={6}>
            {courses.map((course) => (
              <Box 
                key={course.CourseId} 
                p={5} 
                shadow="md" 
                borderWidth="1px" 
                borderRadius="lg" 
                bg={"primary.50"} 
                onClick={
                  () => router.push(`/course/${course.CourseId}`)
                } 
                _hover={{ bg: "primary.100", shadow: "lg" }} 
                transition="background 0.3s, box-shadow 0.3s"
                cursor="pointer"
              >
                <Heading fontSize="xl">{course.CourseName}</Heading>
                <Text mt={4}>{course.Period}</Text>
              </Box>
            ))}
          </Grid>
        </Box>

        <Box>
          <Heading size="md" mb={4}>Your Assignments</Heading>
          <Table variant="simple">
            <Thead>
              <Tr>
                <Th>Course</Th>
                <Th>Title</Th>
                <Th isNumeric>Due Date</Th>
              </Tr>
            </Thead>
            <Tbody>
              {assignments.flatMap(course => 
                course.Assignments.map(assignment => (
                  <Tr 
                    key={assignment.AssignmentId} 
                    onClick={() => router.push(`/assignment/${assignment.AssignmentId}`)} 
                    cursor="pointer"
                    _hover={{ bg: "primary.50" }}
                    transition="background 0.3s"
                  >
                    <Td>{course.CourseName}</Td>
                    <Td>{assignment.AssignmentTitle}</Td>
                    <Td isNumeric>{assignment.DueDate}</Td>
                  </Tr>
                ))
              )}
            </Tbody>
          </Table>
        </Box>

        <Box>
          <Heading size="md" mb={4}>Your Calendar Events</Heading>
          <List spacing={3}>
            {calendarEvents.map(event => (
              <ListItem 
                key={event.EventId} 
                p={2} 
                borderRadius="md" 
                _hover={{ bg: "primary.50" }} 
                transition="background 0.3s"
                onClick={() => router.push(`/calendar_event/${event.EventId}`)} 
                cursor="pointer"
              >
                <Flex alignItems="center">
                  <ListIcon as={CalendarIcon} color="accent.500" />
                  <Text flex="1">{event.EventTitle}</Text>
                  <Badge ml="4" colorScheme="accent">{event.StartDate}</Badge>
                </Flex>
              </ListItem>
            ))}
          </List>
        </Box>
      </VStack>
    </Container>
  );
};

export default Dashboard;
