module InitialConditions

export setup_initial_conditions

# Sets up initial conditions for the reaction system
function setup_initial_conditions(reaction_data)
  # Convert the `initial_conditions` key in the input to a dictionary with Symbol keys
  Dict(Symbol(k) => v for (k, v) in reaction_data["initial_conditions"])
end

end
