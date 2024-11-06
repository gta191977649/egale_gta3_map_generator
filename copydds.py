import os
import shutil

# Paths to the directories
tga_dir = 'F:\\bayview\\l4ra\\beaconhill_east.fbm'  # Update this to the path where your *.tga files are stored
dds_dir = 'F:\\bayview\\main\\img\\textures'  # Update this to the path where your *.dds files are stored
output_dir = 'F:\\bayview\\sa\\txd'  # Update this to your desired output directory
# Ensure the output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Get a list of all .tga filenames without extension
tga_files = [os.path.splitext(f)[0] for f in os.listdir(tga_dir) if f.endswith('.tga')]

# Copy corresponding .dds files
for file_name in tga_files:
    dds_file_path = os.path.join(dds_dir, file_name + '.dds')
    if os.path.exists(dds_file_path):
        shutil.copy(dds_file_path, output_dir)
        print(f'Copied: {dds_file_path} to {output_dir}')
    else:
        print(f'No corresponding .dds file found for {file_name}')

print("Copying complete.")
