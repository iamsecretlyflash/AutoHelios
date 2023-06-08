# AutoHelios

Put the data generation script inside the helios-plusplus-win folder
The data generation script inlcudes final_data_generation_for_bim.ipynb and utils.py

Run the notebook file. It will ask you to enter the path to the 3D meshes. This part will generate the scene and store it inside data/scenes

The survey generation part has little bugs, but it can be used by providing the path to the folder containign the scanner specs. 
Make sure to include the important specifications in the spec files

HELIOS++ can be downloaded and built from the source library : https://github.com/3dgeo-heidelberg/helios
