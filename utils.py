import os
import xml.etree.ElementTree as ET
from yattag import Doc, indent
import numpy as np
from xml.dom import minidom

class XMLScene:
    
    def __init__(self,path):
        # Path : str : path of the folder where all the .obj files to be included in the scene are kept.
        # The id given to the scene will be the name of the folder in lowercase suffixed by '_scene'
        # the name attribute of the scene will be same as id
        # The ids assigned to each part will be starting from 0 and they will be alooted lexicographically
        # For the HELIOS++ library to work with this XML, the 3D files must be in .PLY format
        # Output Directory can be assigned during function call. If none then the ouput XML will be saved in the local directory

        if not os.path.exists(path):
            raise Exception("Input path not found")

        self.files_path = path
        self.result = self.generate_xml()


    def generate_xml(self):

        files = os.listdir(self.files_path) # object paths
        file_links = []
        scene_name = (os.path.basename(self.files_path).lower()+'_scene').replace(' ','_')
        
        doc, tag, text = Doc().tagtext()

        with tag('document'):
            with tag('scene', id = scene_name, name =scene_name):
                for i,file in enumerate(files):
                    file_links.append((i,file))
                    with tag('part', id = str(i)):
                        with tag('filter', type = 'objloader'):
                            doc.stag('param',type = 'string', key = 'filepath', value = os.path.join(self.files_path,file))


        result = indent(
            doc.getvalue(),
            indentation = ' '*4,
            newline = '\n'
        )

        return result,file_links
    
def xml_survey(parsed,survey_name, scene_path):
    root = minidom.Document()
    xml = root.createElement('document')
    root.appendChild(xml)

    surveyAttrib = root.createElement('survey')
    surveyAttrib.setAttribute('name',survey_name)
    surveyAttrib.setAttribute('scene',str(scene_path))
    surveyAttrib.setAttribute('platform',"data/platforms.xml#tripod")
    surveyAttrib.setAttribute('scanner',"data/scanners_tls.xml#"+parsed[0])
    xml.appendChild(surveyAttrib)
    
    legs = parsed[1]
    for leg in legs:
        leg_elem = root.createElement('leg')
        platform = root.createElement('platformSettings')
        platform.setAttribute('x',str(leg['x']))
        platform.setAttribute('y',str(leg['y']))
        platform.setAttribute('z',str(leg['z']))
        platform.setAttribute("onGround","true")

        scanner = root.createElement("scannerSettings")
        x,y,z = leg.pop('x'), leg.pop('y'), leg.pop('z')
        for name,attr in leg.items():
            scanner.setAttribute(str(name),str(attr))
              
        leg_elem.appendChild(platform)
        leg_elem.appendChild(scanner)
        surveyAttrib.appendChild(leg_elem)


    return root.toprettyxml(indent='\t')
    
def parse_spec(spec_path):
    with open(spec_path,'r') as f:
         lines = f.readlines()
    scanner_id = lines[0][1:-2]
    legs = []
    for id,leg in enumerate(lines[1:]):
        spec_list = leg.split('>')[:-1]
        spec_dict = {}
        for spec in spec_list:
            temp_spec = spec.strip()[1:]
            temp_spec = temp_spec.split('=')
            spec_dict[temp_spec[0].strip()] = eval(temp_spec[1])
        legs.append(spec_dict)
    return scanner_id,legs
    
def find_avg_cordinates(path_to_objs):
    points = []

    files = os.listdir(path_to_objs)
    for file in files:
        path = os.path.join(path_to_objs,file)
        with open(path,'r') as f:
            lines = f.readlines()
        for line in lines:
            if line[0] == 'v':
                points.append(list(map(float,line.split()[1:])))
    points = np.array(points)
    return np.mean(points,axis = 0)

def floor_and_avg(coords):
    x = [i[0] for i in coords]
    y = [i[1] for i in coords]
    z = [i[2] for i in coords]
    x_mean = np.mean(x); x_std = np.std(x);x_clean = [i for i in x if x_mean-x_std<=i<=x_mean+x_std]
    y_mean = np.mean(x); y_std = np.std(x);y_clean = [i for i in x if y_mean-y_std<=i<=y_mean+y_std] 
    z_mean = np.mean(x); z_std = np.std(x);z_clean = [i for i in x if z_mean-z_std<=i<=z_mean+z_std] 
    lx = max(x_clean)-min(x_clean)
    ly = max(y_clean) - min(y_clean)
    lz = max(z_clean) - min(z_clean)

def get_scanner_details():
        tls_scanner_tree = ET.parse('data/scanners_tls.xml')
        print('Specifications for the terestrial scanners :')
        for scanner in tls_scanner_tree.getroot():
              scanner_attribs = scanner.attrib
              name = scanner_attribs['name']
              print(f'Name : {name}')
              attrib_values = scanner_attribs.items()
              for key,value in attrib_values:

                        print(f'       {key} : {value}')
        als_scanner_tree = ET.parse('data/scanners_als.xml')
        print('\nSpecifications for the aerial scanners :')
        for scanner in als_scanner_tree.getroot():
              scanner_attribs = scanner.attrib
              name = scanner_attribs['name']
              print(f'Name : {name}')
              attrib_values = scanner_attribs.items()
              for key,value in attrib_values:

                        print(f'       {key} : {value}')
        