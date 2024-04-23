// pages/forum/[forum_id].js
'use client'
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import {
  Box, Container, Heading, VStack, Text, Divider
} from '@chakra-ui/react';
import { getForumById, getForumThreads, getThreadReplies } from '@/services/forum';

// Component to render individual threads and their nested replies
const Thread = ({ thread, level = 0 }) => {
  const [replies, setReplies] = useState([]);
  console.log('Thread Displayed: ', thread);

  useEffect(() => {
    const fetchThreadAndReplies = async () => {
      const repliesData = await getThreadReplies(thread.ThreadId);
      console.log('Replies fetched for Thread: ', thread.ThreadId);
      console.log(repliesData)
      setReplies(repliesData.replies);
    };

    fetchThreadAndReplies();
  }, []);

  return (
    <>
    {thread && 
        <VStack align="start" pl={level * 4} spacing={2}>
      <Text fontWeight="bold">{thread.ThreadTitle}</Text>
      <Text>{thread.ThreadContent}</Text>
      {replies.map(reply => (
        <Thread key={reply.ThreadId} thread={reply} level={level + 1} />
      ))}
    </VStack>
    }
    </>
    
  );
};

const ForumPage = ({ params }) => {
  const [forum, setForum] = useState(null);
  const [threads, setThreads] = useState([]);
  const router = useRouter();
  const forum_id = params.id;

  useEffect(() => {
    const fetchData = async () => {
      const forumData = await getForumById(forum_id);
      setForum(forumData);

      const threadsData = await getForumThreads(forum_id);
      setThreads(threadsData.threads);
    };

    if (forum_id) fetchData();
  }, [forum_id]);

  return (
    <Container maxW="xl" mt={5}>
      {forum && (
        <VStack spacing={4}>
          <Heading>{forum.ForumTitle}</Heading>
          {threads.map(thread => (
            <Box key={thread.ThreadId} w="full">
              <Thread thread={thread} />
              <Divider my={4} />
            </Box>
          ))}
        </VStack>
      )}
    </Container>
  );
};

export default ForumPage;
