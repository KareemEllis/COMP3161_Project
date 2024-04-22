'use client'
import React from 'react'
import { useRouter } from 'next/navigation';
import {
    Box, Heading, Text
} from '@chakra-ui/react';

export default function CourseCard({ course }) {
    const router = useRouter();

    return (
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
            <Text fontWeight={'bold'} color={'primary.800'}>{course.CourseId}</Text>
            <Heading fontSize="xl">{course.CourseName}</Heading>
            <Text mt={4}>{course.Period}</Text>
        </Box>
    )
}
