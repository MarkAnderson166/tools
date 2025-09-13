import os
import shutil

# --- Configuration ---
target_dir = "E:/junk_fill"  # Change to the target drive
sample_file = "dummy_data.bin"
file_size_MB = 1000  # Size of each copy
space_buffer_MB = 2000  # Leave a little room to avoid system errors

# --- Create Sample File ---
with open(sample_file, "wb") as f:
    f.write(os.urandom(file_size_MB * 1024 * 1024))

# --- Fill the Drive ---
count = 0
total, used, free = shutil.disk_usage(target_dir)
goal = int((total-space_buffer_MB-used)/ (file_size_MB* 1024 * 1024))
while True:
    total, used, free = shutil.disk_usage(target_dir)
    if free < space_buffer_MB * 1024 * 1024:
        print("Disk is nearly full. Stopping.")
        break
    new_file = os.path.join(target_dir, f"junk_{count}.bin")
    shutil.copy2(sample_file, new_file)
    count += 1
    print("%s/%s files created, disk: %s %s"%(count,goal,used,free))