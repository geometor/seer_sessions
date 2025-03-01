def code_execution(input_grid, predicted_output, actual_output):
    input_grid = np.array(input_grid)
    predicted_output = np.array(predicted_output)
    actual_output = np.array(actual_output)

    print(f"Input Grid Shape: {input_grid.shape}")
    print(f"Predicted Output Shape: {predicted_output.shape}")
    print(f"Actual Output Shape: {actual_output.shape}")

    correct_elements = np.sum(predicted_output == actual_output)
    total_elements = predicted_output.size
    accuracy = correct_elements / total_elements if total_elements > 0 else 0.0

    print(f"Accuracy: {accuracy:.2f} ({correct_elements}/{total_elements})")
    print("Mismatched indices and values:")
    mismatches = np.where(predicted_output != actual_output)
    for i, j in zip(*mismatches):
        print(f"  Index: ({i}, {j}), Predicted: {predicted_output[i, j]}, Actual: {actual_output[i, j]}")

# Example calls for each training example:
train = [
    [[[8, 8, 8, 7, 8, 8, 8, 8, 8, 7, 8, 8, 8, 7, 8, 8], [5, 0, 0, 5, 0, 0, 0, 5, 0, 0, 0, 5, 0, 0, 0, 5], [5, 9, 9, 5, 9, 9, 9, 5, 9, 9, 9, 5, 9, 9, 9, 5], [0, 0, 0, 5, 0, 0, 0, 5, 0, 0, 0, 5, 0, 0, 0, 5], [8, 8, 8, 7, 8, 8, 8, 8, 8, 7, 8, 8, 8, 7, 8, 8]], [[8, 8, 8, 1], [5, 0, 0, 0], [5, 9, 9, 9], [0, 0, 0, 0]]],
    [[[8, 8, 8, 7, 8, 8, 8, 8, 8, 7, 8, 8, 8, 7, 8, 8], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [8, 8, 8, 7, 8, 8, 8, 8, 8, 7, 8, 8, 8, 7, 8, 8]], [[8, 8, 8, 1], [5, 5, 5, 5], [5, 5, 5, 5], [5, 5, 5, 5]]],
    [[[8, 8, 8, 7, 8, 8, 8, 8, 8, 7, 8, 8, 8, 7, 8, 8], [5, 0, 0, 5, 0, 0, 0, 5, 0, 0, 0, 5, 0, 0, 0, 5], [5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [8, 8, 8, 7, 8, 8, 8, 8, 8, 7, 8, 8, 8, 7, 8, 8]], [[8, 8, 8, 1], [5, 0, 0, 5], [5, 5, 5, 0], [5, 5, 5, 5]]]
]

for i, (input_grid, actual_output) in enumerate(train):
    print(f"\nExample {i+1}:")
    predicted_output = transform(input_grid) # Uses your current transform function
    code_execution(input_grid, predicted_output, actual_output)
