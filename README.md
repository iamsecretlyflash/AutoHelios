# AutoHelios

AutoHelios was developed as a part of my Summer Research Internship at Inria Centre at University of Cotê d'Azur, France. The work was adviced by Prof. Kacper Pluta.

1) Download the HELIOS++ source library from https://github.com/3dgeo-heidelberg/helios. Follow the installation details on their webpage.
2) Put the data generation notebook and utils.py file inside the HELIOS++ folder.
 ![Screenshot 2023-06-19 112220](https://github.com/iamsecretlyflash/AutoHelios/assets/96828194/aff06479-5eea-42ad-86e9-7da1110dd388)

3) Run the data generation notebook. The code will ask you for the path to the sceneparts. The path can be in the following two formats:
   a) Path to the folder containing folders of sceneparts of multiple scenes. Each of the subfolder must contain sceneparts as meshes for the corresponding scene.![4](https://github.com/iamsecretlyflash/AutoHelios/assets/96828194/3ed2027a-cfff-4904-9739-9a102b458881)
   b) Provide path to the folder containing sceneparts of just a single scene (as meshes)![5](https://github.com/iamsecretlyflash/AutoHelios/assets/96828194/58c41ce1-1028-418d-978e-c72050ee7828)
   The scenes will be generated and stored under data/scenes with folder name as the folder name for sceneparts suffixed by '_scenes'![Untitled](https://github.com/iamsecretlyflash/AutoHelios/assets/96828194/e7f82fe4-30ef-4e4c-9876-9092082b5b2e)

   Each of the scene will have a dedicated folder containing scene.xml and links.csv
![Screenshot 2023-06-19 131158](https://github.com/iamsecretlyflash/AutoHelios/assets/96828194/3052405a-aa4e-47ae-a10b-f16a426a30c8)
Scrrenshot from notebook:
![7](https://github.com/iamsecretlyflash/AutoHelios/assets/96828194/99ff859d-1de9-4014-9f84-8e2856d13cc9)

 The links.csv file stores the link between part id and correcpoding part file.

 ![Screenshot 2023-06-19 131417](https://github.com/iamsecretlyflash/AutoHelios/assets/96828194/9fc0ab06-0054-4a82-9d9f-4cdf18ca4c33)
 
4) To generate the survey xmls you need to provide the path to the folder containing scanner specifications (example format : spec_example.txt). The specification file name must match the name of the folder of the scenepart folder for each of the scenes. (site1 must have spec file named site1.txt)
 The path can be provided in two ways. The direct path to the spec file if generating only a single survey, else provide the path to a folder containing all the spec files.
![2](https://github.com/iamsecretlyflash/AutoHelios/assets/96828194/ab2542d6-c3e3-4a73-a36f-238a79f3e11a)
![3](https://github.com/iamsecretlyflash/AutoHelios/assets/96828194/4e22b7fe-5a4f-4053-9a81-1f54d49ce4dd)

5) The survey will be generated and stored under data/survey under a folder named "[specifications_folder_name]_surveys"![efvz](https://github.com/iamsecretlyflash/AutoHelios/assets/96828194/bb3845e0-6a53-4929-a24d-6579ba2988cb)
6) To run the helios scans run the final cell. Multiprocessing should be used based on system specifications.
![10](https://github.com/iamsecretlyflash/AutoHelios/assets/96828194/df10bc68-ef9a-4680-b34b-c1a906a2873a)
7) The outputs will be stored in the outputs folder
   ![11](https://github.com/iamsecretlyflash/AutoHelios/assets/96828194/be21081d-e863-4729-a339-eb11526bffb8)
   Corresponding to each scanner there will be "leg" file. This file contains the information of the points scanned by the scanner. The part id is also stored.

   
