module SimulationSolver

using DifferentialEquations

include("Utils.jl")

using .Utils

export safe_solve_reaction_system

function safe_solve_reaction_system(reaction_network, initial_conditions, tspan)
  prob = ODEProblem(ODESystem(reaction_network), initial_conditions, tspan)

  try
    sol = solve(prob)
    if any(isnan, sol.u) || any(isinf, sol.u)
      return Dict("error" => "Solution contains NaN or Inf values. Check equations and parameters.")
    end
    return Dict("time" => sol.t, "solution" => [Array(sol[i, :]) for i in 1:length(sol.u)])
  catch e
    return Dict("error" => string("Failed to solve: ", e))
  end
end

end
