'use client'
import { Button, Flex, Heading, Text, VStack, Link as ChakraLink } from '@chakra-ui/react';
import Link from 'next/link';

export default function Home() {
  return (
    <Flex minHeight="100vh" width="full" align="center" justifyContent="center" direction="column" bg="primary.50">
      <VStack spacing={8}>
        <Heading color="primary.800">OurVLE</Heading>
        <Text fontSize="xl" color="primary.600">Your Virtual Learning Environment</Text>
        <Flex gap={4}>
            <Button as={ChakraLink} href='/login' colorScheme="primary" variant="solid">
              Login
            </Button>
            <Button as={ChakraLink} href='/register' colorScheme="accent" variant="outline">
              Register
            </Button>
        </Flex>
      </VStack>
    </Flex>
  );
}
