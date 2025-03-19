import numpy as np

def analyze_example(input_grid, output_grid, predicted_grid):
    """Analyzes a single example and provides a report."""

    rows, cols = input_grid.shape
    report = {
        "bottom_rows_consistent": True,
        "propagation_details": [],
    }

    # Check if the bottom two rows are consistent
    if not np.array_equal(input_grid[-2:, :], output_grid[-2:, :]):
        report["bottom_rows_consistent"] = False
    if not np.array_equal(input_grid[-2:, :], predicted_grid[-2:, :]):
        report["bottom_rows_consistent"] = False

    # Analyze propagation
    for i in range(rows - 2):
        for j in range(cols):
            if input_grid[i,j] == 0 and output_grid[i,j] != 0:
              # propagation occurred
              if input_grid[i+2,j] == output_grid[i,j]:
                propagation_type = 'expected'
              else:
                propagation_type = 'unexpected'

              report["propagation_details"].append({
                  "row": i,
                  "col": j,
                  "source_row": i + 2,
                  "source_col": j,
                  "input_value": input_grid[i,j],
                  "output_value": output_grid[i,j],
                  "source_value": input_grid[i+2, j],
                  "predicted_value": predicted_grid[i,j],
                  "propagation_type": propagation_type,
              })
            elif input_grid[i,j] == 0 and output_grid[i,j] == 0 and predicted_grid[i,j] != 0:
              # missed propagation
              report["propagation_details"].append({
                    "row": i,
                    "col": j,
                    "source_row": i + 2,
                    "source_col": j,
                    "input_value": input_grid[i, j],
                    "output_value": output_grid[i, j],
                    "source_value": input_grid[i+2,j],
                    "predicted_value": predicted_grid[i,j],
                    "propagation_type": "missed",
                })

    return report

def run_analysis(task_data):
  results = {}
  for example_index, example in enumerate(task_data['train']):
      input_grid = np.array(example['input'])
      output_grid = np.array(example['output'])
      predicted_grid = transform(input_grid) # Use the current transform function
      results[f'example_{example_index}'] = analyze_example(input_grid, output_grid, predicted_grid)
  return results