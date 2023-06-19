# AutoHelios

1) Download the HELIOS++ source library from https://github.com/3dgeo-heidelberg/helios. Follow the installation details on their webpage.
2) Put the data generation notebook and utils.py file inside the HELIOS++ folder.
 ![Screenshot 2023-06-19 112220](https://github.com/iamsecretlyflash/AutoHelios/assets/96828194/aff06479-5eea-42ad-86e9-7da1110dd388)

3) Run the data generation notebook. The code will ask you for the path to the sceneparts. The path can be in the following two formats:
   a) Path to the folder containing folders of sceneparts of multiple scenes. Each of the subfolder must contain sceneparts as meshes for the corresponding scene.![4](https://github.com/iamsecretlyflash/AutoHelios/assets/96828194/3ed2027a-cfff-4904-9739-9a102b458881)
   b) Provide path to the folder containing sceneparts of just a single scene (as meshes)![5](https://github.com/iamsecretlyflash/AutoHelios/assets/96828194/58c41ce1-1028-418d-978e-c72050ee7828)
   The scenes will be generated and stored under data/scenes with folder name as the folder name for sceneparts suffixed by '_scenes'![Untitled](https://github.com/iamsecretlyflash/AutoHelios/assets/96828194/e7f82fe4-30ef-4e4c-9876-9092082b5b2e)

   Each of the scene will have a dedicated folder containing scene.xml and links.csv
![Screenshot 2023-06-19 131158](https://github.com/iamsecretlyflash/AutoHelios/assets/96828194/3052405a-aa4e-47ae-a10b-f16a426a30c8)

Run the notebook file. It will ask you to enter the path to the 3D meshes. This part will generate the scene and store it inside data/scenes

The survey generation part has little bugs, but it can be used by providing the path to the folder containign the scanner specs. 
Make sure to include the important specifications in the spec files
Check ifc2ply.txt file to get an idea of the spec file format

HELIOS++ can be downloaded and built from the source library : https://github.com/3dgeo-heidelberg/helios

