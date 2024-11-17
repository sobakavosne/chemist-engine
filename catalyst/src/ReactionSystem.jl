module ReactionSystem

using Catalyst
using ModelingToolkit

export create_reaction_system

"""
    create_reaction_system(reaction_data::Dict)

Creates a `ReactionSystem` from the provided reaction data dictionary.

# Arguments
- `reaction_data::Dict`: A dictionary with the following keys:
  - `"species"`: An array of species names (strings).
  - `"reactions"`: An array of reaction definitions. Each reaction definition is a dictionary with:
    - `"rate_constant"`: The reaction rate constant (numeric).
    - `"reactants"`: A list of reactant species (strings).
    - `"products"`: A list of product species (strings).

# Returns
A `ReactionSystem` instance representing the reaction network.
"""
function create_reaction_system(reaction_data::Dict)
  # Ensure `reactions` is a list
  if !isa(reaction_data["reactions"], Vector)
    throw(ErrorException("Expected 'reactions' to be an array but found another type."))
  end

  # Convert species names to symbolic variables
  @species species = Symbol.(reaction_data["species"])
  println("Species: ", species)

  # Create Catalyst reactions
  reactions = map(r -> Reaction(
      r["rate_constant"],              # Reaction rate constant
      Symbol.(r["reactants"]) .|> t -> getindex(species, findfirst(x -> x == Symbol(t), reaction_data["species"])), # Match reactants
      Symbol.(r["products"]) .|> t -> getindex(species, findfirst(x -> x == Symbol(t), reaction_data["species"]))  # Match products
    ), reaction_data["reactions"])
  println("Reactions: ", reactions)

  # Time parameter for the reaction system
  @parameters t

  # Construct and return the ReactionSystem
  ReactionSystem(reactions, t, species)
end

end
