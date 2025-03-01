# Example Data (replace with actual data from the task)
example_input_1 = np.array([
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 2, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0]
])

example_output_1 = np.array([
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 3, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0]
])
predicted_output_1 = transform(example_input_1)
print(f"Example 1 - Number of differing pixels: {np.sum(example_output_1 != predicted_output_1)}")
print(f"Example 1 - Indices of differing pixels (row, col):\n{np.array(np.where(example_output_1 != predicted_output_1)).T}")