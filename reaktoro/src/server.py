import grpc
from concurrent import futures
import reactions_pb2
import reactions_pb2_grpc


class ChemistryService(reactions_pb2_grpc.ChemistryServiceServicer):
    def ComputeReaction(self, request, context):
        # Sample response; replace with your logic
        return reactions_pb2.ReactionResponse(result="Computed reaction")

    def ComputeThermodynamics(self, request, context):
        # Sample response; replace with your logic
        return reactions_pb2.ThermodynamicsResponse(result="Computed thermodynamics")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    reactions_pb2_grpc.add_ChemistryServiceServicer_to_server(
        ChemistryService(), server
    )
    server.add_insecure_port("[::]:50051")  # Ensure it listens on port 50051
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
