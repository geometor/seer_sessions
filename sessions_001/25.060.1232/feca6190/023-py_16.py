def analyze(input_grid, output_grid, predicted_output_grid):
    """Analyzes the input, expected output, and predicted output grids.

    Args:
        input_grid: The input grid.
        output_grid: The expected output grid.
        predicted_output_grid: The output grid predicted by the current code.

    Returns:
        A dictionary containing the analysis results.
    """
    input_shape = input_grid.shape
    output_shape = output_grid.shape
    predicted_output_shape = predicted_output_grid.shape

    input_colors = np.unique(input_grid)
    output_colors = np.unique(output_grid)
    predicted_output_colors = np.unique(predicted_output_grid)

    correct = np.array_equal(output_grid, predicted_output_grid)

    return {
        "input_shape": input_shape,
        "output_shape": output_shape,
        "predicted_output_shape": predicted_output_shape,
        "input_colors": input_colors.tolist(),
        "output_colors": output_colors.tolist(),
        "predicted_output_colors": predicted_output_colors.tolist(),
        "correct": correct,
    }

# Example usage (assuming 'task' is defined and loaded as before)
results = []
for i in range(len(task['train'])):
      predicted_output = transform(np.array(task['train'][i]['input']))
      analysis = analyze(np.array(task['train'][i]['input']), np.array(task['train'][i]['output']), predicted_output)
      results.append(f"Example {i+1}: {analysis}")

for r in results:
    print(r)
