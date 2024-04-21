'use client'
import React from 'react';
import { Container, Flex, Box, Text, Button, Link as ChakraLink, useToast } from '@chakra-ui/react';
import NextLink from 'next/link';
import { useRouter } from 'next/navigation';
import { logoutUser } from '@/services/auth';

const Navbar = () => {
  const router = useRouter();
  const toast = useToast();

  const handleLogout = async () => {
    try {
      await logoutUser();
      toast({
        title: "Logout successful.",
        description: "You have been successfully logged out.",
        status: "success",
        duration: 5000,
        isClosable: true,
      });
      router.push('/login');
    } catch (error) {
      toast({
        title: "Logout failed.",
        description: "An error occurred during logout. Please try again.",
        status: "error",
        duration: 5000,
        isClosable: true,
      });
    }
  };

  return (
    <Box bg={'primary.500'}>
    <Container maxW={'5xl'} p={4} >
    
    <Flex  color={'white'} justifyContent="space-between" alignItems="center" >
      <Box>
        <Text fontSize="xl" fontWeight="bold">OurVLE</Text>
      </Box>
      <Box>
        <NextLink href="/dashboard" passHref>
          <ChakraLink px={2}>Dashboard</ChakraLink>
        </NextLink>
        <NextLink href="/my-profile" passHref>
          <ChakraLink px={2}>My Profile</ChakraLink>
        </NextLink>
        <NextLink href="/courses" passHref>
          <ChakraLink px={2}>Courses</ChakraLink>
        </NextLink>
        <Button colorScheme="accent" ml={4} onClick={handleLogout}>Logout</Button>
      </Box>
    </Flex>
    
    </Container>
    </Box>
  );
};

export default Navbar;
