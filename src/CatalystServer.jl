using HTTP
using JSON

include("ReactionSystem.jl")
include("InitialConditions.jl")
include("SimulationSolver.jl")
include("Utils.jl")

using .ReactionSystem, .InitialConditions, .SimulationSolver, .Utils

function load_config()
  config_path = joinpath(@__DIR__, "..", "config", "config.json")
  return JSON.parsefile(config_path)
end

function handle_request(req::HTTP.Request)
  try
    reaction_data = JSON.parse(String(req.body))
  
    reaction_network = create_reaction_system(reaction_data)
    println("reaction_network: ", reaction_network)
    initial_conditions = setup_initial_conditions(reaction_data)
    println("initial_conditions: ", initial_conditions)
    tspan = (reaction_data["tspan"][1], reaction_data["tspan"][2])

    result = safe_solve_reaction_system(reaction_network, initial_conditions, tspan)

    println("INFO: Successful response - ", JSON.json(result))

    return HTTP.Response(200, JSON.json(result))
  catch e
    error_response = Dict("error" => string("Request failed: ", e))
    println("ERROR: Response - ", JSON.json(error_response))

    return HTTP.Response(400, JSON.json(error_response))
  end
end

function start_server()
  config = load_config()
  host = config["host"]
  port = config["port"]
  HTTP.serve(handle_request, host, port)
end

start_server()
