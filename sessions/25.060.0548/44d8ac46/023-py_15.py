import numpy as np

input_grid = np.array([
    [5, 5, 5, 5, 5],
    [5, 5, 5, 5, 5],
    [5, 5, 5, 5, 5],
    [5, 5, 5, 0, 5],
    [5, 5, 5, 5, 5]
])

output_grid = np.array([
    [5, 5, 5, 5, 5],
    [5, 5, 5, 5, 5],
    [5, 5, 5, 5, 5],
    [5, 5, 5, 1, 5],
    [5, 5, 5, 5, 5]
])

print(f"Input shape: {input_grid.shape}")
print(f"Output shape: {output_grid.shape}")
diff = input_grid != output_grid
print(f"Number of pixel differences: {np.sum(diff)}")
print(f"Indices of differing pixels: {np.where(diff)}")
print(f"Input values at diff: {input_grid[diff]}")
print(f"Output values at diff: {output_grid[diff]}")
