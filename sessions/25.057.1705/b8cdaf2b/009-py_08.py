import numpy as np

input_grid = np.array([
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2]
])

output_grid = np.array([
    [3, 0, 0, 0, 0, 3],
    [0, 3, 0, 0, 3, 0],
    [2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2]
])
result_grid = transform(input_grid)
print(np.array_equal(result_grid, output_grid))