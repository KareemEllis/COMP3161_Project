'use client'
import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

import {
  Box, Container, Flex, Grid, Heading, VStack, Button, Link as ChakraLink
} from '@chakra-ui/react';

import { getUserData } from '@/services/auth';
import { getStudentCourses } from '@/services/course';
import { getMaintainerCourses } from '@/services/course';
import { getAllCourses } from '@/services/course';

import CourseCard from '@/app/components/CourseCard';

const Dashboard = () => {
    const [allCourses, setAllCourses] = useState([]);
    const [courses, setCourses] = useState([]);
    const [userData, setUserData] = useState(null);

    useEffect(() => {
        const fetchUserDataAndContent = async () => {
        try {
            const userData = await getUserData();
            console.log('User data found:', userData);
            setUserData(userData);

            const allCoursesData = await getAllCourses();
            setAllCourses(allCoursesData);

            if (userData.accType == 'Course Maintainer') {
                const maintainerCoursesData = await getMaintainerCourses(userData.userId);
                setCourses(maintainerCoursesData);
            }
            else if (userData.accType == 'Student'){
                const coursesData = await getStudentCourses(userData.userId);
                setCourses(coursesData);
            }
            const coursesData = await getStudentCourses(userData.userId);
            setCourses(coursesData);


        } catch (error) {
            console.error('Error fetching data:', error);
        }
        };

        fetchUserDataAndContent();
    }, []);

    return (
        <Container maxW={'5xl'} mt={5} mb={5}>
        <VStack spacing={8} align="stretch" p={5}>
            <Flex justifyContent="space-between" wrap={'wrap'}>
                <Heading mb={4} mr={4}>Courses</Heading>
                {userData && userData.accType == 'Admin' && (
                <Button 
                    as={ChakraLink} 
                    href='/course/create' 
                    colorScheme="primary" 
                    variant="solid"
                >
                    Create Course
                </Button>
                )}
                
            </Flex>

            {userData && userData.accType != 'Admin' && (
                <Box>
                <Heading size="md" mb={4}>My Courses</Heading>
                <Grid templateColumns={{sm: 'repeat(1, 1fr)', md: 'repeat(2, 1fr)', lg: 'repeat(3, 1fr)'}} gap={6}>
                    {courses.map((course) => (
                        <CourseCard course={course} />
                    ))}
                </Grid>
                </Box>
            )}

            <Box>
            <Heading size="md" mb={4}>All Courses</Heading>
            <Grid templateColumns={{sm: 'repeat(1, 1fr)', md: 'repeat(2, 1fr)', lg: 'repeat(3, 1fr)'}} gap={6}>
                {allCourses.map((course) => (
                    <CourseCard course={course} />
                ))}
            </Grid>
            </Box>

        </VStack>
        </Container>
    );
};

export default Dashboard;
