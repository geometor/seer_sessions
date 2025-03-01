import numpy as np

def analyze_example(input_grid, output_grid, expected_grid):
    metrics = {}

    # Dimensions
    metrics['input_shape'] = input_grid.shape
    metrics['output_shape'] = output_grid.shape
    metrics['expected_shape'] = expected_grid.shape

    # Find red line in input (using the existing function)
    red_row, red_col_start, red_length = find_red_line(input_grid)
    metrics['red_line'] = (red_row, red_col_start, red_length)
    
    diff = output_grid - expected_grid
    metrics['error'] = np.count_nonzero(diff)

    metrics['output_value_counts'] = {i:np.count_nonzero(output_grid==i) for i in range(10)}
    metrics['expected_value_counts'] = {i:np.count_nonzero(expected_grid==i) for i in range(10)}


    return metrics

# Example usage (assuming 'input_grid', 'output_grid', and 'expected_grid' are available)
# You'll need to loop through your examples and call this function for each.
# Initialize 'task' with necessary information

results = []
for example in task["train"]:
  input_grid = np.array(example["input"])
  expected_grid = np.array(example["output"])
  output_grid = transform(input_grid)
  metrics = analyze_example(input_grid,output_grid,expected_grid)
  results.append(metrics)

import json
print(json.dumps(results,indent=2))
