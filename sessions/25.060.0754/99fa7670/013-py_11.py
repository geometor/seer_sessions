import numpy as np

input_grid = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 8, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
])
output_grid = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 8, 8],
    [0, 0, 0, 0, 0, 0, 8, 8],
])
print(f"Input shape: {input_grid.shape}")
print(f"Output shape: {output_grid.shape}")
input_non_zero = np.transpose(np.nonzero(input_grid))
output_non_zero = np.transpose(np.nonzero(output_grid))

print(f"Input non-zero indices: {input_non_zero}")
print(f"Output non-zero indices: {output_non_zero}")