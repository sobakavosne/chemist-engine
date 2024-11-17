Analytical engine API (mocked):

  - Reaktoro 
  - Catalyst.jl

Usage:

  $> docker compose -f docker-compose.yml up --build

  --Reaktoro--

  $> curl -X POST http://localhost:8082/api/kinetics -H "Content-Type: application/json" -d '{
      "database": "phreeqc.dat",
      "components": ["H2O", "H+", "Na+", "Cl-", "CO2"],
      "mineral": "Halite",
      "reaction": "Halite = Na+ + Cl-",
      "rate_constant": 0.001,
      "volume": 1.0,
      "timestep": 60.0,
      "total_time": 3600.0
  }'

  $> curl -X POST http://127.0.0.1:8082/api/equilibrium -H "Content-Type: application/json" -d '{
      "species": ["H2O", "Na+", "Cl-", "CO2"],
      "temperature": 60.0,
      "phase_name": "GaseousPhase",
      "phase_amount": 1e-6,
      "pressure_bounds": [1.0, 1000.0]
  }'

  --Catalyst.jl--

  $> curl -X POST http://localhost:8083/api/kinetics -H "Content-Type: application/json" -d '{
        "species": ["A", "B", "C"],
        "reactions": [
            {
                "rate_constant": 1.0,
                "reactants": ["A"],
                "products": ["B"]
            },
            {
                "rate_constant": 0.5,
                "reactants": ["B"],
                "products": ["C"]
            }
        ],
        "initial_conditions": {
            "A": 1.0,
            "B": 0.0,
            "C": 0.0
        },
        "tspan": [0, 10]
    }'

  ...

Citations:

  Leal, A.M.M. (2015). Reaktoro: An open-source unified framework for modeling chemically reactive systems. https://reaktoro.org

  @article{CatalystPLOSCompBio2023,
   doi = {10.1371/journal.pcbi.1011530},
   author = {Loman, Torkel E. AND Ma, Yingbo AND Ilin, Vasily AND Gowda, Shashi AND Korsbo, Niklas AND Yewale, Nikhil AND Rackauckas, Chris AND Isaacson, Samuel A.},
   journal = {PLOS Computational Biology},
   publisher = {Public Library of Science},
   title = {Catalyst: Fast and flexible modeling of reaction networks},
   year = {2023},
   month = {10},
   volume = {19},
   url = {https://doi.org/10.1371/journal.pcbi.1011530},
   pages = {1-19},
   number = {10},
  }
