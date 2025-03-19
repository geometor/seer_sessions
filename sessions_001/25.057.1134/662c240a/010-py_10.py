# code execution metrics for example 1
import numpy as np

def get_metrics(input_grid, output_grid):
    input_array = np.array(input_grid)
    output_array = np.array(output_grid)

    #find the green square
    green_indices = np.where(input_array == 3)

    if green_indices[0].size == 0: # No green pixels
      min_row, min_col, max_row, max_col = -1, -1, -1, -1
    else:
      min_row, min_col = np.min(green_indices, axis=1)
      max_row, max_col = np.max(green_indices, axis=1)
      
    input_height, input_width = input_array.shape
    output_height, output_width = output_array.shape

    return {
      "input_dims": (input_height, input_width),
      "output_dims": (output_height, output_width),
      "green_bounding_box": {
          "top_left": (min_row, min_col),
          "bottom_right": (max_row, max_col),
          "height": max_row - min_row + 1 if min_row != -1 else 0,
          "width": max_col - min_col + 1 if min_col != -1 else 0
      }
  }

# Example 1 Data:
input_grid_1 = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [3, 3, 3, 0, 0, 0, 0, 0, 0], [3, 3, 3, 0, 0, 0, 0, 0, 0], [3, 3, 3, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]
output_grid_1 = [[3, 3, 3], [3, 3, 3], [3, 3, 3]]
metrics_1 = get_metrics(input_grid_1, output_grid_1)
print(f"Example 1 Metrics: {metrics_1}")

# Example 2 Data
input_grid_2 = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 3, 3, 3, 3, 0, 0], [0, 0, 0, 3, 3, 3, 3, 0, 0], [0, 0, 0, 3, 3, 3, 3, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]
output_grid_2 = [[3, 3, 3, 3], [3, 3, 3, 3], [3, 3, 3, 3]]
metrics_2 = get_metrics(input_grid_2, output_grid_2)
print(f"Example 2 Metrics: {metrics_2}")

# Example 3 Data
input_grid_3 = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 3, 3, 3, 3, 0, 0, 0], [0, 3, 3, 3, 3, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
output_grid_3 = [[3, 3, 3, 3], [3, 3, 3, 3]]
metrics_3 = get_metrics(input_grid_3, output_grid_3)
print(f"Example 3 Metrics: {metrics_3}")
