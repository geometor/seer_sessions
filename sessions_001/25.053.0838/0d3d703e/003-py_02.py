import numpy as np

input_grid = np.array([
    [2, 3, 8],
    [2, 3, 8],
    [2, 3, 8]
])

output_grid = np.array([
    [5, 6, 9],
    [5, 6, 9],
    [5, 6, 9]
])

# Check dimensions
print(f"Input grid dimensions: {input_grid.shape}")
print(f"Output grid dimensions: {output_grid.shape}")

# Unique values in input and output
print(f"Unique values in input: {np.unique(input_grid)}")
print(f"Unique values in output: {np.unique(output_grid)}")

# verify color mapping
color_map_check={}
for i in range(input_grid.size):
       color_map_check[input_grid.item(i)] = output_grid.item(i)

print(color_map_check)