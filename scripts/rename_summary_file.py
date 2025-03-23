import os
from pathlib import Path

def rename_summary_to_index(root_dir: str | Path):
    """
    Renames all files matching the pattern *.summary.json to index.json
    recursively within the given root directory.
    """
    root_path = Path(root_dir)

    if not root_path.is_dir():
        print(f"Error: '{root_dir}' is not a valid directory.")
        return

    for dirpath, dirnames, filenames in os.walk(root_path):
        for filename in filenames:
            if filename.endswith(".summary.json"):
                old_path = Path(dirpath) / filename
                new_path = Path(dirpath) / "index.json"

                try:
                    old_path.rename(new_path)
                    print(f"Renamed: {old_path} -> {new_path}")
                except OSError as e:
                    print(f"Error renaming {old_path}: {e}")

if __name__ == "__main__":
 #  root_directory = input("Enter the root directory to process (e.g., './sessions'): ")
 rename_summary_to_index("../sessions")
 print("Done.")
