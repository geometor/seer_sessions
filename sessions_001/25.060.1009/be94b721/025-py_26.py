import numpy as np

def analyze_example(input_grid, expected_output_grid, actual_output_grid):
    red_pixels = find_pixels_by_color(input_grid, 2)
    height, width = get_rightmost_red_region_dimensions(input_grid, red_pixels)
    if len(red_pixels)>0:
      rightmost_col = np.max(red_pixels[:, 1])
      rightmost_pixels = red_pixels[red_pixels[:, 1] == rightmost_col]
      center_row_index = len(rightmost_pixels) // 2
      center_row, center_col = rightmost_pixels[center_row_index]
    else:
       center_row, center_col = 0,0

    return {
        "input_shape": input_grid.shape,
        "red_pixels": red_pixels.tolist(),
        "rightmost_red_region_dimensions": (height, width),
        "rightmost_red_region_center": (center_row, center_col),
        "expected_output_shape": expected_output_grid.shape,
        "actual_output_shape": actual_output_grid.shape,
    }

# Assuming 'task' is loaded with training examples and 'transform' is the function
results = []
for example in task["train"]:
    input_grid = np.array(example["input"])
    expected_output_grid = np.array(example["output"])
    actual_output_grid = transform(input_grid.copy())
    results.append(analyze_example(input_grid, expected_output_grid, actual_output_grid))

print(results)
