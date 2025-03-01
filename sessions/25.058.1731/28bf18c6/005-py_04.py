from pathlib import Path
import json

task_file = Path("a85d4709.json")
task = json.loads(task_file.read_text())

results = get_example_results(task)
print (json.dumps(results, indent=2))