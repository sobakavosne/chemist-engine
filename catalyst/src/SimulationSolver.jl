module SimulationSolver

using DifferentialEquations

include("Utils.jl")

using .Utils

export safe_solve_reaction_system

# Safely solves the reaction system and handles errors or edge cases
function safe_solve_reaction_system(reaction_network, initial_conditions, tspan)
  # Create an ODE problem from the reaction network
  prob = ODEProblem(ODESystem(reaction_network), initial_conditions, tspan)

  try
    # Solve the ODE problem
    sol = solve(prob)

    # Check for invalid solutions (NaN or Inf values)
    if any(isnan, sol.u) || any(isinf, sol.u)
      return Dict("error" => "Solution contains NaN or Inf values. Check equations and parameters.")
    end

    # Return the solution as a dictionary
    return Dict(
      "time" => sol.t,                          # Simulation time points
      "solution" => [Array(sol[i, :]) for i in 1:length(sol.u)]  # Solution values for each species
    )
  catch e
    # Handle errors during solution
    return Dict("error" => string("Failed to solve: ", e))
  end
end

end
