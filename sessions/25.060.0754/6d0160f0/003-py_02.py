def analyze_example(input_grid, output_grid, predicted_grid):
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    predicted_grid = np.array(predicted_grid)

    grey_lines_input = find_grey_lines(input_grid)
    grey_lines_output = find_grey_lines(output_grid)
    grey_lines_predicted = find_grey_lines(predicted_grid)

    print(f"Input Grey Lines: {grey_lines_input}")
    print(f"Output Grey Lines: {grey_lines_output}")
    print(f"Predicted Grey Lines: {grey_lines_predicted}")
    print(f"Input Shape: {input_grid.shape}")
    print(f"Output Shape: {output_grid.shape}")
    print(f"Predicted Shape: {predicted_grid.shape}")
    
    correct = np.array_equal(output_grid, predicted_grid)
    print(f"Correct: {correct}")
    if not correct:
        diff = output_grid != predicted_grid
        print(f"Number of differing pixels = {np.sum(diff)}")
    # Additional analysis can be added here as needed (e.g., object counting)

# Example usage (replace with actual data from each example)
task_examples = task["train"]
for i in range(len(task_examples)):
    input_grid = task_examples[i]["input"]
    output_grid = task_examples[i]["output"]
    predicted_grid = transform(input_grid)
    print(f"--- Example {i+1} ---")
    analyze_example(input_grid, output_grid, predicted_grid)
