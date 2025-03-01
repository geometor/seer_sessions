import numpy as np

input_grid = np.array([
    [0, 1, 0],
    [1, 5, 1],
    [0, 1, 0]
])
expected_output = np.array([
    [0, 1, 0],
    [0, 5, 0],
    [0, 0, 0]
])
actual_output = transform(input_grid)

print("Example 0")
print("Input:\n", input_grid)
print("Expected Output:\n", expected_output)
print("Actual Output:\n", actual_output)
print("Match:", np.array_equal(actual_output, expected_output))
