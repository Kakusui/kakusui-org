import {
  Button,
  chakra,
  Container,
  Flex,
  Heading,
  Text,
  VStack
} from "@chakra-ui/react";

const InternalErrorPage = () => {
  return (
    <Flex
      bg="gray.800"
      minH="87vh"
      align="center"
      justify="center"
      color="white"
    >
      <Container textAlign="center" maxW="md">
        <VStack spacing={6}>
          <Heading as="h1" size="2xl">
            Oops!
          </Heading>
          <Text fontSize="2xl" fontWeight="semibold">
            500 - Server Error
          </Text>
          <Text fontSize="lg">
            It seems like something went wrong on our end...
          </Text>
          <Button
            as="a"
            href="/"
            bg="blue.600"
            color="white"
            py={2}
            px={4}
            rounded="md"
            mb={4}
            _hover={{
              bg: "black",
              color: "blue.600",
              transition: "0.3s",
            }}
          >
            Return to Home
          </Button>
          <chakra.a
            href="https://github.com/kakusui/kakusui-org/issues"
            target="_blank"
            color="blue.400"
            _hover={{ color: "white" }}
          >
            Something Broken? Tell us!
          </chakra.a>
        </VStack>
      </Container>
    </Flex>
  );
};

export default InternalErrorPage;