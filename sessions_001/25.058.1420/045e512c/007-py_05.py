import numpy as np

def find_object(grid, color):
    """
    Finds the top-left corner and dimensions of a contiguous block of the given color.
    Returns None if no such object is found.
    """
    rows, cols = np.where(grid == color)
    if len(rows) == 0:
        return None

    min_row, min_col = np.min(rows), np.min(cols)
    max_row, max_col = np.max(rows), np.max(cols)
    height = max_row - min_row + 1
    width = max_col - min_col + 1

    return (min_row, min_col), height, width

def analyze_grid(grid):
    """
    Analyzes the grid and returns information about objects of specified colors.
    """
    colors = [2, 3, 8]  # Red, Green, Azure
    object_info = {}
    for color in colors:
        obj_data = find_object(grid, color)
        if obj_data:
            pos, height, width = obj_data
            object_info[color] = {
                "position": pos,
                "height": height,
                "width": width
            }
    return object_info
#task.train gives the train examples. task.train[n] gives a specific example.
#within each example, 'input' and 'output' are the grids.
example_results = []
for i in range(len(task.train)):

    input_grid = np.array(task.train[i]['input'])
    output_grid = np.array(task.train[i]['output'])

    input_analysis = analyze_grid(input_grid)
    output_analysis = analyze_grid(output_grid)

    example_results.append({
      "example_index": i,
      "input": input_analysis,
      "output": output_analysis,
      "grid_height": input_grid.shape[0],
      "grid_width": input_grid.shape[1]
    })


for res in example_results:
  print(res)