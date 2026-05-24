import os
import random

def main():
    directory = os.getcwd()

    files = [
        f for f in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, f))
    ]

    if not files:
        print("No files found.")
        return

    preview_count = min(5, len(files))

    print("This script will rename files in the current directory.")
    print(f"Total files: {len(files)}")
    print("Sample files:")
    for name in files[:preview_count]:
        print(f"  {name}")

    response = input("Are you sure you want to continue? Type 'yes' to proceed: ").strip().lower()
    if response != "yes":
        print("Aborted.")
        return

    existing = set(files)

    for filename in files:
        while True:
            prefix = f"{random.randint(0, 999):03d}_"
            new_name = prefix + filename
            if new_name not in existing:
                break

        os.rename(filename, new_name)
        existing.add(new_name)

    print("Done.")

if __name__ == "__main__":
    main()
