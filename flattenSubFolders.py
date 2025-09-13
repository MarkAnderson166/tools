import os
import shutil

# Get the current (root) directory where the script is
root_dir = os.getcwd()

# Go through all immediate subdirectories in root_dir
for item in os.listdir(root_dir):
    item_path = os.path.join(root_dir, item)

    if os.path.isdir(item_path):
        # Skip if the directory is the script's own directory (root)
        # Start walking inside this subfolder
        for sub_item in os.listdir(item_path):
            sub_item_path = os.path.join(item_path, sub_item)

            # Compute the target path in the root folder
            dest_path = os.path.join(root_dir, sub_item)

            # If name collision, rename by appending _1, _2, etc.
            if os.path.exists(dest_path):
                base_name, ext = os.path.splitext(sub_item)
                counter = 1
                while True:
                    new_name = f"{base_name}_{counter}{ext}"
                    new_dest_path = os.path.join(root_dir, new_name)
                    if not os.path.exists(new_dest_path):
                        dest_path = new_dest_path
                        break
                    counter += 1

            # Move the file or directory
            shutil.move(sub_item_path, dest_path)

print("All contents from subfolders moved to the main folder.")

