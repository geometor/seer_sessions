import numpy as np

# Provided transform function (copied here for completeness)
def transform(input_grid):
    # Initialize a 15x15 output grid filled with zeros.
    output_grid = np.zeros((15, 15), dtype=int)

    # Iterate through each pixel of the 3x3 input grid.
    for i in range(input_grid.shape[0]):
        for j in range(input_grid.shape[1]):
            pixel_value = input_grid[i, j]

            # Determine the top-left corner of the 5x5 block.
            row_start = i * 5
            col_start = j * 5

            if pixel_value != 0:
                # Fill the 5x5 block with the value of the input pixel.
                output_grid[row_start:row_start + 5, col_start:col_start + 5] = pixel_value
            else:
                # Zero Pixel Handling
                # Check for non-zero pixels in the same row or column
                non_zero_in_row = any(input_grid[i, k] != 0 for k in range(input_grid.shape[1]))
                non_zero_in_col = any(input_grid[k, j] != 0 for k in range(input_grid.shape[0]))

                if non_zero_in_row or non_zero_in_col:
                    # Find the non-zero value to propagate
                    if non_zero_in_row:
                        for k in range(input_grid.shape[1]):
                            if input_grid[i,k] != 0:
                                fill_value = input_grid[i,k]
                                break
                    elif non_zero_in_col:
                        for k in range(input_grid.shape[0]):
                            if input_grid[k,j] != 0:
                                fill_value = input_grid[k, j]
                                break

                    # output the block
                    output_grid[row_start:row_start+5, col_start:col_start+5] = fill_value
                # else:  # implicit from initialization with 0
                #     pass

    return output_grid
# Example data (replace with actual data from the task)
train_input_0 = np.array([[5, 0, 0], [0, 0, 0], [0, 0, 8]])
train_output_0 = np.array([[5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 8, 8], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 8, 8], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 8, 8], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 8, 8], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 8, 8]])
result_0 = transform(train_input_0)
diff_0 = np.sum(result_0 != train_output_0)
print(f"Example 0 Differences: {diff_0}")

train_input_1 = np.array([[1, 0, 0], [0, 2, 0], [0, 0, 3]])
train_output_1 = np.array([[1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3]])
result_1 = transform(train_input_1)
diff_1 = np.sum(result_1 != train_output_1)
print(f"Example 1 Differences: {diff_1}")

train_input_2 = np.array([[0, 7, 0], [0, 0, 0], [0, 6, 0]])
train_output_2 = np.array([[0, 0, 0, 0, 0, 7, 7, 7, 7, 7, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 7, 7, 7, 7, 7, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 7, 7, 7, 7, 7, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 7, 7, 7, 7, 7, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 7, 7, 7, 7, 7, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 6, 6, 6, 6, 6, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 6, 6, 6, 6, 6, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 6, 6, 6, 6, 6, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 6, 6, 6, 6, 6, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 6, 6, 6, 6, 6, 0, 0, 0, 0, 0]])
result_2 = transform(train_input_2)
diff_2 = np.sum(result_2 != train_output_2)
print(f"Example 2 Differences: {diff_2}")


for i in range(3):
   print(f"input shape {i}: {eval(f'train_input_{i}').shape}")
   print(f"output shape {i}: {eval(f'train_output_{i}').shape}")