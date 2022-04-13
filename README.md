# gostshyp-542-benchmark
evaluate gostshyp implementation as in Q-Chem 5.4.2
To perform the benchmark you will need two installed versions of Q-Chem, Q-Chem 5.4.2 and Q-Chem  5.4.

Steps to perform the benchmark:
1. Download this repo to your local machine.
2. Set the varaibles QCold and QCnew to the install paths of the corresponding Q-Chem versions in the benchmark_gostshyp-542.sh script.
3. Perform the bencmark by running (You can add/remove molecules to the benchmarkset by adding/removing files to the geoms folder)
benchmark_gostshyp-542.sh geoms
4. run evaluate_benchmark.py to evaluate and plot data from the benchmark. (To evaluate memory you need to manipulate the source code to print the memory usage, thus memory evaluation is turned of by default.)
