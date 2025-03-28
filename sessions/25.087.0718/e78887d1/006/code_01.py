import numpy as np
expected_output_2 = [[2, 2, 2, 0, 3, 0, 3, 0, 1, 0, 0], [0, 2, 0, 0, 0, 3, 0, 0, 1, 1, 1], [0, 2, 0, 0, 3, 0, 3, 0, 0, 0, 1]]
grid = np.array(expected_output_2)
print(np.sum(grid))
print(np.count_nonzero(grid))
unique, counts = np.unique(grid[grid != 0], return_counts=True)
print(dict(zip(unique, counts)))