# analysis-scripts
A selection of analysis scripts for ORCA and Q-Chem

1. 2d_scan.py takes a csv file containing x coordinates, y coordinates, and energies in Hartrees, and creates a contour plot
2. aimdanalysis.py is an analysis script for Q-Chem AIMD calculations
3. run_multicas.py is used to generate diatomic CAS-CI input files for the preprint https://doi.org/10.26434/chemrxiv-2023-1lprg
4. run_polyatomic_scan.py is used to generate polyatomic CAS-CI input files for the preprint https://doi.org/10.26434/chemrxiv-2023-1lprg
5. trj_analysis.py takes ORCA AIMD trj files and creates step vs distance and violin plots according to user-specified atomic pairs
6. mof_heatmap.py takes a numpy array and creates a heatmap showing likelihood of HAT with neighboring amines
7. intramolecular_hat.zip contains graphviz.ipynb, a script that can be run in a Jupyter Notebook using the data contained within the zip folder to generate reaction networks for intramolecular hydrogen atom transfer
