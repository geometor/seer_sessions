# code execution metrics for example 1
import numpy as np

input_grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [3, 3, 3, 0, 0, 0, 0, 0, 0], [3, 3, 3, 0, 0, 0, 0, 0, 0], [3, 3, 3, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]
output_grid = [[3, 3, 3], [3, 3, 3], [3, 3, 3]]

input_array = np.array(input_grid)
output_array = np.array(output_grid)
print(f"Input shape: {input_array.shape}")
print(f"Output shape: {output_array.shape}")

#find the green square
green_indices = np.where(input_array == 3)
min_row, min_col = np.min(green_indices, axis=1)
max_row, max_col = np.max(green_indices, axis=1)

print(f"Green square: Top-left: ({min_row},{min_col}), Bottom-right: ({max_row},{max_col})")