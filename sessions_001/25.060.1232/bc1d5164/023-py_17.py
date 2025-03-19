def code_execution(input_grid, expected_output, actual_output):
    """
    Analyzes and compares the input, expected output, and actual output grids.
    Gathers metrics and provides observations.
    """
    results = {}

    def grid_analysis(grid):
      if not grid:
          return {
              "dimensions": (0, 0),
              "objects": [],
              "unique_colors": []
              }
      np_grid = np.array(grid)
      unique_colors = np.unique(np_grid).tolist()
      objects = []
      for color in unique_colors:
          if color == 0: #ignore background for object detection
              continue
          coords = np.where(np_grid == color)
          min_row, max_row = min(coords[0]), max(coords[0])
          min_col, max_col = min(coords[1]), max(coords[1])
          width = max_col - min_col + 1
          height = max_row - min_row + 1
          objects.append({
              "color": color,
              "top_left": (min_row, min_col),
              "bottom_right": (max_row, max_col),
              "width": width,
              "height": height,
              "shape": "rectangle",
              "pixel_count": len(coords[0])

          })

      return {
          "dimensions": np_grid.shape,
          "objects": objects,
          "unique_colors": unique_colors,

      }

    results["input_analysis"] = grid_analysis(input_grid)
    results["expected_output_analysis"] = grid_analysis(expected_output)
    results["actual_output_analysis"] = grid_analysis(actual_output)

    print(results)

# Example Usage (assuming task, transform are already defined, along with other needed imports)
for i, example in enumerate(task['train']):
    input_grid = example['input']
    expected_output = example['output']
    actual_output = transform(input_grid)
    print(f"--- Example {i+1} ---")
    code_execution(input_grid, expected_output, actual_output)