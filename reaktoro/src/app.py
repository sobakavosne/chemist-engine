import logging
from flask import Flask, request, jsonify
from reactions import compute_reaction
from thermo import compute_thermodynamics

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route("/reactions", methods=["POST"])
def reactions():
    data = request.json
    logger.info("Received POST request on /reactions with data: %s", data)

    # Ensure data has the correct structure
    try:
        species = data["species"]  # Should be a list of strings
        rate_constant = float(data["rate_constant"])  # Ensure it's a float
    except (KeyError, TypeError, ValueError) as e:
        logger.error("Invalid input data: %s", e)
        return jsonify({"error": f"Invalid input data: {e}"}), 400

    # Compute reaction result
    result = compute_reaction(species, rate_constant)
    logger.info("Reaction computation result: %s", result)
    return jsonify({"result": result})


@app.route("/thermodynamics", methods=["POST"])
def thermodynamics():
    data = request.json
    logger.info("Received POST request on /thermodynamics with data: %s", data)

    # Compute thermodynamics result
    try:
        parameters = data["parameters"]
    except KeyError as e:
        logger.error("Invalid input data: %s", e)
        return jsonify({"error": f"Invalid input data: {e}"}), 400

    result = compute_thermodynamics(parameters)
    logger.info("Thermodynamics computation result: %s", result)
    return jsonify({"result": result})


if __name__ == "__main__":
    from waitress import serve

    logger.info("Starting Flask server with Waitress on port 5000")
    serve(app, host="0.0.0.0", port=5000)
