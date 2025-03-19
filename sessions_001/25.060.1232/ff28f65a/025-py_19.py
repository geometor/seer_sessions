input_grid0 = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 2, 2, 0, 0, 0],
    [0, 0, 0, 2, 2, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
])
expected_output0 = np.array([[0, 0, 1, 0, 0]])

print(f"input: {describe_grid(input_grid0)}")
print(f"expected: {describe_grid(expected_output0)}")

predicted_output0 = transform(input_grid0)
print(f"predicted: {describe_grid(predicted_output0)}")

check_output(predicted_output0, expected_output0)