module InitialConditions

export setup_initial_conditions

function setup_initial_conditions(reaction_data)
  Dict(Symbol(k) => v for (k, v) in reaction_data["initial_conditions"])
end

end
