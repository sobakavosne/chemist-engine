from concurrent import futures
import grpc
import chemistry_pb2
import chemistry_pb2_grpc
from reactions import compute_reaction
from thermo import compute_thermodynamics

class ChemistryService(chemistry_pb2_grpc.ChemistryServiceServicer):
    def ComputeReaction(self, request, context):
        # Use the provided data to compute the reaction
        result = compute_reaction({
            "species": request.species,
            "rate_constant": request.rate_constant
        })
        return chemistry_pb2.ReactionResponse(result=result)

    def ComputeThermodynamics(self, request, context):
        # Use the provided data to compute thermodynamics
        result = compute_thermodynamics({"parameters": request.parameters})
        return chemistry_pb2.ThermodynamicsResponse(result=result)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chemistry_pb2_grpc.add_ChemistryServiceServicer_to_server(ChemistryService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
