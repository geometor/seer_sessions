def analyze_example(input_grid, expected_output, predicted_output):
    input_grid = np.array(input_grid)
    expected_output = np.array(expected_output)
    predicted_output = np.array(predicted_output)

    print("Input Grid:")
    print(input_grid)
    print("Expected Output Grid:")
    print(expected_output)
    print("Predicted Output Grid:")
    print(predicted_output)

    input_red_count = np.sum(input_grid == 2)
    expected_red_count = np.sum(expected_output == 2)
    predicted_red_count = np.sum(predicted_output == 2)


    print(f"Input Red Count: {input_red_count}")
    print(f"Expected Red Count: {expected_red_count}")
    print(f"Predicted Red Count: {predicted_red_count}")

    input_white_count = np.sum(input_grid == 0)
    expected_white_count = np.sum(expected_output == 0)
    predicted_white_count = np.sum(predicted_output == 0)

    print(f"Input White Count: {input_white_count}")
    print(f"Expected White Count: {expected_white_count}")
    print(f"Predicted White Count: {predicted_white_count}")

    dims_match = input_grid.shape == expected_output.shape
    print(f"Dimensions Match between the input and expected: {dims_match}")

    diff = expected_output - predicted_output
    print(f"Difference Between Expected and Predicted:\n{diff}")
    print("-----")


# Example data (replace with actual data from the task)
examples = [
    ([[0, 2, 0, 2, 0, 2, 0, 2, 0]], [[2, 2, 0, 0, 0, 0, 0, 0, 0], [2, 2, 0, 0, 0, 0, 0, 0, 0]], [[2, 2, 0, 0, 0, 0, 0, 0, 0], [2, 2, 0, 0, 0, 0, 0, 0, 0]]),
    ([[0, 2, 0, 0, 0, 2, 0, 2, 0, 0, 2, 0]], [[2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0]], [[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
    ([[0, 2, 2, 0, 0, 2, 0, 2, 0, 0, 2, 0]], [[2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0]], [[2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
]

for input_grid, expected_output, predicted_output in examples:
    analyze_example(input_grid, expected_output, predicted_output)
