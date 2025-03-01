import numpy as np

input_grid = np.array([
    [6, 1, 6],
    [1, 0, 1],
    [6, 1, 6]
])
expected_output = np.array([
    [6, 1, 6],
    [0, 0, 0],
    [6, 0, 6]
])
actual_output = transform(input_grid)

print("Example 1")
print("Input:\n", input_grid)
print("Expected Output:\n", expected_output)
print("Actual Output:\n", actual_output)
print("Match:", np.array_equal(actual_output, expected_output))
