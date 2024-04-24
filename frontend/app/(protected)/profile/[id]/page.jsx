'use client'
import { useEffect, useState } from 'react';

import {
  Box, Text, VStack, Heading, Tag, Container, useColorModeValue
} from '@chakra-ui/react';
import { getUserById } from '@/services/auth';

const UserProfilePage = ({ params }) => {
  const [user, setUser] = useState(null);

  const id = params.id;

  const bg = useColorModeValue('gray.50', 'gray.700');
  const primaryColor = useColorModeValue('primary.500', 'primary.300');
  const accentColor = useColorModeValue('accent.400', 'accent.200');

  useEffect(() => {
    if (id) { // Ensure id is not null or undefined
      getUserById(id)
        .then(setUser)
        .catch(error => {
        console.error('Failed to fetch user data:', error);
      });
    }
  }, [id]);

  if (!user) {
    return <Text>Loading user profile...</Text>; // Loading state
  }

  return (
    <Container maxW="lg" centerContent>
      <Box p={5} w="full">
        <VStack spacing={4} align="center">
          <Heading color={primaryColor}>User Profile</Heading>
          <Text fontSize="xl" fontWeight="bold">{user.Name}</Text>
          <Text>Username: {user.Username}</Text>
          <Tag size="md" colorScheme={user.AccType === 'Student' ? 'blue' : 'teal'}>{user.AccType}</Tag>
        </VStack>
      </Box>
    </Container>
  );
};

export default UserProfilePage;
