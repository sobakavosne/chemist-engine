import logging
from flask import Flask, request, jsonify
from equilibrium import compute_equilibrium
from kinetics import compute_kinetics

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route("/api/equilibrium", methods=["POST"])
def compute_equilibrium_handler():
    """
    Handles POST requests to the /api/equilibrium endpoint for equilibrium calculations.

    Expects a JSON payload with the following structure:
        {
            "species": ["H2O", "Na+", "Cl-", "CO2"],
            "temperature": 60.0,      # Optional, default 298.15 K
            "pressure_bounds": [1.0, 1000.0],  # Optional, bar
            "phase_amount": 1e-6,    # Optional, default 1e-6 mol
            "phase_name": "GaseousPhase"  # Optional, default "GaseousPhase"
        }
    """
    try:
        # Validate JSON payload
        if not request.is_json:
            logger.error("Invalid request: Content-Type must be application/json")
            return jsonify({"error": "Content-Type must be application/json"}), 400

        data = request.get_json()
        logger.info("Received POST request on /api/equilibrium with data: %s", data)

        # Extract required parameters
        species = data.get("species")
        if not species or not isinstance(species, list):
            logger.error("Invalid 'species' key in input data.")
            return jsonify({"error": "'species' must be a non-empty list."}), 400

        # Extract optional parameters with defaults
        temperature = data.get("temperature", 298.15)
        phase_name = data.get("phase_name", "GaseousPhase")
        phase_amount = data.get("phase_amount", 1e-6)
        pressure_bounds = data.get("pressure_bounds", [1.0, 1000.0])

        if not isinstance(pressure_bounds, list) or len(pressure_bounds) != 2:
            logger.error("Invalid 'pressure_bounds' format.")
            return (
                jsonify(
                    {
                        "error": "'pressure_bounds' must be a list of two values [lower, upper]."
                    }
                ),
                400,
            )

        # Perform equilibrium calculation
        result = compute_equilibrium(
            species=species,
            temperature=temperature,
            phase_amount=phase_amount,
            phase_name=phase_name,
            pressure_bounds=tuple(pressure_bounds),
        )

        # Respond with the result
        logger.info("Equilibrium computation completed successfully.")
        return jsonify(result), 200

    except KeyError as e:
        logger.error("Invalid input data: Missing key - %s", e)
        return jsonify({"error": f"Invalid input data: Missing key - {str(e)}"}), 400

    except Exception as e:
        logger.exception("An error occurred during equilibrium computation.")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


@app.route("/api/kinetics", methods=["POST"])
def compute_kinetics_handler():
    """
    Handles POST requests to /api/kinetics endpoint for performing kinetics simulations.

    Expects a JSON payload with the following structure:
        {
            "database": "phreeqc.dat",
            "components": ["H2O", "Na+", "Cl-", "CO2"],
            "mineral": "Halite",
            "reaction": "Halite = Na+ + Cl-",
            "rate_constant": 0.001,
            "volume": 1.0,
            "timestep": 60.0,
            "total_time": 3600.0
        }
    """
    try:
        # Parse and validate input JSON
        if not request.is_json:
            logger.error("Invalid request: Content-Type must be application/json")
            return jsonify({"error": "Content-Type must be application/json"}), 400

        data = request.get_json()
        logger.info("Received POST request on /api/kinetics with data: %s", data)

        # Validate required fields
        required_keys = [
            "database",
            "components",
            "mineral",
            "reaction",
            "rate_constant",
            "volume",
            "timestep",
            "total_time",
        ]
        missing_keys = [key for key in required_keys if key not in data]
        if missing_keys:
            logger.error("Missing required keys in input data: %s", missing_keys)
            return (
                jsonify({"error": f"Missing required keys: {', '.join(missing_keys)}"}),
                400,
            )

        # Perform the kinetics computation
        result = compute_kinetics(
            database=data["database"],
            components=data["components"],
            mineral=data["mineral"],
            reaction=data["reaction"],
            rate_constant=data["rate_constant"],
            volume=data["volume"],
            timestep=data["timestep"],
            total_time=data["total_time"],
        )
        logger.info("Kinetics computation completed successfully")

        # Return the computed results
        return jsonify({"result": result}), 200

    except KeyError as e:
        logger.error("Invalid input data: Missing key - %s", e)
        return jsonify({"error": f"Invalid input data: Missing key - {str(e)}"}), 400

    except Exception as e:
        logger.exception("An error occurred during kinetics computation")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


if __name__ == "__main__":
    from waitress import serve

    logger.info("Starting Flask server with Waitress on port 8082")
    serve(app, host="0.0.0.0", port=8082)
