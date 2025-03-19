import numpy as np

inp = np.array([[5, 1, 5],
       [1, 1, 1],
       [1, 2, 1],
       [1, 1, 1],
       [1, 2, 1],
       [1, 1, 1],
       [5, 1, 5]])

out = np.array([[5, 0, 5],
       [0, 0, 0],
       [0, 2, 0],
       [0, 0, 0],
       [0, 2, 0],
       [0, 0, 0],
       [5, 0, 5]])

# running transform
output_grid = np.copy(inp)
if output_grid.shape[1] % 2 != 0:
    center_col = output_grid.shape[1] // 2
    output_grid[0, center_col] = 0

diff = output_grid - out
print(diff)