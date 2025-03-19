example_input_3 = np.array([
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 3, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0]
])

example_output_3 = np.array([
    [0, 0, 4, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0]
])
predicted_output_3 = transform(example_input_3)
print(f"Example 3 - Number of differing pixels: {np.sum(example_output_3 != predicted_output_3)}")
print(f"Example 3 - Indices of differing pixels (row, col):\n{np.array(np.where(example_output_3 != predicted_output_3)).T}")