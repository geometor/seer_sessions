import numpy as np

def analyze_example(input_grid, output_grid, expected_output_grid):
    """Analyzes a single example and reports metrics."""

    input_shape = input_grid.shape
    output_shape = output_grid.shape
    expected_output_shape = expected_output_grid.shape
    success = np.array_equal(output_grid, expected_output_grid)


    print(f"  Input Shape: {input_shape}")
    print(f"  Output Shape: {output_shape}")
    print(f"  Expected Output Shape: {expected_output_shape}")
    print(f"  Success: {success}")

    if not success:

      diff = output_grid - expected_output_grid

      changed_indices = np.where(diff != 0)
      if changed_indices[0].size > 0 :

        row_start, col_start = changed_indices[0][0], changed_indices[1][0]
        #find the last row and column of the change
        row_end, col_end = changed_indices[0][-1], changed_indices[1][-1]

        print(f"  Difference first detected : row={row_start} , col={col_start}")

        height = row_end - row_start + 1
        width = col_end - col_start + 1
        print(f"  Dimensions of region incorrectly changed: {height}x{width}")
        print(f"  Incorrect change values:\n{output_grid[row_start:row_end+1, col_start:col_end+1]}")
        print(f"  Expected values:\n{expected_output_grid[row_start:row_end+1, col_start:col_end+1]}")

      else:
        print("no differences detected")

# Example Usage (replace with actual data).  Assuming you have loaded:
# train_input_2, train_output_2, train_predicted_output_2

print("Example 2 Analysis:")
# analyze_example(train_input_2, train_predicted_output_2, train_output_2)


print("\nExample 3 Analysis:")
# analyze_example(train_input_3, train_predicted_output_3, train_output_3)

