import numpy as np

def compare_grids(grid1, grid2):
    """Compares two grids and returns the number of differing pixels."""
    if grid1.shape != grid2.shape:
        return -1  # Indicate shape mismatch
    diff_count = np.sum(grid1 != grid2)
    return diff_count

# Example Usage and Metrics Gathering (This would be done for EACH example)

# Example 1
input_grid1 = np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]])
expected_output1 = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])
generated_output1 = transform(input_grid1)
diff1 = compare_grids(expected_output1, generated_output1)
print(f"Example 1 Differences: {diff1}")  # Expected: 0

# Example 2
input_grid2 = np.array([[0, 0, 0], [0, 2, 0], [0, 0, 0]])
expected_output2 = np.array([[0, 2, 0], [2, 2, 2], [0, 2, 0]])
generated_output2 = transform(input_grid2)
diff2 = compare_grids(expected_output2, generated_output2)
print(f"Example 2 Differences: {diff2}")  # Expected: 0

# Example 3
input_grid3 = np.array([[0, 0, 0, 0], [0, 0, 8, 0], [0, 0, 0, 0], [9, 0, 0, 0]])
expected_output3 = np.array([[9, 0, 8, 0], [9, 8, 8, 8], [9, 0, 8, 0], [9, 9, 9, 9]])
generated_output3 = transform(input_grid3)
diff3 = compare_grids(expected_output3, generated_output3)
print(f"Example 3 Differences: {diff3}")  # Expected: 0

# Example 4
input_grid4 = np.array([[0, 0, 0, 5], [0, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0]])
expected_output4 = np.array([[0, 1, 0, 5], [1, 1, 1, 5], [1, 1, 1, 5], [0, 1, 0, 5]])
generated_output4 = transform(input_grid4)
diff4 = compare_grids(expected_output4, generated_output4)
print(f"Example 4 Differences: {diff4}")  # Expected: 0

# Example 5:
input_grid5 = np.array([[0, 0, 7, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 5], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]])
expected_output5 = np.array([[0, 0, 7, 0, 5], [0, 0, 7, 0, 5], [0, 0, 7, 0, 5], [0, 0, 7, 0, 5], [0, 0, 7, 0, 5]])
generated_output5 = transform(input_grid5)
diff5 = compare_grids(expected_output5, generated_output5)
print(f"Example 5 Differences: {diff5}") # Expected 0
