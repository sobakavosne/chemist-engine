from flask import Flask, request, jsonify
import grpc
import chemistry_pb2
import chemistry_pb2_grpc

app = Flask(__name__)

# Establish a gRPC channel
channel = grpc.insecure_channel('localhost:50051')
stub = chemistry_pb2_grpc.ChemistryServiceStub(channel)

@app.route('/reactions', methods=['POST'])
def reactions():
    data = request.json
    # Prepare the gRPC request
    reaction_request = chemistry_pb2.ReactionRequest(
        species=data['species'],
        rate_constant=data['rate_constant']
    )
    # Make the gRPC call
    reaction_response = stub.ComputeReaction(reaction_request)
    return jsonify({"result": reaction_response.result})

@app.route('/thermodynamics', methods=['POST'])
def thermodynamics():
    data = request.json
    # Prepare the gRPC request
    thermo_request = chemistry_pb2.ThermodynamicsRequest(parameters=data['parameters'])
    # Make the gRPC call
    thermo_response = stub.ComputeThermodynamics(thermo_request)
    return jsonify({"result": thermo_response.result})

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=5000)
