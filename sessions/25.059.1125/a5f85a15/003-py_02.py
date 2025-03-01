import numpy as np

def compare_grids(grid1, grid2):
    """Compares two grids and returns a detailed report."""
    if grid1.shape != grid2.shape:
        return "Grids have different shapes."

    diff = grid1 != grid2
    num_diffs = np.sum(diff)
    diff_indices = np.where(diff)
    diff_report = []

    for i in range(num_diffs):
        row = diff_indices[0][i]
        col = diff_indices[1][i]
        diff_report.append(
            f"Pixel mismatch at ({row}, {col}): Expected {grid2[row, col]}, Got {grid1[row, col]}"
        )
    
    report = {
      'num_differences': num_diffs,
      'details': diff_report,
      'same': num_diffs == 0
    }

    return report

# Example usage with the provided transform function (assuming it's defined as above)
# Assume train_in_0, train_out_0 etc. hold the training inputs and outputs as numpy arrays

task = '6fa7a44f' # this would be loaded from the json in the full run

import json
with open('data/training/' + task + '.json', 'r') as f:
    task_data = json.load(f)

train_examples = task_data['train']
train_results = []
for i, ex in enumerate(train_examples):
  train_in = np.array(ex['input'])
  train_out = np.array(ex['output'])
  predicted_output = transform(train_in)
  comparison_result = compare_grids(predicted_output, train_out)
  train_results.append(
      {
          'example_index': i,
          'comparison': comparison_result
      }
  )

print(train_results)
