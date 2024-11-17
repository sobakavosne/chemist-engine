using HTTP
using JSON
using Catalyst
using DifferentialEquations

include("ReactionSystem.jl")
include("InitialConditions.jl")
include("SimulationSolver.jl")

using .ReactionSystem, .InitialConditions, .SimulationSolver

# Router to handle incoming requests
using URIs

function router(req::HTTP.Request)
    # Parse the URI from the request
    uri = URIs.URI(req.target)
    
    # Route based on the path
    if uri.path == "/api/kinetics"
        return handle_kinetics_request(req)
    elseif uri.path == "/api/equilibrium"
        return handle_equilibrium_request(req)
    else
        return HTTP.Response(404, "Not Found")
    end
end


# Handles requests to the `/api/kinetics` endpoint
function handle_kinetics_request(req::HTTP.Request)
    try
        # Parse request body
        data = JSON.parse(String(req.body))
        println("Kinetics request data: ", data)

        # Create reaction system and solve kinetics
        reaction_network = create_reaction_system(data)
        initial_conditions = setup_initial_conditions(data)
        tspan = data["tspan"]
        result = safe_solve_reaction_system(reaction_network, initial_conditions, tspan)

        println("Kinetics computation successful.")
        return HTTP.Response(200, JSON.json(result))
    catch e
        println("Error in /api/kinetics: ", e)
        return HTTP.Response(400, JSON.json(Dict("error" => "Invalid kinetics request")))
    end
end

# Handles requests to the `/api/equilibrium` endpoint
function handle_equilibrium_request(req::HTTP.Request)
    try
        # Parse request body
        data = JSON.parse(String(req.body))
        println("Equilibrium request data: ", data)

        # Create equilibrium simulation
        reaction_network = create_reaction_system(data)
        initial_conditions = setup_initial_conditions(data)
        tspan = data["tspan"]
        result = safe_solve_reaction_system(reaction_network, initial_conditions, tspan)

        println("Equilibrium computation successful.")
        return HTTP.Response(200, JSON.json(result))
    catch e
        println("Error in /api/equilibrium: ", e)
        return HTTP.Response(400, JSON.json(Dict("error" => "Invalid equilibrium request")))
    end
end

# Starts the server
function start_server()
    println("Starting CatalystServer...")

    host = "0.0.0.0"
    port = 8083
    HTTP.serve(router, host, port)
end

# Run the server
start_server()
