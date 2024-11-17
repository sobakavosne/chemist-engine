from reaktoro import *


def compute_equilibrium(
    species, temperature, phase_amount, phase_name, pressure_bounds=None
):
    """
    Computes chemical equilibrium with a fixed phase amount using Reaktoro.

    Args:
        species (list): List of species involved in the system.
        temperature (float): Temperature of the system in Celsius.
        phase_amount (float): Amount of the constrained phase (e.g., gaseous phase) in mol.
        phase_name (str): Name of the constrained phase (e.g., "GaseousPhase").
        pressure_bounds (tuple, optional): A tuple specifying lower and upper bounds for pressure in bar.

    Returns:
        dict: Results containing final state properties and computation status.
    """
    try:
        # Step 1: Define the chemical system
        db = PhreeqcDatabase("pitzer.dat")

        # Create the aqueous and gaseous phases
        solution = AqueousPhase(speciate(" ".join(species)))
        solution.set(ActivityModelPitzer())

        gases = GaseousPhase(f"{species[-1]}(g)")  # Assume the last species is gaseous
        gases.set(ActivityModelPengRobinsonPhreeqcOriginal())

        system = ChemicalSystem(db, solution, gases)

        # Step 2: Define the initial chemical state
        state = ChemicalState(system)
        state.temperature(temperature, "celsius")

        # Set initial amounts for all species
        for specie in species:
            state.set(specie, 1.0, "mol")
        state.set("H2O", 1.0, "kg")  # Initial water amount

        # Step 3: Set up equilibrium specifications
        specs = EquilibriumSpecs(system)
        specs.temperature()
        specs.phaseAmount(phase_name)

        solver = EquilibriumSolver(specs)

        # Step 4: Define equilibrium conditions
        conditions = EquilibriumConditions(specs)
        conditions.temperature(temperature, "celsius")
        conditions.phaseAmount(phase_name, phase_amount, "mol")

        # Set pressure bounds if provided
        if pressure_bounds:
            lower_bound, upper_bound = pressure_bounds
            conditions.setLowerBoundPressure(lower_bound, "bar")
            conditions.setUpperBoundPressure(upper_bound, "bar")

        # Step 5: Solve equilibrium problem
        result_status = solver.solve(state, conditions)

        if result_status.succeeded:
            # Extract final pressure and species amounts
            final_pressure = float(state.pressure())  # Convert pressure to float
            species_amounts = {
                specie: float(state.speciesAmount(specie)) for specie in species
            }

            result = {
                "status": "success",
                "temperature": temperature,
                "pressure": final_pressure,
                "species_amounts": species_amounts,
                "message": "Equilibrium computation completed successfully.",
            }
        else:
            result = {
                "status": "failure",
                "message": "Equilibrium computation failed.",
                "error": result_status.message,
            }

        return result

    except AttributeError as e:
        return {
            "status": "failure",
            "message": "Invalid API usage: Missing method or attribute.",
            "error": str(e),
        }

    except Exception as e:
        return {
            "status": "failure",
            "message": "An unexpected error occurred.",
            "error": str(e),
        }
