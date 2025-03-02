def code_execution(input_grid, expected_output, predicted_output):
    input_grid = np.array(input_grid)
    expected_output = np.array(expected_output)
    predicted_output = np.array(predicted_output)

    # Find magenta pixels in input
    magenta_pixels = np.argwhere(input_grid == 6)
    num_magenta_pixels = len(magenta_pixels)

    # Bounding box dimensions
    if num_magenta_pixels > 0:
      min_row, min_col = np.min(magenta_pixels, axis=0)
      max_row, max_col = np.max(magenta_pixels, axis=0)
      bounding_box_height = max_row - min_row + 1
      bounding_box_width = max_col - min_col + 1
    else:
      min_row, min_col, max_row, max_col = 0,0,0,0
      bounding_box_height = 0
      bounding_box_width = 0
    
    # check for shape equality first
    shapes_equal = (expected_output.shape == predicted_output.shape)
    
    # Output dimensions
    expected_height, expected_width = expected_output.shape if expected_output.size > 0 else (0,0)
    predicted_height, predicted_width = predicted_output.shape if predicted_output.size> 0 else (0,0)
    
    if shapes_equal:
      grids_equal = np.array_equal(expected_output, predicted_output)
    else:
      grids_equal = False

    return {
        "num_magenta_pixels": num_magenta_pixels,
        "bounding_box_height": bounding_box_height,
        "bounding_box_width": bounding_box_width,
        "expected_height": expected_height,
        "expected_width": expected_width,
        "predicted_height": predicted_height,
        "predicted_width": predicted_width,
        "shapes_equal": shapes_equal,
        "grids_equal": grids_equal,
        "min_row": min_row,
        "max_row": max_row,
        "min_col": min_col,
        "max_col": max_col
    }

# Example usage (replace with actual data from the task)
task_data = [
  {
        "input": [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 5, 5, 5, 5, 5, 5, 0],
            [0, 5, 6, 5, 5, 6, 5, 0],
            [0, 5, 5, 5, 5, 5, 5, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ],
        "output": [
            [5, 5, 5, 5, 5, 5],
            [5, 6, 5, 5, 6, 5],
            [5, 5, 5, 5, 5, 5],
        ],
    },
    {
        "input": [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 6, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ],
        "output": [[6]],
    },
    {
        "input": [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 6, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 6],
        ],
        "output": [
            [0, 0, 6, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 6]
        ],
    },
]

# this is hard coded from the transform function in the prompt
predicted_outputs = [
    [[6, 6]],
    [[6]],
    [[6],[6]]
]

results = []
for i,example in enumerate(task_data):
  results.append(code_execution(example["input"], example["output"], predicted_outputs[i]))

print(results)
