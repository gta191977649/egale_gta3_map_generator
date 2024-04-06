import os
import shutil

from dymatic_object import getObjectDat
from quaternion import *
from model.sa_model import *
USE_SA_PROP = True
GAME = "VC"
MAP_NAME = "LCS"
AUTHOR = "NURUPO"
DESCRIPTION = "LCS CONVERTED BY NURUPO"
# Path to your gta.dat file
dat_file_path = '/Users/nurupo/Desktop/dev/vcs_map/'
output_resource_dir = '/Users/nurupo/Desktop/dev/vcs_map/vcs'

zones = []
file_lists = {
    "defs":[],
    "maps":[],
    "imgs":[],
    "files":[],
}

exits_img = {
    "dffs":[]
}

objects_dat = []
def add_exsit_img(t,file):
    if file not in exits_img[t]:
        exits_img[t].append(file)
def add_file_lists(t,file):
    if file not in file_lists[t]:
        file_lists[t].append(file)
def copy_model(zonename,modelName, txdName):
    #print(f"Processing Copy Model Zone: {zonename} ...")

    path_dff = os.path.join(dat_file_path, "img", f"{modelName}.dff")
    path_txd = os.path.join(dat_file_path, "img", f"{txdName}.txd")
    path_col = os.path.join(dat_file_path, "img", f"{modelName}.col")

    dff_exist = os.path.exists(path_dff)
    txd_exist = os.path.exists(path_txd)
    col_exist = os.path.exists(path_col)
    if not dff_exist:
        print(f"DFF file for {modelName}.dff does not exist.")

    if not txd_exist:
        print(f"TXD file for {txdName}.txd does not exist.")

    if not col_exist:
        print(f"COL file for {modelName}.col does not exist.")


    # copy the files to zone directory
    if dff_exist and txd_exist and col_exist:
        # Directories for dff, txd, and col in the output resource directory
        dff_dir = os.path.join(output_resource_dir,"zones",zonename, "dff")
        txd_dir = os.path.join(output_resource_dir,"zones",zonename, "txd")
        col_dir = os.path.join(output_resource_dir,"zones",zonename, "col")

        # Create directories if they don't exist
        os.makedirs(dff_dir, exist_ok=True)
        os.makedirs(txd_dir, exist_ok=True)
        os.makedirs(col_dir, exist_ok=True)

        # Copy the files
        shutil.copy2(path_dff, dff_dir)
        shutil.copy2(path_txd, txd_dir)
        shutil.copy2(path_col, col_dir)
        print(f"Files copied for {modelName}.dff,{txdName}.txd, {modelName}.col, zone: {zonename}")
        # append to file list cache
        add_file_lists("imgs","zones/{}/dff/{}.dff".format(zonename,modelName))
        add_file_lists("imgs","zones/{}/txd/{}.txd".format(zonename,txdName))
        add_file_lists("imgs","zones/{}/col/{}.col".format(zonename,modelName))

        add_exsit_img("dffs", modelName.lower())
        return True

    return False
def read_gta_dat(dat_file_path):
    ide_files = []
    ipl_files = []
    with open("{}/gta.dat".format(dat_file_path), 'r', newline='\n') as file:
        for line in file:
            if line.startswith('IDE'):
                ide_files.append(line.split()[1].lower())
            elif line.startswith('IPL'):
                ipl_files.append(line.split()[1].lower())

    return ide_files, ipl_files
def create_def(output_resource_dir, model_data):
    zonename = model_data['zonename']
    # Define the path for the definition file
    def_file_path = os.path.join(output_resource_dir,"zones" ,zonename, f"{zonename}.definition")

    # Check if 'timeIn' and 'timeOut' flags are present in the flags
    timeIn = None
    timeOut = None

    # Check if breakable
    breakable = "false"
    if model_data["modelName"].lower() in objects_dat: breakable = "true"

    if "timeOn" in model_data['flags'] or "timeOff" in model_data['flags']:
        time_flags = model_data['flags'].split()  # Assuming flags are space-separated
        for flag in time_flags:
            if flag.startswith("timeOn"):
                timeIn = flag.split('=')[1]
            elif flag.startswith("timeOff"):
                timeOut = flag.split('=')[1]

    # Create the zonename directory if it doesn't exist
    os.makedirs(os.path.dirname(def_file_path), exist_ok=True)

    # Write to the definition file
    with open(def_file_path, 'a', newline='\n') as def_file:
        if USE_SA_PROP and getSAModelID(model_data["modelName"]):
            def_line = f'\t<definition id="{model_data["modelName"]}" zone="{zonename}" default=\"true\"'
        else:
            def_line = f'\t<definition id="{model_data["modelName"]}" zone="{zonename}" dff="{model_data["modelName"]}" col="{model_data["modelName"]}" txd="{model_data["txdName"]}"'

        if timeIn:
            def_line += f' timeIn="{timeIn}"'
        if timeOut:
            def_line += f' timeOut="{timeOut}"'
        def_line += f' lod="{model_data["lod"]}" lodDistance="{model_data["drawDistance"]}" flags="{model_data["flags"]}" doubleSided="true" breakable="{breakable}"></definition>\n'

        # Check if the file is newly created or not, to add <zoneDefinitions> tag
        if os.path.getsize(def_file_path) == len(def_line):
            def_file.seek(0)
            def_file.write('<zoneDefinitions>\n')
            def_file.write(def_line)
        else:
            def_file.write(def_line)


def initialize_definition_file(output_resource_dir, zonename):
    def_file_path = os.path.join(output_resource_dir,"zones" , zonename, f"{zonename}.definition")
    # Create the directory for the definition file if it doesn't exist
    os.makedirs(os.path.dirname(def_file_path), exist_ok=True)

    # Create file with opening tag if it doesn't exist
    if not os.path.exists(def_file_path):
        with open(def_file_path, 'w', newline='\n') as def_file:
            def_file.write('<zoneDefinitions>\n')
def close_definition_file(output_resource_dir, zonename):
    def_file_path = os.path.join(output_resource_dir,"zones" , zonename, f"{zonename}.definition")

    # Append the closing tag only if the file exists
    if os.path.exists(def_file_path):
        with open(def_file_path, 'a', newline='\n') as def_file:
            def_file.write('</zoneDefinitions>\n')

    add_file_lists("defs","zones/{}/{}.definition".format(zonename,zonename))
def create_map(output_resource_dir, map_data):
    zonename = map_data['zonename']


    map_file_path = os.path.join(output_resource_dir, "zones" ,zonename, f"{zonename}.map")

    # Convert quaternion to Euler angles if needed
    if 'rotW' in map_data:                                                                                                                                                                                                                              
        rotX, rotY, rotZ = from_quaternion( float(map_data['rotX']), float(map_data['rotY']), float(map_data['rotZ']),float(map_data['rotW']))
    else:
        rotX, rotY, rotZ = map_data['rotX'], map_data['rotY'], map_data['rotZ']

    # Create the zonename directory if it doesn't exist
    os.makedirs(os.path.dirname(map_file_path), exist_ok=True)

    # Append each object to the map file
    with open(map_file_path, 'a', newline='\n') as map_file:
        if USE_SA_PROP and getSAModelID(map_data["model"]):
            object_line = f'\t<object id="{map_data["model"]}" model="{getSAModelID(map_data["model"])}" posX="{map_data["posX"]}" posY="{map_data["posY"]}" posZ="{map_data["posZ"]}" rotX="{rotX}" rotY="{rotY}" rotZ="{rotZ}" interior="{map_data.get("interior", "0")}" dimension="{map_data.get("dimension", "-1")}"></object>\n'
        else:
            object_line = f'\t<object id="{map_data["model"]}" model="8585" posX="{map_data["posX"]}" posY="{map_data["posY"]}" posZ="{map_data["posZ"]}" rotX="{rotX}" rotY="{rotY}" rotZ="{rotZ}" interior="{map_data.get("interior", "0")}" dimension="{map_data.get("dimension", "-1")}"></object>\n'
        map_file.write(object_line)


def initialize_map_file(output_resource_dir, zonename):
    map_file_path = os.path.join(output_resource_dir,"zones" , zonename, f"{zonename}.map")
    os.makedirs(os.path.dirname(map_file_path), exist_ok=True)

    # Open and write the opening tag only if the file doesn't exist
    if not os.path.exists(map_file_path):
        with open(map_file_path, 'w', newline='\n') as map_file:
            map_file.write('<map>\n')

def close_map_file(output_resource_dir, zonename):
    map_file_path = os.path.join(output_resource_dir,"zones" ,zonename, f"{zonename}.map")
    if os.path.exists(map_file_path):
        with open(map_file_path, 'a', newline='\n') as map_file:
            map_file.write('</map>\n')
    file_lists["maps"].append(f"zones/{zonename}/{zonename}.map")
def read_ide(file, game="VC"):
    with open(file, 'r', newline='\n') as f:
        zonename, _ = os.path.splitext(os.path.basename(f.name))
        initialize_definition_file(output_resource_dir, zonename)
        process_lines = False

        if zonename not in zones:
            zones.append(zonename)

        for line in f:
            line = line.strip()
            if line == 'objs':
                process_lines = True
                continue
            elif line == 'end':
                process_lines = False
                close_definition_file(output_resource_dir, zonename)
                break

            if process_lines and line and not line.startswith('#'):
                components = line.split(',')

                # Game version-specific parsing
                if game in ["III", "VC", "LCS"]:
                    if len(components) in [6, 7, 8]:  # Types 1, 2, 3
                        model_data = {
                            'zonename': zonename,
                            'id': components[0].strip(),
                            'modelName': components[1].strip(),
                            'txdName': components[2].strip(),
                            'meshCount': components[3].strip(),
                            'drawDistance': components[-2].strip(),
                            'flags': components[-1].strip(),
                            'lod': 'true' if components[1].strip().startswith("LOD") else 'nil',
                        }
                        # only create the defs that contains exist model file
                        if copy_model(zonename, model_data['modelName'], model_data['txdName']):
                            create_def(output_resource_dir, model_data)
                if game in ["SA"]:
                    if len(components) == 5:  # Types 1, 2, 3
                        model_data = {
                            'zonename': zonename,
                            'id': components[0].strip(),
                            'modelName': components[1].strip(),
                            'txdName': components[2].strip(),
                            'meshCount': 'nil',
                            'drawDistance': components[-2].strip(),
                            'flags': components[-1].strip(),
                            'lod': 'true' if components[1].strip().startswith("LOD") else 'nil',
                        }
                        # only create the defs that contains exist model file
                        if copy_model(zonename, model_data['modelName'], model_data['txdName']):
                            create_def(output_resource_dir, model_data)



def read_ipl(file, game="VC"):
    with open(file, 'r', newline='\n') as f:
        zonename, _ = os.path.splitext(os.path.basename(f.name))
        initialize_map_file(output_resource_dir, zonename)
        process_lines = False
        if zonename not in zones:
            zones.append(zonename)

        for line in f:
            line = line.strip()
            if line == 'inst':
                process_lines = True
                continue
            elif line == 'end':
                process_lines = False
                continue

            if process_lines and line and not line.startswith('#'):
                components = line.split(',')

                if game == "III":
                    # GTA III format
                    map_data = {
                        'zonename': zonename,
                        'id': components[0].strip(),
                        'model': components[1].strip(),
                        'posX': components[2].strip(),
                        'posY': components[3].strip(),
                        'posZ': components[4].strip(),
                        'rotX': components[8].strip(),
                        'rotY': components[9].strip(),
                        'rotZ': components[10].strip(),
                        'rotW': components[11].strip() if len(components) > 11 else '1',
                        'dimension': '-1'
                    }
                elif game == "VC":
                    # Vice City format
                    map_data = {
                        'zonename': zonename,
                        'id': components[0].strip(),
                        'model': components[1].strip(),
                        'interior': components[2].strip(),
                        'posX': components[3].strip(),
                        'posY': components[4].strip(),
                        'posZ': components[5].strip(),
                        'rotX': components[9].strip(),
                        'rotY': components[10].strip(),
                        'rotZ': components[11].strip(),
                        'rotW': components[12].strip() if len(components) > 9 else '1',
                        'dimension': '-1'
                    }
                elif game == "SA":
                    # San Andreas format
                    map_data = {
                        'zonename': zonename,
                        'id': components[0].strip(),
                        'model': components[1].strip(),
                        'interior': components[2].strip(),
                        'posX': components[3].strip(),
                        'posY': components[4].strip(),
                        'posZ': components[5].strip(),
                        'rotX': components[6].strip(),
                        'rotY': components[7].strip(),
                        'rotZ': components[8].strip(),
                        'rotW': components[9].strip(),
                        'lod': components[10].strip() if len(components) > 9 else 'nil',
                        'dimension': '-1'
                    }

                if USE_SA_PROP and getSAModelID(map_data["model"].lower()):
                    print(f"{map_data["model"]} is skipped because it is a sa dynamic prop")
                    create_map(output_resource_dir, map_data)
                if map_data["model"].lower() in exits_img["dffs"]:
                    create_map(output_resource_dir, map_data)
        close_map_file(output_resource_dir, zonename)

def read_ide_ipl_files(files, directory):
    for file in files:
        # Split the file name and get the extension
        file_name, file_extension = os.path.splitext(file)
        file_extension = file_extension.lower()

        file = file.replace('\\', '/')
        path = os.path.join(directory, file)

        # Check if the file is an IDE or IPL file
        if file_extension == '.ide':
            file_type = "IDE"
            read_ide(path, "SA")
        elif file_extension == '.ipl':
            file_type = "IPL"
            read_ipl(path, "SA")
        else:
            print(f"Unknown file type for {file}")
            continue
        print(f"Reading {file_type} file: {file}")

def generate_zonefile():
    # Write unique zone names to eagleZones.txt
    eagle_zones_path = os.path.join(output_resource_dir, "eagleZones.txt")
    with open(eagle_zones_path, 'w', newline='\n') as file:
        for zone in zones:
            file.write(zone + '\n')

    file_lists["files"].append(f"eagleZones.txt")

def generate_map():

    # Read gta.dat file
    ide_files, ipl_files = read_gta_dat(dat_file_path)

    # Read and display the contents of .ide and .ipl files
    read_ide_ipl_files(ide_files,dat_file_path)
    read_ide_ipl_files(ipl_files,dat_file_path)
    generate_zonefile()

    # You might want to add additional code to handle DFF, TXD, and COL files in the img folder
def generate_meta_xml():
    output = "<meta>\n"
    output += f"\t<info type=\"scrip\" name=\"{MAP_NAME}\" author=\"{AUTHOR}\" description=\"{DESCRIPTION}\" version=\"1\" eagleLoad=\"1\" />\n"
    # load maps
    for map in file_lists["maps"]:
        output += f"\t<map src=\"{map}\" type=\"server\" />\n"
    # load defs
    for df in file_lists["defs"]:
        output += f"\t<file src=\"{df}\" type=\"client\" />\n"

    # load imgs
    for img in file_lists["imgs"]:
        output += f"\t<file src=\"{img}\" type=\"client\" />\n"
        
    # finally eagleZones.txt
    for file in file_lists["files"]:
        output += f"\t<file src=\"{file}\" type=\"client\" />\n"
    # close tag
    output += "</meta>"
    # write file
    eagle_zones_path = os.path.join(output_resource_dir,"meta.xml")
    with open(eagle_zones_path, 'w', newline='\n') as file:
         file.write(output)

if __name__ == '__main__':
    # handle with object.dat for dynamic objects
    # obj_dat = getObjectDat("/Users/nurupo/Desktop/dev/vcs_map/object.dat")
    # for obj in obj_dat:
    #     objects_dat.append(obj["modelName"].lower())

    generate_map()
    generate_meta_xml()
