from pathlib import Path
import json
# this assumes you have a /data directory with the unzipped ARC data
data_path = Path('./data')
training_path = data_path / 'training'

task_file = training_path / '88a10456.json'
task = json.loads(task_file.read_text())

# transform defined in "Previous Code" section above

results = describe_differences(task)
for line in results:
  print(line)