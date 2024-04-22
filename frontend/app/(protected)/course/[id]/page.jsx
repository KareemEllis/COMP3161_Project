'use client'
import { 
    Container,
    Box, 
    Heading, 
    Text, 
    VStack, 
    Accordion, AccordionItem, AccordionButton, AccordionPanel, AccordionIcon, 
    Tag, 
    Link,
    Table, Thead, Tbody, Tr, Th, Td,
    List, ListItem, ListIcon,
    useColorModeValue 
} from '@chakra-ui/react';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';

import { FaUserGraduate, FaChalkboardTeacher, FaCalendarAlt } from 'react-icons/fa';

import { getCourseById } from '@/services/course';
import { getCourseContent } from '@/services/course-content';
import { getCourseAssignments } from '@/services/assignment';
import { getCourseMembers } from '@/services/course';
import { getCalendarEventsForCourse } from '@/services/calendar';

const CourseContentPage = ({ params }) => {
    const [course, setCourse] = useState(null); // [1
    const [courseContent, setCourseContent] = useState(null);
    const [assignments, setAssignments] = useState([]);
    const [members, setMembers] = useState([]);
    const [calendarEvents, setCalendarEvents] = useState([])

    const id = params.id;

    const primaryColor = useColorModeValue('primary.500', 'primary.300');
    const accentColor = useColorModeValue('accent.400', 'accent.200');

    useEffect(() => {
      const fetchData = async () => {
        try {
            const courseData = await getCourseById(id);
            setCourse(courseData);
            const contentData = await getCourseContent(id);
            setCourseContent(contentData);
            const assignmentsData = await getCourseAssignments(id);
            setAssignments(assignmentsData.assignments);
            const membersData = await getCourseMembers(id);
            setMembers(membersData.members);
            const calendarEventData = await getCalendarEventsForCourse(id);
        setCalendarEvents(calendarEventData.calendarEvents);
        } catch (error) {
            console.error('Error retrieving data:', error);
        }
      };

      fetchData();
    }, [id]);

    // Helper function to render section content appropriately
    const renderSectionContent = (content) => {
        // Check if the content is a link to a file (e.g., ends in .pdf)
        const fileFormats = ['.pdf', '.docx', '.pptx', '.xlsx', '.csv', '.txt', '.zip', '.jpg', '.png', '.jpeg', '.gif', '.mp4', '.mp3', '.wav', '.flac', '.avi', '.mov', '.mkv', '.webm', '.ogg', '.flv', '.wmv', '.wma', '.m4a', '.aac', '.flac', '.opus', '.webp', '.svg', '.eps', '.ai', '.psd', '.tiff', '.bmp', '.ico', '.webp', '.heic', '.heif', '.avif', '.pdf', '.docx', '.pptx', '.xlsx', '.csv', '.txt', '.zip', '.jpg', '.png', '.jpeg', '.gif', '.mp4', '.mp3', '.wav', '.flac', '.avi', '.mov', '.mkv', '.webm', '.ogg', '.flv', '.wmv', '.wma', '.m4a', '.aac', '.flac', '.opus', '.webp', '.svg', '.eps', '.ai', '.psd', '.tiff', '.bmp', '.ico', '.webp', '.heic', '.heif', '.avif'];

        if (fileFormats.some(format => content.endsWith(format))) {
            return (
                <Link href={'#'} color={'primary.600'}>
                {content}
                </Link>
            );
        }
        // Default text rendering
        return <Text>{content}</Text>;
    };

  if (!courseContent) {
    return <Text>Loading course content...</Text>;
  }

  return (
    <Container maxW={'5xl'} mt={5} mb={5}>
    <Box p={5}>
      <VStack spacing={4} align="start">
        <Heading color={primaryColor}>Course: {course?.CourseName}</Heading>
        <Text fontWeight={'bold'}>{courseContent?.courseId}</Text>
        <Tag colorScheme="blue">{course?.Period}</Tag>

        {/* Members list */}
        <Heading size="md" my={4}>Members</Heading>
        <List>
          {members.map(member => (
            <ListItem key={member.UserId} display="flex" alignItems="center">
              <ListIcon as={member.AccType === 'Student' ? FaUserGraduate : FaChalkboardTeacher} color={accentColor} />
              {member.Name} - {member.AccType}
            </ListItem>
          ))}
        </List>

        {/* Assignments */}
        <Box w="full">
          <Heading size="md" my={4}>Assignments</Heading>
          <Table variant="simple">
            <Thead>
              <Tr>
                <Th>Title</Th>
                <Th isNumeric>Due Date</Th>
              </Tr>
            </Thead>
            <Tbody>
              { assignments && assignments.map((assignment) => (
                <Tr key={assignment.AssignmentId}>
                  <Td>{assignment.AssignmentTitle}</Td>
                  <Td isNumeric>{assignment.DueDate}</Td>
                </Tr>
              ))}
            </Tbody>
          </Table>
        </Box>
        
        {/* Calendar Events Section */}
        <Heading size="md" my={4}>Calendar Events</Heading>
        <List>
          {calendarEvents.map((event) => (
            <ListItem key={event.EventId} display="flex" alignItems="center">
              <ListIcon as={FaCalendarAlt} color={accentColor} mr={2} />
              <Box flex="1">
                <Text fontWeight="bold">{event.EventTitle}</Text>
                <Text fontSize="sm">{event.Description}</Text>
                <Text fontSize="sm">Starts: {event.StartDate}</Text>
                <Text fontSize="sm">Ends: {event.EndDate}</Text>
              </Box>
            </ListItem>
          ))}
        </List>

        {/* Course Content */}
        <Heading size="md" my={4}>Content</Heading>
        {courseContent && courseContent.sections.map((section) => (
          <Accordion allowToggle key={section.SectionId} w="full">
            <AccordionItem borderLeftColor={primaryColor} borderLeftWidth={4}>
              <h2>
                <AccordionButton _expanded={{ bg: accentColor, color: 'white' }}>
                  <Box flex="1" textAlign="left">
                    {section.SectionTitle}
                  </Box>
                  <AccordionIcon />
                </AccordionButton>
              </h2>
              <AccordionPanel pb={4}>
                <Text mt={4} fontWeight="bold">Topics:</Text>
                {section.Topics.map((topic) => (
                  <Tag key={topic.TopicId} colorScheme="blue" mr={2} mt={2}>{topic.TopicTitle}</Tag>
                ))}

                <Text mt={4} fontWeight="bold">Content:</Text>
                {section.SectionItems.map((item) => (
                  <Box key={item.ItemId} my={2}>
                    {renderSectionContent(item.SectionContent)}
                  </Box>
                ))}
              </AccordionPanel>
            </AccordionItem>
          </Accordion>
        ))}
      </VStack>
    </Box>
    </Container>
  );
};

export default CourseContentPage;
