import numpy as np

def is_solid_color_line(line):
    """Checks if a line (list) contains only one unique non-zero value."""
    unique_values = np.unique(line)
    return len(unique_values) == 1 and unique_values[0] != 0

def analyze_examples(task_data):
    results = []
    for example in task_data['train']:
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])

        input_solid_lines = []
        for i, row in enumerate(input_grid):
            if is_solid_color_line(row):
                input_solid_lines.append((i, row[0]))  # (row index, color)

        output_solid_lines = []
        for i, row in enumerate(output_grid):
            if is_solid_color_line(row):
                output_solid_lines.append((i, row[0])) # (row index, color)

        example_data = {
            'input_shape': input_grid.shape,
            'output_shape': output_grid.shape,
            'input_solid_lines': input_solid_lines,
            'output_solid_lines': output_solid_lines,
            'output_line_length': output_grid.shape[1] if len(output_grid) > 0 else 0,

        }
        results.append(example_data)
    return results

# the task data will be provided later when this block is executed in a notebook
# the notebook will define task_data
# for local dev, it can be initialized to an empty dict like this:
# task_data = {}
if 'task_data' not in locals():
    task_data = {}
    print("WARNING: `task_data` not found, initializing to empty {}.  This is expected behavior for local development, but not in the SEER evaluation notebook environment".format(task_data))
else:
  analysis_results = analyze_examples(task_data)
  print (analysis_results)