# AutoHelios

Put the data generation script inside the helios-plusplus-win folder
The data generation script inlcudes final_data_generation_for_bim.ipynb and utils.py

Run the notebook file. It will ask you to enter the path to the 3D meshes. This part will generate the scene and store it inside data/scenes

The survey generation part has little bugs, but it can be used by providing the path to the folder containign the scanner specs. 
Make sure to include the important specifications in the spec files
Check ifc2ply.txt file to get an idea of the spec file format

HELIOS++ can be downloaded and built from the source library : https://github.com/3dgeo-heidelberg/helios



@article{heliosPlusPlus,
title = {Virtual laser scanning with HELIOS++: 
A novel take on ray tracing-based simulation 
of topographic full-waveform 3D laser scanning},
journal = {Remote Sensing of Environment},
volume = {269},
year = {2022},
issn = {0034-4257},
doi = {https://doi.org/10.1016/j.rse.2021.112772},
author = {Lukas Winiwarter and Alberto Manuel {Esmorís Pena}
and Hannah Weiser and Katharina Anders 
and Jorge {Martínez Sánchez} and Mark Searle and Bernhard Höfle}
}
