import numpy as np

def analyze_example(input_grid, output_grid, object_color=8):
    """
    Analyzes a single input-output pair and returns a dictionary of observations.
    """
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)

    object_rows, object_cols = np.where(input_grid == object_color)

    if len(object_rows) == 0:
        return {
            "object_present": False,
            "input_shape": input_grid.shape,
            "output_shape": output_grid.shape
        }

    min_row, max_row = np.min(object_rows), np.max(object_rows)
    min_col, max_col = np.min(object_cols), np.max(object_cols)

    object_height = max_row - min_row + 1
    object_width = max_col - min_col + 1

    # Count object pixels in each row and column
    object_pixels_per_row = np.sum(input_grid == object_color, axis=1)
    object_pixels_per_col = np.sum(input_grid == object_color, axis=0)

    output_object_rows, output_object_cols = np.where(output_grid == object_color)
    output_object_height = 0
    output_object_width = 0
    if (len(output_object_rows) > 0):
      output_object_height = np.max(output_object_rows) - np.min(output_object_rows) + 1
      output_object_width = np.max(output_object_cols) - np.min(output_object_cols) + 1

    return {
        "object_present": True,
        "input_shape": input_grid.shape,
        "output_shape": output_grid.shape,
        "object_height": object_height,
        "object_width": object_width,
        "object_pixels_per_row": object_pixels_per_row,
        "object_pixels_per_col": object_pixels_per_col,
        "output_object_height": output_object_height,
        "output_object_width": output_object_width
    }

def get_example_results(task):
  results = []
  for example in task["train"]:
    results.append(analyze_example(example["input"], example["output"]))
  return results