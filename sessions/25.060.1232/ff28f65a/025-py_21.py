input_grid2 = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 2, 2, 0, 0, 0, 0],
    [0, 0, 2, 2, 0, 0, 0, 0],
])
expected_output2 = np.array([[0, 1, 0, 0, 0, 0]])
print(f"input: {describe_grid(input_grid2)}")
print(f"expected: {describe_grid(expected_output2)}")

predicted_output2 = transform(input_grid2)
print(f"predicted: {describe_grid(predicted_output2)}")

check_output(predicted_output2, expected_output2)