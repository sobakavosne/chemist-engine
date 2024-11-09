module ReactionSystem

using Catalyst

export create_reaction_system

function create_reaction_system(reaction_data)
  if !isa(reaction_data["reactions"], Vector)
    throw(ErrorException("Expected 'reactions' to be an array but found a dictionary or other type."))
  end

  species = Symbol.(reaction_data["species"])

  reactions = map(r -> Reaction(
      r["rate_constant"],
      Symbol.(r["reactants"]) => Symbol.(r["products"])
    ), reaction_data["reactions"])

  @parameters t
  ReactionSystem(reactions, t, species, [Symbol(r["name"]) for r in reaction_data["reactions"]])
end

end
