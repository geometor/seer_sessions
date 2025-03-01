def report_metrics(input_grid, output_grid, predicted_output_grid):
    """
    Generates a report comparing the expected output and predicted output,
    highlighting discrepancies.
    """

    discrepancies = []
    if not np.array_equal(output_grid, predicted_output_grid):
        diff = output_grid != predicted_output_grid
        rows, cols = np.where(diff)
        for row, col in zip(rows, cols):
          discrepancies.append({
                "location": (row, col),
                "expected": output_grid[row, col],
                "predicted": predicted_output_grid[row, col],
            })
    
    report = {
        "input_grid_shape": input_grid.shape,
        "output_grid_shape": output_grid.shape,
        "predicted_output_grid_shape": predicted_output_grid.shape,
        "discrepancies": discrepancies,
    }
    return report

# this will be populated in the next code execution block.  It's important
# that it be defined here for continuity.
task_data = {}

example_reports = []
for example_index, example in enumerate(task_data['train']):
  input_grid = np.array(example['input'])
  output_grid = np.array(example['output'])
  predicted_output_grid = transform(input_grid)

  example_reports.append(report_metrics(input_grid, output_grid, predicted_output_grid))
# add the test example
input_grid = np.array(task_data['test'][0]['input'])
predicted_test_output = transform(input_grid)

print(example_reports)