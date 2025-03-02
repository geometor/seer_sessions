import json
from pathlib import Path

def replace_key(sessions_root):
    """
    Finds all JSON files under sessions_root and replaces "status" key with "match".
    """
    for json_file in sessions_root.glob("**/*.json"):
        try:
            with open(json_file, 'r+') as f:  # Open in read-write mode
                data = json.load(f)

                modified = False
                if isinstance(data, list):
                    for item in 
                        if isinstance(item, dict) and "status" in item:
                            item["match"] = item.pop("status")
                            modified = True
                elif isinstance(data, dict) and "status" in 
                    data["match"] = data.pop("status")
                    modified = True

                if modified:
                    f.seek(0)  # Rewind to the beginning of the file
                    json.dump(data, f, indent=4)  # Write the updated data
                    f.truncate() #remove remaining part of old data
                    print(f"Updated: {json_file}")

        except (json.JSONDecodeError, OSError) as e:
            print(f"Error processing {json_file}: {e}")

if __name__ == "__main__":
    scripts_dir = Path(__file__).parent
    sessions_root = scripts_dir.parent / "sessions"
    replace_key(sessions_root)
