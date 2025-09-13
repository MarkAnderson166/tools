import os

# Define the substring you want to remove
substring_to_remove = "ytmp3free.cc_"
#substring_to_remove = "-youtubemp3free.org"

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Loop through all files in the directory
for filename in os.listdir(script_dir):
    file_path = os.path.join(script_dir, filename)

    # Make sure it's a file (not a directory)
    if os.path.isfile(file_path) and substring_to_remove in filename:
        # Create new filename by removing the substring
        new_filename = filename.replace(substring_to_remove, "")
        new_file_path = os.path.join(script_dir, new_filename)

        # Rename the file
        os.rename(file_path, new_file_path)
        print(f"Renamed: '{filename}' → '{new_filename}'")
