def compare_output(input_grid, expected_output, predicted_output):
    correct = np.array_equal(expected_output, predicted_output)
    input_shape = input_grid.shape
    output_shape = expected_output.shape
    predicted_shape = predicted_output.shape
    
    if correct:
        return "Correct", input_shape, output_shape, predicted_shape
    else:
        mismatches = np.where(expected_output != predicted_output)
        num_mismatches = len(mismatches[0])
        mismatch_details = []
        for i in range(num_mismatches):
            row = mismatches[0][i]
            col = mismatches[1][i]
            expected_val = expected_output[row, col]
            predicted_val = predicted_output[row, col]
            input_val = input_grid[row,col]
            mismatch_details.append(f"  at ({row},{col}): input={input_val}, expected={expected_val}, predicted={predicted_val}")
        return "Incorrect", input_shape, output_shape, predicted_shape, num_mismatches, mismatch_details
# Example usage (assuming you have loaded your task data)
results = []
for i, (train_input, train_output) in enumerate(task["train"]):
    input_grid = np.array(train_input['input'])
    expected_output = np.array(train_output['output'])
    predicted_output = transform(input_grid)  # Uses the function from initial code
    
    comparison_result = compare_output(input_grid, expected_output, predicted_output)
    results.append((f"Example {i+1}", comparison_result))

for result in results:
    print(f"{result[0]}:")
    print(f"  Result: {result[1][0]}")
    print(f"  Input Shape: {result[1][1]}")
    print(f"  Output Shape: {result[1][2]}")
    print(f"  Predicted Shape: {result[1][3]}")    
    if result[1][0] == "Incorrect":
        print(f"  Number of Mismatches: {result[1][4]}")
        for detail in result[1][5]:
            print(detail)