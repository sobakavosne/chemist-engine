from reaktoro import *


def compute_kinetics(
    database, components, mineral, reaction, rate_constant, volume, timestep, total_time
):
    """
    Simulates chemical kinetics using Reaktoro.

    Args:
        database (str): Path to the thermodynamic database (e.g., "phreeqc.dat").
        components (list): List of chemical components for the system.
        mineral (str): Name of the mineral phase (e.g., "Halite").
        reaction (str): General reaction string for the mineral (e.g., "Halite = Na+ + Cl-").
        rate_constant (float): Reaction rate constant (k0).
        volume (float): Initial volume of the mineral phase in cm³.
        timestep (float): Time step for kinetics simulation in seconds.
        total_time (float): Total simulation time in seconds.

    Returns:
        dict: Results containing time, mineral volume, and species amounts.
    """

    # Reaction rate model function
    Abar = 6.0  # Surface area per volume (m²/m³)

    def ratefn(props: ChemicalProps):
        """
        Defines the reaction rate model.
        """
        aprops = AqueousProps(props)  # Get aqueous properties
        q = props.phaseProps(mineral).volume()  # Current mineral volume in m³
        Omega = aprops.saturationRatio(mineral)  # Saturation ratio Ω = IAP/K
        return q * Abar * rate_constant * (1 - Omega)  # Net reaction rate

    # Step 1: Initialise the chemical system
    db = PhreeqcDatabase(database)
    system = ChemicalSystem(
        db,
        AqueousPhase(" ".join(components)).set(ActivityModelPhreeqc(db)),
        MineralPhase(mineral),
        GeneralReaction(reaction).setRateModel(ratefn),
    )

    # Step 2: Set up the initial state
    state = ChemicalState(system)
    state.temperature(25.0, "C")
    state.pressure(1.0, "bar")
    state.set("H2O", 1.0, "kg")  # 1 kg of pure water
    state.scalePhaseVolume(mineral, volume, "cm3")  # Initial mineral volume

    # Step 3: Configure kinetics solver
    solver = KineticsSolver(system)

    # Step 4: Run simulation
    table = Table()
    steps = int(total_time / timestep)

    for i in range(steps + 1):
        result = solver.solve(state, timestep)
        assert result.succeeded(), f"Calculation failed at timestep {i}."

        props = state.props()
        table.column("Time") << i * timestep / 60  # Convert time to minutes
        (
            table.column(mineral) << props.phaseProps(mineral).volume() * 1e6
        )  # Convert m³ to cm³
        for species in components:
            table.column(species) << props.speciesAmount(
                species
            )  # Species amounts in mol

    # Prepare results
    return {
        "time": table["Time"],
        "mineral_volume": table[mineral],
        "species_amounts": {species: table[species] for species in components},
    }
