# ICAIL 2023




# The simulation #

Simulation Classes, for implementing agents and such in the simulation. Read MESA documentation for more information about the classes and functions.  Main model: GroteMarkt.py. CreateMap.py creates the simulation environment. Reporters.py creates the reporters.

Runtime Instructions for seeing the simulation

> install requirements
> python3 Sim_Viz.py

Or run:
> python3 main.py

For generating the frequency data for events in the simulation
The data generated is stored in the file "GroteMarktOutcomes.csv"

Note: the data used in the experiment described in the paper can be found at "analysePosteriors/GroteMarktPrivate.csv" (10.000 runs)

# The Bayesian Networks #

The BNs used in the experiment can be found at BayesianNetworks.
Key:
GD -> algorithmic/constrained, GG -> algorithmic/unit
MD -> manual/constrained, MD -> manual/unit

Code for generating the unit BNs from data is found in analyinsPosteriors/CreateBayesianNetworks.R
For the constrained BNs, the original BN was rounded to the intervals decribed in the paper.


# Analysing Posteriors #
The Bayesian Networks are tested for each evidence valuation. This is done in "analysePosteriors/generatingPosteriors.py". The posteriors found for the papers are "Posteriors.csv" for the manual networks, and "PosteriorsGenerated.csv" for the algoritmic netowrks.

Analyse the posteriors by running Analysis.R. When you run the whole file you should get the same plot as in the paper.
