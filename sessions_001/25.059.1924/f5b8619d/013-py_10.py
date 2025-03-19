def grid_info(grid):
    shape = grid.shape
    colors = np.unique(grid)
    return f"Shape: {shape}, Colors: {colors}"

input_output_pairs = task_data["train"]

reports = []
for i, pair in enumerate(input_output_pairs):
    input_grid = np.array(pair['input'])
    output_grid = np.array(pair['output'])
    predicted_output = transform(input_grid)
    comparison = np.array_equal(output_grid, predicted_output)

    report = f"""
Example {i + 1}:
Input Info: {grid_info(input_grid)}
Output Info: {grid_info(output_grid)}
Predicted Output Info: {grid_info(predicted_output)}
Match: {comparison}
"""
    reports.append(report)

print(*reports, sep='\n')