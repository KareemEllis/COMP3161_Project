'use client'
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import {
  Box, Button, Flex, FormControl, FormLabel, Input, Select, useToast,
} from '@chakra-ui/react';
import { registerUser } from '@/services/auth';

export default function Register() {
  const [formData, setFormData] = useState({
    userId: '',
    username: '',
    name: '',
    password: '',
    accType: '',
  });
  const toast = useToast();
  const router = useRouter();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await registerUser(formData.userId, formData.username, formData.name, formData.password, formData.accType);
      toast({
        title: 'Registration successful.',
        description: "You're now redirected to login.",
        status: 'success',
        duration: 5000,
        isClosable: true,
      });
      router.push('/login');
    } catch (error) {
      toast({
        title: 'Registration failed.',
        description: error.message.toString(),
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
  };

  return (
    <Flex minHeight="100vh" width="full" align="center" justifyContent="center" bg="primary.50">
      <Box borderWidth="1px" px={4} width="full" maxWidth="500px" borderRadius="lg" textAlign="center" boxShadow="lg" bg="white">
        <Box p={4}>
          <Box textAlign="center">
            <Box>Register</Box>
          </Box>
          <Box my={8} textAlign="left">
            <form onSubmit={handleSubmit}>
              <FormControl isRequired>
                <FormLabel>User ID</FormLabel>
                <Input name="userId" value={formData.userId} onChange={handleChange} />
              </FormControl>
              <FormControl isRequired mt={4}>
                <FormLabel>Username</FormLabel>
                <Input name="username" value={formData.username} onChange={handleChange} />
              </FormControl>
              <FormControl isRequired mt={4}>
                <FormLabel>Full Name</FormLabel>
                <Input name="name" value={formData.name} onChange={handleChange} />
              </FormControl>
              <FormControl isRequired mt={4}>
                <FormLabel>Password</FormLabel>
                <Input name="password" type="password" value={formData.password} onChange={handleChange} />
              </FormControl>
              <FormControl isRequired mt={4}>
                <FormLabel>Account Type</FormLabel>
                <Select name="accType" value={formData.accType} onChange={handleChange}>
                  <option value="">Select Account Type</option>
                  <option value="Admin">Admin</option>
                  <option value="Student">Student</option>
                  <option value="Course Maintainer">Course Maintainer</option>
                </Select>
              </FormControl>
              <Button mt={4} colorScheme="primary" type="submit">Register</Button>
            </form>
          </Box>
        </Box>
      </Box>
    </Flex>
  );
}
