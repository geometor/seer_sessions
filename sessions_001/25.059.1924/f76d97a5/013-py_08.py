import json
import numpy as np

# Load the task data
with open('data/training/6fa7a44f.json', 'r') as f:
    task_data = json.load(f)

# the transform() and get_diagonally_adjacent_indices() functions as defined before.

def analyze_results(task_data):
  for example in task_data['train']:
        input_grid = example['input']
        expected_output_grid = example['output']
        predicted_output_grid = transform(input_grid)

        input_grid_np = np.array(input_grid)
        expected_output_np = np.array(expected_output_grid)
        predicted_output_np = np.array(predicted_output_grid)
        
        print(f"Example:")
        print(f"Input:\n{input_grid_np}")
        print(f"Expected Output:\n{expected_output_np}")
        print(f"Predicted Output:\n{predicted_output_np}")

        if not np.array_equal(expected_output_np, predicted_output_np):
            print("Differences:")
            diff = expected_output_np != predicted_output_np
            print(diff)

        print("-" * 20)

analyze_results(task_data)