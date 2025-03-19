import numpy as np

def get_object_coordinates(grid, obj_color):
    coords = []
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r,c] == obj_color:
                coords.append((r,c))
    return coords

def analyze_example(input_grid, expected_output_grid, actual_output_grid):
    """Analyzes a single example and provides a report."""
    
    print(f"Input Grid:\n{input_grid}\n")
    print(f"Expected Output Grid:\n{expected_output_grid}\n")
    print(f"Actual Output Grid:\n{actual_output_grid}\n")

    report = {
        "input_shape": input_grid.shape,
        "expected_output_shape": expected_output_grid.shape,
        "actual_output_shape": actual_output_grid.shape,
        "object_color_input": None,
        "object_color_output": None,
        "input_object_coords": None,
        "expected_object_coords": None,
        "actual_object_coords": None,        
        "error": not np.array_equal(expected_output_grid, actual_output_grid),
        "comments": "",
    }

    # Determine the object color by finding the difference
    diff = input_grid != expected_output_grid
    if np.any(diff):
      changing_colors = np.unique(input_grid[diff])
      for color in changing_colors:
        if color != 0: # don't include the background in the search
          report["object_color_input"] = int(color) #ensure json friendly type
          break

    if report['object_color_input'] is not None:
        report["input_object_coords"] = get_object_coordinates(input_grid, report["object_color_input"])
        report["expected_object_coords"] = get_object_coordinates(expected_output_grid, report["object_color_input"])
        
        #check if transform created the expected object
        if report['object_color_input'] in actual_output_grid:
            report['object_color_output'] = report['object_color_input']
            report['actual_object_coords'] = get_object_coordinates(actual_output_grid, report["object_color_input"])

    return report

# Example Usage (replace with actual data)
# Assuming input_grids, expected_output_grids, actual_output_grids are lists of numpy arrays

input_grids = [
    np.array([[0, 0, 0], [0, 3, 0], [0, 0, 0]]),
    np.array([[0, 0, 0, 0], [0, 0, 0, 0], [6, 0, 0, 0]]),
    np.array([[0, 0, 0, 0, 0], [0, 0, 7, 0, 0], [0, 0, 0, 0, 0]]),
]
expected_output_grids = [
    np.array([[0, 0, 0], [0, 0, 3], [0, 0, 0]]),
    np.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 6, 0, 0]]),
    np.array([[0, 0, 0, 0, 0], [0, 0, 0, 7, 0], [0, 0, 0, 0, 0]]),
]
actual_output_grids = [
    np.array([[0, 0, 0], [0, 0, 3], [0, 0, 0]]),
    np.array([[0, 0, 0, 0], [0, 0, 0, 0], [6, 0, 0, 0]]),
    np.array([[0, 0, 0, 0, 0], [0, 0, 0, 7, 0], [0, 0, 0, 0, 0]]),

]

reports = []
for i in range(len(input_grids)):
    report = analyze_example(input_grids[i], expected_output_grids[i], actual_output_grids[i])
    reports.append(report)
    print("---")

print("\nAggregated Reports (YAML format):\n")
print("```yaml")
for i, report in enumerate(reports):
    print(f"example_{i+1}:")
    for key, value in report.items():
        print(f"  {key}: {value}")
    print()
print("```")
