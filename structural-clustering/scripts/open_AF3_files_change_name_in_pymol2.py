# Use Pymol to automate loading and renaming AF3 cif file.
# Open and run this code inside of Pymol.

import os
from pymol import cmd

# Main folder path having AF3 files
root_dir = r"D:\sp154-b_4"

# Extract main folder name for naming convention
main_folder_name = os.path.basename(root_dir)  # Gets p26572_1 from the path

# Loop through all subfolders
for subfolder in os.listdir(root_dir):
    subfolder_path = os.path.join(root_dir, subfolder)

    if os.path.isdir(subfolder_path):
        model_file = os.path.join(subfolder_path, "model.cif")
        
        if os.path.exists(model_file):
            try:
                seed = subfolder.split("seed-")[-1].split("_sample-")[0]
                sample = subfolder.split("_sample-")[-1]
                new_name = f"{main_folder_name}_s{seed}_p{sample}"  # Unique name

                cmd.load(model_file, new_name)
                print(f"✅ Loaded and named: {model_file} → {new_name}")
            except Exception as e:
                print(f"❌ Error loading {model_file}: {e}")
        else:
            print(f"⚠️ model.cif not found in {subfolder_path}")

