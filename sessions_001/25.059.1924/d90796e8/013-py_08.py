import numpy as np

def report_on_grids(input_grid, expected_output, actual_output):
    """
    Generates reports on the grids.

    Args:
    input_grid: A numpy array representing the input grid.
    expected_output: A numpy array representing the expected output grid.
    actual_output: A numpy array representing the actual output grid.

    Returns:
      dict: report on the grids
    """

    report = {}

    report['input_grid_shape'] = input_grid.shape
    report['expected_output_shape'] = expected_output.shape
    report['actual_output_shape'] = actual_output.shape
    report['input_unique_colors'] = np.unique(input_grid).tolist()
    report['expected_unique_colors'] = np.unique(expected_output).tolist()
    report['actual_unique_colors'] = np.unique(actual_output).tolist()
    report['pixel_differences_count'] = np.sum(expected_output != actual_output)
    report['different_pixels'] = []
    
    for row in range(expected_output.shape[0]):
        for col in range(expected_output.shape[1]):
          if expected_output[row,col] != actual_output[row,col]:
            report['different_pixels'].append(
                {
                   'location':(row,col),
                   'expected':int(expected_output[row,col]),
                   'actual': int(actual_output[row,col])
                }
            )
    return report


def load_grids(task_json, pair_index):
    """Loads and returns the input, expected, and actual grids for a given task and pair index."""
    
    import json
    with open(task_json, 'r') as f:
        task = json.load(f)
    
    input_grid = np.array(task['train'][pair_index]['input'])
    expected_output = np.array(task['train'][pair_index]['output'])
    
    # execute the transform function on the input_grid
    with open("previous_code.py", "r") as f:
        previous_code = f.read()
    
    exec(previous_code, globals())
    actual_output = transform(input_grid)
    
    return input_grid, expected_output, actual_output

# Example usage (assuming you have 'task.json' and 'previous_code.py'):
task_json = 'task.json'  # Replace with your actual task file
all_reports = {}

for i in range(3): # assuming 3 example pairs
  input_grid, expected_output, actual_output = load_grids(task_json, i)
  report = report_on_grids(input_grid, expected_output, actual_output)
  all_reports[f'pair_{i}'] = report

# you can now analyze all all_reports
print(all_reports)