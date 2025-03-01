import numpy as np

task = {
    "train": [
        {
            "input": [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 6, 6, 0, 0], [0, 0, 0, 6, 6, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 3, 0]],
            "output": [[0, 0, 0, 0, 0, 0, 0], [0, 3, 0, 6, 6, 0, 3], [0, 0, 0, 6, 6, 0, 0], [0, 0, 0, 6, 6, 0, 0], [0, 3, 0, 6, 6, 0, 3]],
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 6, 6, 0, 0], [0, 0, 0, 0, 0, 6, 6, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 3, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 3, 0, 0, 0], [0, 0, 0, 0, 0, 6, 6, 0, 3], [0, 0, 0, 0, 0, 6, 6, 0, 0], [0, 0, 0, 0, 0, 6, 6, 0, 0], [0, 3, 0, 0, 0, 6, 6, 0, 0]],
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 6, 6, 0, 0, 0, 0, 0], [0, 0, 0, 6, 6, 0, 3, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 3, 0, 0, 0, 0, 0, 0], [0, 0, 0, 6, 6, 0, 0, 3, 0, 0], [0, 0, 0, 6, 6, 0, 0, 0, 0, 0], [0, 0, 0, 6, 6, 0, 0, 0, 0, 0], [0, 0, 0, 6, 6, 0, 0, 0, 0, 0]],
        },
    ],
    "test": [{"input": [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 6, 6, 0, 0], [0, 0, 0, 0, 6, 6, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 3]], "output": []}],
}

def find_object(grid, color, shape=None):
    """Finds an object of a specific color and optionally shape."""
    coords = np.argwhere(grid == color)
    if len(coords) == 0:
        return None

    if shape == "point":
      if len(coords) == 1:
        return coords[0]
      else:
        return None

    if shape == "2x2 square":
        min_row = np.min(coords[:, 0])
        max_row = np.max(coords[:, 0])
        min_col = np.min(coords[:, 1])
        max_col = np.max(coords[:, 1])

        if (max_row - min_row == 1) and (max_col - min_col == 1):
           return (min_row, min_col)  # Return top-left corner
        else:
          return None

    return coords # return all coordinates of matching color

def analyze_green_placement(task):
  results = []
  for example in task["train"]:
      input_grid = np.array(example["input"])
      output_grid = np.array(example["output"])

      magenta_square_coord = find_object(input_grid, 6, "2x2 square")
      if magenta_square_coord is None:
          results.append({"error": "Magenta square not found"})
          continue # skip to next iteration

      # Expanded magenta square coordinates
      exp_top_left_row = magenta_square_coord[0] - 1
      exp_top_left_col = magenta_square_coord[1] - 1
      exp_bottom_right_row = magenta_square_coord[0] + 2
      exp_bottom_right_col = magenta_square_coord[1] + 2

      # Find green pixels in output
      green_pixel_coords = find_object(output_grid, 3)
      if green_pixel_coords is None:
        results.append({"error": "no green pixels found"})
        continue

      # calculate offsets
      offsets = []
      for green_coord in green_pixel_coords:
          row_offset = green_coord[0] - exp_top_left_row
          col_offset = green_coord[1] - exp_top_left_col
          offsets.append((row_offset, col_offset))

      results.append({
          "magenta_top_left": magenta_square_coord,
          "expanded_top_left": (exp_top_left_row, exp_top_left_col),
          "expanded_bottom_right": (exp_bottom_right_row, exp_bottom_right_col),
          "green_pixel_coords": green_pixel_coords.tolist(),
          "green_offsets": offsets
      })
  return results

analysis_results = analyze_green_placement(task)
for i, result in enumerate(analysis_results):
    print(f"Example {i+1}:")
    for key, value in result.items():
        print(f"  {key}: {value}")
    print("-" * 20)