# code execution metrics for example 2
import numpy as np
input_grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0], [0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0], [0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0]]
output_grid = [[4, 4, 4], [4, 4, 4], [4, 4, 4]]

input_array = np.array(input_grid)
output_array = np.array(output_grid)
print(f"Input shape: {input_array.shape}")
print(f"Output shape: {output_array.shape}")

#find the yellow square
yellow_indices = np.where(input_array == 4)
min_row, min_col = np.min(yellow_indices, axis=1)
max_row, max_col = np.max(yellow_indices, axis=1)
print(f"Yellow square: Top-left: ({min_row},{min_col}), Bottom-right: ({max_row},{max_col})")