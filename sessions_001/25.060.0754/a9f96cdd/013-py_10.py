example_input_2 = np.array([
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 4, 0]
])
example_output_2 = np.array([
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 2, 0, 0],
    [0, 0, 0, 0, 0, 0]
])
predicted_output_2 = transform(example_input_2)
print(f"Example 2 - Number of differing pixels: {np.sum(example_output_2 != predicted_output_2)}")
print(f"Example 2 - Indices of differing pixels (row, col):\n{np.array(np.where(example_output_2 != predicted_output_2)).T}")