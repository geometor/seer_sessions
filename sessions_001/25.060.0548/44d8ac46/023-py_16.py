import numpy as np
input_grid = np.array([
    [8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 0, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8]
])

output_grid = np.array([
    [8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 2, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8]
])

print(f"Input shape: {input_grid.shape}")
print(f"Output shape: {output_grid.shape}")

diff = input_grid != output_grid
print(f"Number of pixel differences: {np.sum(diff)}")
print(f"Indices of differing pixels: {np.where(diff)}")
print(f"Input value at diff:{input_grid[diff]}")
print(f"Output value at diff: {output_grid[diff]}")