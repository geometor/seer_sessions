import numpy as np

def calculate_metrics(input_grid, expected_output, predicted_output):
  """Calculates metrics comparing expected and predicted outputs."""

  metrics = {
      "input_shape": input_grid.shape,
      "expected_output_shape": expected_output.shape,
      "predicted_output_shape": predicted_output.shape,
      "object_colors_input": list(np.unique(input_grid)),
        "object_colors_expected": list(np.unique(expected_output)),
       "object_colors_predicted": list(np.unique(predicted_output)),
      "match": np.array_equal(expected_output, predicted_output)
  }
  return metrics

# Provided examples
examples = [
    (np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 7, 7, 7, 7, 7, 7, 0, 0], [0, 7, 7, 7, 7, 7, 7, 0, 0], [0, 7, 7, 7, 7, 7, 7, 0, 0], [0, 7, 7, 7, 7, 7, 7, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
     np.array([[2, 2, 2, 2, 2, 2, 2], [2, 7, 7, 7, 7, 7, 7, 2], [2, 7, 7, 7, 7, 7, 7, 2], [2, 7, 7, 7, 7, 7, 7, 2], [2, 7, 7, 7, 7, 7, 7, 2], [2, 2, 2, 2, 2, 2, 2]])),
    (np.array([[0, 0, 0, 0, 0, 0], [0, 0, 4, 4, 0, 0], [0, 4, 0, 0, 4, 0], [0, 4, 4, 4, 4, 0], [0, 0, 0, 0, 0, 0]]),
     np.array([[2, 2, 2, 2], [2, 4, 4, 2], [2, 4, 4, 2], [2, 2, 2, 2]])),
    (np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 8, 0], [0, 0, 0, 0, 0, 0, 0, 8, 0], [0, 0, 0, 0, 0, 0, 0, 8, 0], [0, 0, 0, 0, 0, 0, 0, 8, 0], [0, 0, 0, 0, 0, 0, 0, 8, 0], [0, 0, 0, 0, 0, 0, 0, 8, 0], [0, 0, 0, 0, 0, 0, 0, 8, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
     np.array([[2, 2, 2], [2, 8, 2], [2, 8, 2], [2, 8, 2], [2, 8, 2], [2, 8, 2], [2, 8, 2], [2, 8, 2], [2, 2, 2]])),
]

# Assuming 'transform' function is defined elsewhere (from the previous code)

for i, (input_grid, expected_output) in enumerate(examples):
  predicted_output = transform(input_grid)
  metrics = calculate_metrics(input_grid, expected_output, predicted_output)
  print(f"Example {i+1} Metrics:")
  for key, value in metrics.items():
    print(f"  {key}: {value}")