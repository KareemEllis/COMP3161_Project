'use client'
import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import {
  Container, Box, Button, FormControl, FormLabel, Input, useToast, Heading,
  VStack, useColorModeValue
} from '@chakra-ui/react';

import { createCourse } from '@/services/course';
import { getUserData } from '@/services/auth';


const CreateCoursePage = () => {
  const [courseData, setCourseData] = useState({
    courseId: '',
    courseName: '',
    period: '',
  });
  const [userData, setUserData] = useState({});
  const router = useRouter();
  const toast = useToast();

  // Check if the user is an admin
  useEffect(() => {
    const fetchUserData = async () => {
      const userData = await getUserData();
      setUserData(userData);

      if (userData.accType !== 'Admin') {
        router.push('/dashboard');
      }
    };

    fetchUserData();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setCourseData(prevState => ({ ...prevState, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const userId = userData.userId; // Get this from the actual user session or context
    try {
      await createCourse(userId, courseData.courseId, courseData.courseName, courseData.period);
      toast({
        title: 'Course created successfully',
        status: 'success',
        duration: 5000,
        isClosable: true,
      });
      router.push('/course');
    } catch (error) {
      toast({
        title: 'Failed',
        description: error.message,
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
  };

  return (
    <Container maxW={'5xl'} mt={5} mb={5}>
    <Box p={5}>
      <Heading mb={4}>Create a New Course</Heading>
      <form onSubmit={handleSubmit}>
        <VStack spacing={4}>
          <FormControl isRequired>
            <FormLabel>Course ID</FormLabel>
            <Input name="courseId" value={courseData.courseId} onChange={handleChange} />
          </FormControl>
          <FormControl isRequired>
            <FormLabel>Course Name</FormLabel>
            <Input name="courseName" value={courseData.courseName} onChange={handleChange} />
          </FormControl>
          <FormControl isRequired>
            <FormLabel>Period</FormLabel>
            <Input name="period" value={courseData.period} onChange={handleChange} />
          </FormControl>
          <Button colorScheme="primary" type="submit">Create Course</Button>
        </VStack>
      </form>
    </Box>
    </Container>
  );
};

export default CreateCoursePage;
