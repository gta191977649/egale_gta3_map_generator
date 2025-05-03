import os

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

            if line.startswith('IDE'): # Read IDE
                if os.path.exists(full_path):
                    ide_files.append(full_path)
                else:
                    print(f"{full_path} not found")

            if line.startswith('IPL'): # Read IPL
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

def load_ide(path,game="SA"):
   items = process_section(path)
   for section in items:
       if section == "objs":
           print(section)
           for obj in items[section]:
               print(obj)

def load_map(path):
    ide_list, ipl_list = read_gta_dat(path)

    for ide_file in ide_list:
        load_ide(ide_file)
        return
    print("IDE files:", ide_list)
    print("IPL files:", ipl_list)



# Example usage:
if __name__ == '__main__':
    dat_folder = "/Users/nurupo/Desktop/dev/map"
    load_map(dat_folder)
