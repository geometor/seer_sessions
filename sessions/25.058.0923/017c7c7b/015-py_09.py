import numpy as np

def find_vertical_line(grid, color):
    # Find columns that have at least one pixel of the specified color
    cols_with_color = np.any(grid == color, axis=0)

    # Ensure that all elements in these columns, that are not the background color, equal to color
    for col_idx in np.where(cols_with_color)[0]:
        column = grid[:, col_idx]
        if not np.all((column == color) | (column == 0)):  # Assuming 0 is background
           return None
    # return the index
    return np.where(cols_with_color)[0]

def transform(input_grid):
    # Initialize output_grid as a copy of input and change the color
    output_grid = input_grid.copy()
    output_grid[output_grid == 1] = 2

    # Find the vertical line of blue pixels
    blue_line_cols = find_vertical_line(input_grid, 1)

    # Add three rows for the red
    if blue_line_cols is not None:
       num_rows_to_add = 3
       rows, cols = output_grid.shape
       new_output_grid = np.zeros((rows + num_rows_to_add, cols), dtype=int)
       new_output_grid[:rows,:] = output_grid
       for col in blue_line_cols:
          new_output_grid[rows:,col] = 2
       output_grid = new_output_grid

    return output_grid

task = {
  "train": [
    {
      "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0]],
      "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 0, 0, 0, 0, 0]]
    },
    {
      "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0]],
      "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 0, 0, 0, 0, 0]]
    },
    {
      "input": [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0]],
      "output": [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 0, 0, 0, 0], [0, 0, 0, 2, 0, 0, 0, 0], [0, 0, 0, 2, 0, 0, 0, 0], [0, 0, 0, 2, 0, 0, 0, 0], [0, 0, 0, 2, 0, 0, 0, 0], [0, 0, 0, 2, 0, 0, 0, 0]]
    }
  ],
  "test": [
    {
      "input": [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0]],
      "output": [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 0, 0, 0], [0, 0, 0, 2, 0, 0, 0], [0, 0, 0, 2, 0, 0, 0], [0, 0, 0, 2, 0, 0, 0], [0, 0, 0, 2, 0, 0, 0]]
    }
  ]
}

for i, example in enumerate(task["train"]):
    input_grid = np.array(example['input'])
    expected_output = np.array(example['output'])
    actual_output = transform(input_grid)
    print(f"Train Example {i+1}:")
    print(f"  Input grid shape: {input_grid.shape}")
    print(f"  Expected output shape: {expected_output.shape}")
    print(f"  Actual output shape: {actual_output.shape}")
    print(f"  Expected output:\n{expected_output}")
    print(f"  Actual output:\n{actual_output}")
    print(f"  Correct: {np.array_equal(actual_output, expected_output)}\n")

print("Test Example:")
test_input = np.array(task['test'][0]['input'])
expected_test_output = np.array(task['test'][0]['output'])
actual_test_output = transform(test_input)
print(f"  Input grid shape: {test_input.shape}")
print(f"  Expected output shape: {expected_test_output.shape}")
print(f"  Actual output shape: {actual_test_output.shape}")
print(f"  Expected output:\n{expected_test_output}")
print(f"  Actual output:\n{actual_test_output}")
print(f"  Correct: {np.array_equal(actual_test_output, expected_test_output)}\n")
