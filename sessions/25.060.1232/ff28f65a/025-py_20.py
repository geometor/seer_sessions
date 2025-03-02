input_grid1 = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 2, 2, 0, 0, 0, 0, 0],
    [0, 0, 2, 2, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
])
expected_output1 = np.array([[0, 1, 0, 0, 0, 0]])

print(f"input: {describe_grid(input_grid1)}")
print(f"expected: {describe_grid(expected_output1)}")

predicted_output1 = transform(input_grid1)
print(f"predicted: {describe_grid(predicted_output1)}")

check_output(predicted_output1, expected_output1)
