import numpy as np

# Example data (replace with actual data from the task)
example1_input = np.array([[1, 1, 2, 2], [1, 1, 2, 2], [3, 3, 4, 4], [3, 3, 4, 4]])
example1_output = np.array([[1, 2], [3, 4]])

example2_input = np.array([[5, 5, 5, 5], [5, 5, 5, 5], [6, 6, 6, 6], [6, 6, 6, 6]])
example2_output = np.array([[5, 5], [6, 6]])

example3_input = np.array([
    [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2],
    [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2],
    [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2],
    [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2],
    [3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5],
    [3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5],
    [3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5],
    [3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5],
    [6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8],
    [6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8],
    [6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8],
    [6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8],
])
example3_output = np.array([
    [0, 1, 2, 2, 1, 0],
    [0, 1, 2, 2, 1, 0],
    [3, 4, 5, 5, 4, 3],
    [3, 4, 5, 5, 4, 3],
    [6, 7, 8, 8, 7, 6],
    [6, 7, 8, 8, 7, 6],
])

def check_downsampling(input_grid, output_grid, method="top-left"):
    input_rows, input_cols = input_grid.shape
    output_rows, output_cols = input_rows // 2, input_cols // 2

    if output_grid.shape != (output_rows, output_cols):
        return False

    if method == "top-left":
        for i in range(output_rows):
            for j in range(output_cols):
                if input_grid[i * 2, j * 2] != output_grid[i, j]:
                    return False
        return True
    else:
        return False  # Other methods not implemented yet

print("Example 1 - Top-left:", check_downsampling(example1_input, example1_output))
print("Example 2 - Top-left:", check_downsampling(example2_input, example2_output))
print("Example 3 - Top-left:", check_downsampling(example3_input, example3_output))

def analyze_example3(input_grid, output_grid):
  input_rows, input_cols = input_grid.shape
  output_rows, output_cols = output_grid.shape

  mapping = {}

  for out_row in range(output_rows):
    for out_col in range(output_cols):
      found = False
      for in_row in range(input_rows):
        for in_col in range(input_cols):
          if input_grid[in_row,in_col] == output_grid[out_row, out_col]:
            key = f"({out_row},{out_col})"
            if key not in mapping:
               mapping[key] = []
            if (in_row, in_col) not in mapping[key]:
              mapping[key].append((in_row,in_col))


  return mapping

example_3_map = analyze_example3(example3_input, example3_output)
print("Example 3 Detailed Mapping")
print(example_3_map)