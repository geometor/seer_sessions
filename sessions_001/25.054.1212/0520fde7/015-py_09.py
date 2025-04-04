import numpy as np

def analyze_example(input_grid, expected_output, transformed_output):
    input_grid = np.array(input_grid)
    expected_output = np.array(expected_output)
    transformed_output = np.array(transformed_output)

    match = np.array_equal(expected_output, transformed_output)
    pixels_off = np.sum(expected_output != transformed_output)
    size_correct = input_grid.shape[0] >= expected_output.shape[0]
    color_palette_correct = all([x in [0,1,2,5] for x in np.unique(np.concatenate((input_grid.flatten(), expected_output.flatten(), transformed_output.flatten())))])

    input_rows, input_cols = input_grid.shape
    gray_stripe_col = -1
    for j in range(input_cols):
      if all(input_grid[i,j] == 5 for i in range(input_rows)):
        gray_stripe_col = j
        break

    row_mapping = {}
    if input_rows > 0: # prevent division by 0
      zone_size = input_rows / 3
      for output_row in range(3):
          start_input_row = int(output_row * zone_size)
          end_input_row = int((output_row + 1) * zone_size)
          row_mapping[output_row] = list(range(start_input_row, end_input_row))
    else:
        row_mapping[0]=[]
        row_mapping[1]=[]
        row_mapping[2]=[]

    adjacent_blues = {"left": [False, False, False], "right": [False, False, False]}

    for output_row in range(3):
        for input_row in row_mapping[output_row]:
            if 0 <= gray_stripe_col-1 < input_cols and  input_grid[input_row, gray_stripe_col - 1] == 1:
                adjacent_blues["left"][output_row] = True
            if 0 <= gray_stripe_col+1 < input_cols and input_grid[input_row, gray_stripe_col + 1] == 1:
                adjacent_blues["right"][output_row] = True

    print(f"  match: {match}")
    print(f"  pixels_off: {pixels_off}")
    print(f"  size_correct: {size_correct}")
    print(f"  color_palette_correct: {color_palette_correct}")
    print(f"  gray_stripe_col: {gray_stripe_col}")
    print(f"  row_mapping: {row_mapping}")
    print(f"  adjacent_blues: {adjacent_blues}")
    print("-----")

print("Example 1:")
analyze_example(
    [[1, 0, 0, 5, 0, 1, 0], [0, 1, 0, 5, 1, 1, 1], [1, 0, 0, 5, 0, 0, 0]],
    [[0, 0, 0], [0, 2, 0], [0, 0, 0]],
    [[0, 0, 0], [0, 0, 2], [0, 0, 0]],
)

print("Example 2:")
analyze_example(
    [[1, 1, 0, 5, 0, 1, 0], [0, 0, 1, 5, 1, 1, 1], [1, 1, 0, 5, 0, 1, 0]],
    [[0, 2, 0], [0, 0, 2], [0, 2, 0]],
    [[0, 0, 0], [2, 0, 2], [0, 0, 0]],
)

print("Example 3:")
analyze_example(
    [[0, 0, 1, 5, 0, 0, 0], [1, 1, 0, 5, 1, 0, 1], [0, 1, 1, 5, 1, 0, 1]],
    [[0, 0, 0], [2, 0, 0], [0, 0, 2]],
    [[2, 0, 0], [0, 0, 2], [2, 0, 2]],
)