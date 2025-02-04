"""
Module for Server with Logging
"""

import logging
from concurrent import futures
import grpc
from .. import minitwitter_pb2
from .. import minitwitter_pb2_grpc

# Configure logging
logging.basicConfig(
    filename="logs/server.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

messages: list[str] = []


class MiniTwitterServicer(minitwitter_pb2_grpc.MiniTwitterServicer):
    """
    gRPC Servicer class for handling MiniTwitter commands.
    """

    def sendMessage(self, request, context):
        """
        Handles sending a message by appending it to the messages list.

        Args:
            request: The request containing the message to be sent.
            context: The gRPC context (unused here).

        Returns:
            A MessageResponse with a status message.
        """
        messages.append(request.message)
        logging.info("Received message: '%s'", request.message)
        return minitwitter_pb2.MessageResponse(status="Message sent successfully")

    def getMessages(self, request, context):
        """
        Retrieves the most recent messages up to the specified count.

        Args:
            request: The request containing the count of messages to retrieve.
            context: The gRPC context (unused here).

        Returns:
            A MessageListResponse containing the messages.
        """
        recent_messages = messages[-request.count:]
        logging.info("Retrieving last %d messages - Sent: %s", request.count, recent_messages)
        return minitwitter_pb2.MessageListResponse(
            messages=recent_messages, status="Messages retrieved successfully"
        )


def serve() -> None:
    """
    Start the gRPC server to handle client requests.

    This function starts the server, binds it to port 50051, and waits for termination.
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    minitwitter_pb2_grpc.add_MiniTwitterServicer_to_server(MiniTwitterServicer(), server)
    server.add_insecure_port("[::]:50051")

    server.start()
    logging.info("MiniTwitter server started on port 50051")
    print("MiniTwitter server started on port 50051")

    server.wait_for_termination()


if __name__ == "__main__":
    serve()
