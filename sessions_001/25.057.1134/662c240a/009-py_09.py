# code execution metrics for example 3
import numpy as np

input_grid = [[0, 0, 0, 0, 0, 0, 1, 1, 1], [0, 0, 0, 0, 0, 0, 1, 1, 1], [0, 0, 0, 0, 0, 0, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]
output_grid = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]

input_array = np.array(input_grid)
output_array = np.array(output_grid)
print(f"Input shape: {input_array.shape}")
print(f"Output shape: {output_array.shape}")

blue_indices = np.where(input_array == 1)
min_row, min_col = np.min(blue_indices, axis=1)
max_row, max_col = np.max(blue_indices, axis=1)

print(f"Blue square: Top-left: ({min_row},{min_col}), Bottom-right: ({max_row},{max_col})")