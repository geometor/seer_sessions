import numpy as np

def analyze_example(input_grid, output_grid):
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)

    report = {
        'red_objects': [],
        'blue_objects': [],
        'diagonal': [],
    }

    # Find red and blue objects (simplified for demonstration)
    for color, obj_list in [(2, report['red_objects']), (1, report['blue_objects'])]:
        for r in range(input_grid.shape[0]):
            for c in range(input_grid.shape[1]):
                if input_grid[r, c] == color:
                    obj_list.append((r, c))

    # Find the extreems
    if(len(report['red_objects'])):
      min_red = min(report['red_objects'])
      max_red = max(report['red_objects'])
    if(len(report['blue_objects'])):
      min_blue = min(report['blue_objects'])
      max_blue = max(report['blue_objects'])

    # Check diagonal path in output
    diff = output_grid - input_grid
    for r in range(diff.shape[0]):
        for c in range(diff.shape[1]):
            if diff[r, c] != 0:
                report['diagonal'].append((r, c, diff[r,c]))

    return {
        'red_extrema': (min_red, max_red) if len(report['red_objects']) else (),
        'blue_extrema': (min_blue, max_blue) if len(report['blue_objects']) else (),
        'diagonal': report['diagonal']
    }


# Example usage (replace with actual input/output grids)
task_examples = [
    ([[2, 2, 0, 0, 0, 0], [2, 2, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 1], [0, 0, 0, 0, 1, 1]], [[2, 2, 0, 0, 0, 0], [2, 2, 1, 0, 0, 0], [0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 1, 1], [0, 0, 0, 0, 1, 1]]),
    ([[2, 2, 0, 0, 0, 0, 0], [2, 2, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 1, 0], [0, 0, 0, 0, 1, 1, 0]], [[2, 2, 0, 0, 0, 0, 0], [2, 2, 1, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 1, 1, 0], [0, 0, 0, 0, 1, 1, 0]]),
    ([[0, 0, 0, 2, 2, 0, 0], [0, 0, 0, 2, 2, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 1, 1, 0, 0, 0, 0], [0, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]], [[0, 0, 0, 2, 2, 0, 0], [0, 0, 0, 2, 2, 0, 0], [0, 0, 0, 0, 0, 1, 0], [0, 1, 1, 0, 0, 0, 0], [0, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]),
    ([[2, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1]], [[2, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 1]]),
]

reports = []
for in_grid, out_grid in task_examples:
  reports.append(analyze_example(in_grid, out_grid))

for i, report in enumerate(reports):
  print(f"Example {i+1}:")
  print(f"  Red Extrema: {report['red_extrema']}")
  print(f"  Blue Extrema: {report['blue_extrema']}")
  print(f"  Diagonal Changes: {report['diagonal']}")