# SAT SOLVER #

Repository contains files for Logic in computer science homework, which was to implement a SAT solver.

## Authors
* Ana Borovac
* Katarina Černe

## How to run the code 
1. Prepare test file/s in [dimacs format](http://www.satcompetition.org/2009/format-benchmarks2009.html) - "InputFile.txt". There are some examples in folder [Primeri](Primeri).
2. There are two ways of running the code:

	* Run file [sat-solver1.py](sat-solver1.py) and call function `main("InputFile.txt","OutputFile.txt")`.
	* It can be run from command line; `python sat-solver1.py "InputFile.txt" "OutputFile.txt"`.
	
The code generates an output file "Outputfile.txt" which contains variables that should be set to True for a valuation to be satisfying.
If the solver doesn't find a satisfying valuation, the output file will contain only 0.

## Contents
* `sat-solver1.py` contains the main functions for solving a SAT problem
* `FormatSolution.py` contains some functions for converting problems like sudoku and k-colouring of a graph to dimasc format
* the folder `Primeri` contains some files in dimacs format that were used for testing the SAT solver as well as the outputs the SAT solver generated and some official solutions to those problems
* the folder `Viri` contains some literature
* `sat-solver2.py` contains an alternative implementation of a SAT solver which is not yet complete