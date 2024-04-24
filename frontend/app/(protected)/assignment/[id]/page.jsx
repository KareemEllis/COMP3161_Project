'use client'
import { useEffect, useState } from 'react';
import {
  Box, Container, Heading, Text, Table, Thead, Tbody, Tr, Th, Td,
  useColorModeValue, VStack
} from '@chakra-ui/react';

import { getAssignmentById } from '@/services/assignment';
import { getUserAssignmentSubmission } from '@/services/assignment';
import { getAssignmentSubmissions } from '@/services/assignment';
import { getUserData } from '@/services/auth';

const AssignmentDetailsPage = ({ params }) => {
  const [userData, setUserData] = useState(null);
  const [assignment, setAssignment] = useState(null);
  const [userSubmission, setUserSubmission] = useState(null);
  const [submissions, setSubmissions] = useState([]);
  const assignment_id = params.id;

  useEffect(() => {
    const fetchData = async () => {
      try {
        const userData = await getUserData();
        setUserData(userData);
        const userId = userData.userId;

        if (assignment_id && userId) {
          const fetchedAssignment = await getAssignmentById(assignment_id);
          setAssignment(fetchedAssignment);

          const fetchedSubmissions = await getAssignmentSubmissions(assignment_id);
          setSubmissions(fetchedSubmissions);

          const fetchedSubmission = await getUserAssignmentSubmission(assignment_id, userId);
          setUserSubmission(fetchedSubmission);
        }
      } catch (error) {
        console.error('Failed to fetch data:', error);
      }
    };

    fetchData();
  }, [assignment_id]);

  return (
    <Container maxW="lg" centerContent>
      <Box p={5} w="full" my={5}>
        <VStack spacing={4} align="start">
          {assignment ? (
            <>
              <Heading>{assignment.AssignmentTitle}</Heading>
              <Text>Due Date: {assignment.DueDate}</Text>
              <Text>Course ID: {assignment.CourseId}</Text>
            </>
          ) : (
            <Text>Loading assignment details...</Text>
          )}

          {userSubmission ? (
            <>
              <Heading size="md" mt={5}>Your Submission</Heading>
              <Table variant="simple">
                <Thead>
                  <Tr>
                    <Th>Name</Th>
                    <Th>Username</Th>
                    <Th isNumeric>Grade</Th>
                    <Th>Submission Date</Th>
                  </Tr>
                </Thead>
                <Tbody>
                  <Tr>
                    <Td>{userSubmission.Name}</Td>
                    <Td>{userSubmission.Username}</Td>
                    <Td isNumeric>{userSubmission.Grade}</Td>
                    <Td>{userSubmission.SubmissionDate}</Td>
                  </Tr>
                </Tbody>
              </Table>
            </>
          ) : (
            <Text>No submission found.</Text>
          )}

          {userData && userData.accType !== 'Student' &&
            <>
            <Heading size="md" mt={5}>Submissions</Heading>
            <Table variant="simple">
              <Thead>
                <Tr>
                  <Th>Name</Th>
                  <Th>Username</Th>
                  <Th isNumeric>Grade</Th>
                  <Th>Submission Date</Th>
                </Tr>
              </Thead>
              <Tbody>
                {submissions.map(submission => (
                  <Tr key={submission.SubmissionId}>
                    <Td>{submission.Name}</Td>
                    <Td>{submission.Username}</Td>
                    <Td isNumeric>{submission.Grade}</Td>
                    <Td>{submission.SubmissionDate}</Td>
                  </Tr>
                ))}
              </Tbody>
            </Table>
            </>
          }
        </VStack>
      </Box>
    </Container>
  );
};

export default AssignmentDetailsPage;
