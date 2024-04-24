'use client'
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import {
  Box, Button, Flex, FormControl, FormLabel, Input, useToast, VStack,
} from '@chakra-ui/react';
import { loginUser } from '@/services/auth';

export default function Login() {
  const [userId, setUserId] = useState('');
  const [password, setPassword] = useState('');
  const toast = useToast();
  const router = useRouter();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await loginUser(userId, password);
      toast({
        title: response.message,
        status: 'success',
        duration: 5000,
        isClosable: true,
      });

      // Check user's account type and redirect accordingly
      const accType = response.user.accType;
      if (accType === 'Student' || accType === 'Course Maintainer') {
        router.push('/dashboard');
      } else if (accType === 'Admin') {
        router.push('/admin/dashboard');
      }
    } catch (error) {
      toast({
        title: 'Login failed.',
        description: error.message.toString(),
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
  };

  return (
    <Flex minHeight="100vh" width="full" align="center" justifyContent="center" direction="column" bg="primary.50">
        <Box borderWidth="1px" px={4} width="full" maxWidth="500px" borderRadius="lg" textAlign="center" boxShadow="lg" bg="white">
          <Box p={4}>
            <Box textAlign="center">
              <Box>Login</Box>
            </Box>
            <Box my={8} textAlign="left">
              <form onSubmit={handleSubmit}>
                <FormControl isRequired mt={4}>
                  <FormLabel>User ID</FormLabel>
                  <Input name="userId" value={userId} onChange={(e) => setUserId(e.target.value)} />
                </FormControl>
                <FormControl isRequired mt={4}>
                  <FormLabel>Password</FormLabel>
                  <Input name="password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
                </FormControl>
                <Button mt={4} colorScheme="primary" type="submit">Login</Button>
              </form>
            </Box>
          </Box>
        </Box>
    </Flex>
  );
}
