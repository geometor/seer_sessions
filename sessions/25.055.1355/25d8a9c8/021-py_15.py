import numpy as np

def get_bottom_row_colors(grid):
    """Returns the unique colors present in the bottom row of the grid."""
    return np.unique(grid[-1, :])

def analyze_example(input_grid, expected_output, predicted_output):
    """Analyzes a single example and returns relevant metrics."""
    input_bottom_colors = get_bottom_row_colors(input_grid)
    expected_bottom_colors = get_bottom_row_colors(expected_output)
    predicted_bottom_colors = get_bottom_row_colors(predicted_output)

    metrics = {
        "input_bottom_colors": input_bottom_colors.tolist(),
        "expected_bottom_colors": expected_bottom_colors.tolist(),
        "predicted_bottom_colors": predicted_bottom_colors.tolist(),
        "match": np.array_equal(expected_output, predicted_output)
    }
    return metrics

# Dummy data for demonstration - replace with actual grids
example_data = [
  {
        "input": np.array([[1, 1, 1], [2, 2, 2], [3, 3, 3]]),
        "output": np.array([[0, 0, 0], [0, 0, 0], [3, 3, 3]]),
        "predicted": np.array([[0, 0, 0], [0, 0, 0], [5, 5, 5]])
  },
  {
        "input": np.array([[4, 4, 4], [5, 5, 5], [6, 6, 7]]),
        "output": np.array([[0, 0, 0], [0, 0, 0], [6, 6, 7]]),
        "predicted": np.array([[0, 0, 0], [0, 0, 0], [5, 5, 5]])
  },
      {
        "input": np.array([[1, 1, 1], [2, 2, 2], [3, 2, 1]]),
        "output": np.array([[0, 0, 0], [0, 0, 0], [3, 2, 1]]),
        "predicted": np.array([[0, 0, 0], [0, 0, 0], [5, 5, 5]])
  }
]
results = []
for ex in example_data:
  results.append(analyze_example(ex["input"],ex["output"],ex["predicted"]))

print(results)
