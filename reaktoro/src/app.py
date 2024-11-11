import os
import grpc
from flask import Flask, request, jsonify
import reactions_pb2
import reactions_pb2_grpc

app = Flask(__name__)

# Use Docker service name to connect to the gRPC server
grpc_server_host = os.getenv("GRPC_SERVER_HOST", "chemist-engine-reaktoro")
channel = grpc.insecure_channel(f"{grpc_server_host}:50051")
stub = reactions_pb2_grpc.ChemistryServiceStub(channel)


@app.route("/reactions", methods=["POST"])
def reactions():
    data = request.json

    # Ensure data has the correct structure
    try:
        species = data["species"]  # Should be a list of strings
        rate_constant = float(data["rate_constant"])  # Ensure it's a float
    except (KeyError, TypeError, ValueError) as e:
        return jsonify({"error": f"Invalid input data: {e}"}), 400

    # Prepare the gRPC request
    reaction_request = reactions_pb2.ReactionRequest(
        species=species, rate_constant=rate_constant
    )

    # Make the gRPC call
    try:
        reaction_response = stub.ComputeReaction(reaction_request)
        return jsonify({"result": reaction_response.result})
    except grpc.RpcError as e:
        return jsonify({"error": f"gRPC error: {e.details()}"}), 500


@app.route("/thermodynamics", methods=["POST"])
def thermodynamics():
    data = request.json
    # Prepare the gRPC request
    thermo_request = reactions_pb2.ThermodynamicsRequest(parameters=data["parameters"])
    # Make the gRPC call
    thermo_response = stub.ComputeThermodynamics(thermo_request)
    return jsonify({"result": thermo_response.result})


if __name__ == "__main__":
    from waitress import serve

    serve(app, host="0.0.0.0", port=5000)
