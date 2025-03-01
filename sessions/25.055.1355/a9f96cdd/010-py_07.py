import json
import numpy as np

def find_pixel(grid, color_value):
    rows, cols = np.where(grid == color_value)
    if len(rows) > 0:
        return rows[0], cols[0]  # Return the first occurrence
    return None

def analyze_examples(task):
    results = []
    for example in task['train']:
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])

        red_input_pos = find_pixel(input_grid, 2)
        green_input_pos = find_pixel(input_grid, 3) # important - look for green in the input
        red_output_pos = find_pixel(output_grid, 2)
        green_output_pos = find_pixel(output_grid, 3)

        results.append({
            'input_red': red_input_pos,
            'input_green': green_input_pos,
            'output_red': red_output_pos,
            'output_green': green_output_pos,
        })
    return results

# Load the task data from the JSON file
task_file_path = '868de0fa.json'  # Replace with the actual path to your task file
with open(task_file_path, 'r') as f:
    task = json.load(f)

analysis_results = analyze_examples(task)
print(analysis_results)
