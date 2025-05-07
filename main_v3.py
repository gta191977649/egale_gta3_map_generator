# This is for eagleloader v3
import os
from model.defination import *
from model.placement import *
from helper import normalize_path
import shutil

map_data = {
	"defination_files": {},
	"zone": {}, # stores for all related zones
}

def read_gta_dat(dat_file_path):
	ide_files = []
	ipl_files = []

	gta_dat = os.path.join(dat_file_path, "gta.dat")
	if not os.path.exists(gta_dat):
		raise FileNotFoundError(f"{gta_dat} not found")

	with open(gta_dat, 'r', newline='\n') as file:
		for line in file:
			if not (line.startswith('IDE') or line.startswith('IPL')):
				continue

			rel_path = line.split()[1].lower()
			full_path = os.path.normpath(os.path.join(dat_file_path, rel_path)).replace('\\', '/').lower()

			if line.startswith('IDE'):  # Read IDE
				if os.path.exists(full_path):
					ide_files.append(full_path)
				else:
					print(f"{full_path} not found")

			if line.startswith('IPL'):  # Read IPL
				if os.path.exists(full_path):
					ipl_files.append(full_path)
				else:
					print(f"{full_path} not found")

	return ide_files, ipl_files


def process_section(path):
	items = {}
	current_section = None
	with open(path, 'r', newline='\n') as f:
		for line in f:
			text = line.strip()
			if not text:
				continue
			key = text.lower()
			if key == 'end':
				current_section = None
				continue
			if current_section is None:
				current_section = key
				items[current_section] = []
				continue
			if ',' in text:
				parts = [p.strip() for p in text.split(',')]
				items[current_section].append(parts)
			else:
				items[current_section].append(text)
	return items

def copy_model(path, modelName, txdName, colName):
    path_dff = normalize_path(os.path.join(path,  f"{modelName}.dff"))
    path_txd = normalize_path(os.path.join(path,  f"{txdName}.txd"))
    path_col = normalize_path(os.path.join(path,  f"{colName}.col"))

    if not os.path.exists(path_dff):
        print(f"DFF file for {path_dff} does not exist.")
        return False
    if not os.path.exists(path_txd):
        print(f"TXD file for {path_txd} does not exist.")
        return False
    if not os.path.exists(path_col):
        print(f"COL file for {path_col} does not exist.")
        return False

    dff_dir = os.path.join(output_dir, "imgs", "dff")
    txd_dir = os.path.join(output_dir, "imgs", "txd")
    col_dir = os.path.join(output_dir, "imgs", "col")

    # if already copied, skip
    if (os.path.exists(os.path.join(dff_dir, f"{modelName}.dff")) and
        os.path.exists(os.path.join(txd_dir, f"{txdName}.txd")) and
        os.path.exists(os.path.join(col_dir, f"{colName}.col"))):
        return True

    os.makedirs(dff_dir, exist_ok=True)
    os.makedirs(txd_dir, exist_ok=True)
    os.makedirs(col_dir, exist_ok=True)

    shutil.copy2(path_dff, dff_dir)
    shutil.copy2(path_txd, txd_dir)
    shutil.copy2(path_col, col_dir)
    print(f"Files copied for {modelName}.dff, {txdName}.txd, {colName}.col")
    return True

def load_ides(path, game="SA"):
	defination_files = []
	items = process_section(path)
	# Get IDE Name from path
	zone = os.path.splitext(os.path.basename(path))[0]
	for section in items:
		if section == "objs":
			for obj in items[section]:
				# id =int(obj[0])
				id = obj[1].strip().lower() # use model name for id instead ...
				model = obj[1].strip().lower()
				txd = obj[2].strip().lower()
				draw_dist = int(obj[3])
				flag = int(obj[4])

				#Only append model with exits
				if copy_model(img_folder,modelName=model,txdName=txd,colName=model):
					ide = Defination(zone=zone, id=id, dff=model, col=model, txd=txd, lodDistance=draw_dist, flag=flag)
					defination_files.append(ide)
		if section == "tobjs":
			print("Not implemented tobj")
		if section == "2dfx":
			print("Not implemented 2dfx")

	return defination_files


def load_ipls(path, game="SA"):
	placements_files = []
	items = process_section(path)
	# Get IDE Name from path
	zone = os.path.splitext(os.path.basename(path))[0]
	for section in items:
		# ID, ModelName, Interior, PosX, PosY, PosZ, RotX, RotY, RotZ, RotW, LOD (SA FORMAT)
		if section == "inst":
			for obj in items[section]:
				if game == "SA":
					# id =int(obj[0])
					id = obj[1].strip().lower()  # use model name for id instead ...
					model = obj[1].strip().lower()
					interior = int(obj[2])
					x = float(obj[3])
					y = float(obj[4])
					z = float(obj[5])
					rx = float(obj[6])
					ry = float(obj[7])
					rz = float(obj[8])
					rw = float(obj[9])
					lod = int(obj[10]) # Todo. For SA, need to search for the co-responding LodModel Name

					if id in map_data["defination_files"]:
						defination = map_data["defination_files"][id]
						ipl = None
						if defination.lodDistance > 299:  # if lod is not set but drawdist is > 299, set itself
							ipl = Building(id=id, x=x, y=y, z=z, rx=rx, ry=ry, rz=rz ,rw=rw)
						else:
							ipl = Object(id=id, x=x, y=y, z=z, rx=rx, ry=ry, rz=rz ,rw=rw)
						placements_files.append(ipl)
					else:
						print(f"{id} not found in defination!")
	return placements_files

def writeDefs(zone, definitions):
	path_def = os.path.join(output_dir, "zones", zone, f"{zone}.definition")
	os.makedirs(os.path.dirname(path_def), exist_ok=True)

	output_string_buffer = "<zoneDefinitions>\n"
	for d in definitions:
		output_string_buffer += f"\t{d}\n"
	output_string_buffer += "</zoneDefinitions>"

	try:
		with open(path_def, "w", encoding="utf-8") as f:
			f.write(output_string_buffer)
		print(f"{os.path.basename(path_def)} is created")
	except Exception as e:
		print(f"Failed to write {os.path.basename(path_def)}: {e}")

def writeMaps(zone, plcements):
	path_def = os.path.join(output_dir, "zones", zone, f"{zone}.map")
	os.makedirs(os.path.dirname(path_def), exist_ok=True)

	output_string_buffer = "<map>\n"
	for p in plcements:
		output_string_buffer += f"\t{p}\n"
	output_string_buffer += "</map>"

	try:
		with open(path_def, "w", encoding="utf-8") as f:
			f.write(output_string_buffer)
		print(f"{os.path.basename(path_def)} is created")
	except Exception as e:
		print(f"Failed to write {os.path.basename(path_def)}: {e}")

def writeZones(zones):
	# this creates eagleZones.txt
	path_txt = os.path.join(output_dir, "eagleZones.txt")
	output_string_buffer = ""
	for zone in zones:
		output_string_buffer += f"{zone}\n"

	try:
		with open(path_txt, "w", encoding="utf-8") as f:
			f.write(output_string_buffer)
		print(f"{os.path.basename(path_txt)} is created")
	except Exception as e:
		print(f"Failed to write {os.path.basename(path_txt)}: {e}")

def load_map(path):
	ide_paths, ipl_paths = read_gta_dat(path)

	# Load IDE first
	for ide_file in ide_paths:
		defination_files = load_ides(ide_file)
		zone = os.path.splitext(os.path.basename(ide_file))[0].lower()
		map_data["zone"][zone] = {
			"defination": defination_files,
			"placement": [],
		}
		# process defination hash table
		for defination in defination_files:
			map_data["defination_files"][defination.id] = defination


	# Then Lod IPL
	for ipl_file in ipl_paths:
		zone = os.path.splitext(os.path.basename(ipl_file))[0].lower()
		placement_files = load_ipls(ipl_file)
		map_data["zone"][zone]["placement"] = placement_files


	# Process zone & write .defs & .maps
	for zone in map_data["zone"]:
		print("Process Zone:",zone)
		definations = map_data["zone"][zone]["defination"]
		placements = map_data["zone"][zone]["placement"]

		writeDefs(zone, definations)
		writeMaps(zone, placements)

	# Write zone index file
	writeZones(map_data["zone"])

	# Todo. Finally Write meta.xml

# Example usage:
if __name__ == '__main__':
	dat_folder = "E:\\bayview\\sa"
	img_folder = "E:\\bayview\\sa\\img"
	output_dir = "E:\\bayview\\output"

	load_map(dat_folder)
