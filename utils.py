import os
import xml.etree.ElementTree as ET
from yattag import Doc, indent
import numpy as np
import pandas as pd
from xml.dom import minidom
from scipy.spatial import KDTree
class XMLScene:
    
    def __init__(self,path,vert_axis = 'z',lin_perterb_max = 0,rot_perterb_max = 0,lin_perterb_prob = (0.1,0.1,0.1),rot_perterb_prob = (0.1,0.1,0.1)):
        # Path : str : path of the folder where all the .obj files to be included in the scene are kept.
        # The id given to the scene will be the name of the folder in lowercase suffixed by '_scene'
        # the name attribute of the scene will be same as id
        # The ids assigned to each part will be starting from 0 and they will be alooted lexicographically
        # For the HELIOS++ library to work with this XML, the 3D files must be in .PLY format
        # Output Directory can be assigned during function call. If none then the ouput XML will be saved in the local directory

        if not os.path.exists(path):
            raise Exception("Input path not found")

        self.files_path = path
        self.vert_axis = vert_axis
        self.lin_perterb_max = lin_perterb_max
        self.rot_perterb_max = rot_perterb_max
        self.lin_perterb_prob = lin_perterb_prob
        self.rot_perterb_prob = rot_perterb_prob
        self.result = self.generate_xml()


    def generate_xml(self):

        files = os.listdir(self.files_path) # object paths
        file_links = {'id':[],'file':[],'file_path':[]}
        scene_name = (os.path.basename(self.files_path).lower()+'_scene').replace(' ','_')
        
        doc, tag, text = Doc().tagtext()

        with tag('document'):
            with tag('scene', id = scene_name, name =scene_name):
                for i,file in enumerate(files):
                    file_links['id'].append(i)
                    file_links['file'].append(file)
                    file_links['file_path'].append(os.path.join(self.files_path,file))
                    with tag('part', id = str(i)):
                        with tag('filter', type = 'objloader'):
                            doc.stag('param',type = 'string', key = 'filepath', value = os.path.join(self.files_path,file))
                        if self.lin_perterb_max != 0:
                            val = lambda : np.random.uniform(-self.lin_perterb_max,self.lin_perterb_max)
                            px,py,pz = px,py,pz = val(),val(),val()
                            if np.random.random() >self.lin_perterb_prob[0] or self.vert_axis == 'x': px = 0
                            if np.random.random() >self.lin_perterb_prob[1] or self.vert_axis == 'y': py = 0
                            if np.random.random() >self.lin_perterb_prob[2] or self.vert_axis == 'z': pz = 0
                            with tag('filter', type = 'translate'):
                                doc.stag('param',type = 'vec3', key = 'offset', value = str(px)+";"+str(py)+";"+str(pz))
                        if self.rot_perterb_max != 0:
                            val = lambda : np.random.uniform(-self.rot_perterb_max,self.rot_perterb_max)
                            px,py,pz = val(),val(),val()
                            if np.random.random() >self.rot_perterb_prob[0]: px = 0
                            if np.random.random() >self.rot_perterb_prob[1]: py = 0
                            if np.random.random() >self.rot_perterb_prob[2]: pz = 0
                            with tag('filter', type = 'rotation'):
                                with tag('param', type = 'rotation',key = "rotation"):
                                    doc.stag("rot", axis ="x", angle_deg = str(px))
                                with tag('param', type = 'rotation',key = "rotation"):
                                    doc.stag("rot", axis ="y", angle_deg = str(py))
                                with tag('param', type = 'rotation',key = "rotation"):
                                    doc.stag("rot", axis ="z", angle_deg = str(pz))
                        
        result = indent(
            doc.getvalue(),
            indentation = ' '*4,
            newline = '\n'
        )

        return result,pd.DataFrame(file_links)
    
    def perturbation(self,abs_max = 1):
         while True:
              num = np.random.standard_normal()
              if abs(num) <abs_max:
                   return num
    
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

def merge_output_xyz(folder_path,save_path = None):
    merged = []
    for file in os.listdir(folder_path):
         if os.path.splitext(file)[1] == '.xyz':
              with open(os.path.join(folder_path,file),'r') as f:
                   merged.extend(f.readlines())
    
    if save_path is not None:
         if os.path.splitext(save_path)[1] != '.xyz':
              save_path = os.path.splitext(save_path)[0]+'.xyz'
         with open(save_path,'w') as f:
              f.writelines(merged)
    return merged
    
def add_texture_to_point_cloud(file_path):
    #default value of colums to keep x,y,z co-ord and part id of the default helios output
    file = None
    if type(file_path )== 'str':
        with open(file_path,'r') as f:
            file = f.readlines()
        if os.path.splitext(file_path)[1] == '.ply':
            end_header = 0
            for line in file:
                end_header+=1
                if line == 'end_header\n':break
                
            file = file[end_header:]
    else:
         file = file_path
    points_with_id = np.array([list(map(float,i.split())) for i in file],dtype = np.double)
    points_tree = KDTree(points_with_id[:,:3])
    log = []
    points_queried = np.zeros(len(points_with_id))
    for i in range(len(points_with_id)):
        if np.random.uniform(0,1)>0.8 and points_queried[i] == 0:
            point = points_with_id[:,:3][i]
            log.append(point)
            three_points = points_with_id[points_tree.query(point,3)[1]][:,:3]
            cross = np.cross(three_points[0]-three_points[1],three_points[0]-three_points[2])
            cross = cross/np.linalg.norm(cross)
            points_ball = points_tree.query_ball_point(point,0.1)
            update_coord = np.argmax(abs(cross))
            updates = sorted(np.random.normal(0,0.01,len(points_ball)).tolist(),reverse = True)
            temp = points_with_id[points_ball][:,update_coord]+np.array(updates)
            for pnt in range(len(points_ball)):
                points_with_id[points_ball[pnt]][update_coord] = temp[pnt]
            points_queried[points_ball] = 1
    
    return points_with_id,log

        
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
        