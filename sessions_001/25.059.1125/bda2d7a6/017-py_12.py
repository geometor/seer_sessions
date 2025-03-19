import numpy as np

input_grid = np.array([
    [0, 0, 0, 0, 0, 0, 0],
    [0, 6, 6, 6, 6, 6, 0],
    [0, 6, 6, 0, 6, 6, 0],
    [0, 6, 6, 6, 6, 6, 0],
    [0, 6, 6, 6, 6, 6, 0],
    [0, 6, 6, 6, 6, 6, 0],
    [0, 0, 0, 0, 0, 0, 0]
])
expected_output_grid = np.array([
    [0, 0, 0, 0, 0, 0, 0],
    [0, 2, 2, 2, 2, 2, 0],
    [0, 2, 2, 0, 2, 2, 0],
    [0, 2, 2, 2, 2, 2, 0],
    [0, 2, 2, 2, 2, 2, 0],
    [0, 2, 2, 2, 2, 2, 0],
    [0, 0, 0, 0, 0, 0, 0]
])
actual_output_grid = transform(input_grid)
print(f"Matches Expected: {np.array_equal(actual_output_grid, expected_output_grid)}")
print(f"Expected:\n{expected_output_grid}")
print(f"Actual:\n{actual_output_grid}")