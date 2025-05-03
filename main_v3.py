import os
from model.defination import *
from model.placement import *

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


def load_ides(path, game="SA"):
	defination_files = []
	items = process_section(path)
	# Get IDE Name from path
	zone = os.path.splitext(os.path.basename(path))[0]
	for section in items:
		if section == "objs":
			for obj in items[section]:
				# id =int(obj[0])
				id = obj[1]  # use model name for id instead ...
				model = obj[1]
				txd = obj[2]
				draw_dist = int(obj[3])
				flag = int(obj[3])

				ide = Defination(zone=zone, id=id, dff=model, col=model, txd=txd, lodDistance=draw_dist, flag=flag)
				defination_files.append(ide)
	return defination_files


def load_ipls(path, game="SA"):
	placements = []
	items = process_section(path)
	# Get IDE Name from path
	zone = os.path.splitext(os.path.basename(path))[0]
	for section in items:
		# ID, ModelName, Interior, PosX, PosY, PosZ, RotX, RotY, RotZ, RotW, LOD (SA FORMAT)
		if section == "inst":
			for obj in items[section]:
				if game == "SA":
					# id =int(obj[0])
					id = obj[1]  # use model name for id instead ...
					model = obj[1]
					interior = int(obj[2])
					x = float(obj[3])
					y = float(obj[4])
					z = float(obj[5])
					rx = float(obj[6])
					ry = float(obj[7])
					rz = float(obj[8])
					rw = float(obj[9])
					lod = int(obj[10])

					defination = map_data["defination_files"][id]
					if defination:
						object = None
						if defination.lodDistance > 299:  # if lod is not set but drawdist is > 299, set itself
							object = Building(id=id, x=x, y=y, z=z, rx=rx, ry=ry, rz=rz)
						else:
							object = Object(id=id, x=x, y=y, z=z, rx=rx, ry=ry, rz=rz)
						placements.append(object)
					else:
						print(f"{id} not found in defination!")
	return placements


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



	for ipl_file in ipl_paths:
		zone = os.path.splitext(os.path.basename(ipl_file))[0].lower()
		placement_files = load_ipls(ipl_file)
		map_data["zone"][zone]["placement"] = placement_files,


	# process zone
	for zone in map_data["zone"]:
		print(zone)
		definations = map_data["zone"][zone]["defination"]
		placements = map_data["zone"][zone]["placement"]
		print(definations)



# Example usage:
if __name__ == '__main__':
	dat_folder = "E:\\bayview\\sa"
	load_map(dat_folder)
