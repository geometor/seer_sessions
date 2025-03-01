import numpy as np

input_grid = np.array([
    [1, 0, 1],
    [0, 8, 0],
    [1, 0, 1]
])
expected_output = np.array([
    [1, 0, 1],
    [0, 8, 0],
    [1, 0, 1]
])
actual_output = transform(input_grid)

print("Example 2")
print("Input:\n", input_grid)
print("Expected Output:\n", expected_output)
print("Actual Output:\n", actual_output)
print("Match:", np.array_equal(actual_output, expected_output))
