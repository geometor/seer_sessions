# this is used for reporting, it won't be part of the final solution
# Load the task data
import json
task_file = 'b2862040.json'  # path to the task file

with open(task_file, 'r') as f:
    task_data = json.load(f)

analysis = analyze_results(task_data)

for idx,result in enumerate(analysis):
    print (f"Example {idx}")
    print (f"Correct: {result['correct']}")
    print (f"Input objects: {result['input_objects']}")
    print (f"Output objects: {result['output_objects']}")
    print (f"Predicted Objects: {result['predicted_objects']}")
    print (f"Output last column: {result['output_last_col']}")
    print (f"Predicted last column: {result['predicted_last_col']}")
    print ("---")