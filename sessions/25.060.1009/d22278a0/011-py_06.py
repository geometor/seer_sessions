import numpy as np

def calculate_metrics(input_grid, output_grid, predicted_grid):
    """Calculates metrics comparing the predicted output to the actual output."""

    correct_pixels = np.sum(output_grid == predicted_grid)
    incorrect_pixels = np.sum(output_grid != predicted_grid)
    total_pixels = output_grid.size
    accuracy = correct_pixels / total_pixels if total_pixels > 0 else 0.0

    return {
        'input_shape': input_grid.shape,
        'output_shape': output_grid.shape,
        'predicted_shape': predicted_grid.shape,
        'correct_pixels': correct_pixels,
        'incorrect_pixels': incorrect_pixels,
        'total_pixels': total_pixels,
        'accuracy': accuracy
    }

def show_grid(grid, label):
  """Prints a grid."""
  print(f"--- {label} ---")
  print(grid)

# Example Data (replace with actual data from the ARC task)
# I'm reconstructing these from the problem description.
train_examples = [
    (np.array([[8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
     np.array([[8, 0, 8, 0, 8, 0, 0, 0, 0, 0, 8, 8],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 8],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [8, 8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
     np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8]]),
      np.array([[3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3, 0],
                [0, 3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3],
                [3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3, 0],
                [0, 3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3],
                [3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3, 0],
                [0, 3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3],
                [3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3, 0],
                [0, 3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3],
                [3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3, 0],
                [0, 3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 8]]),
    np.array([[0, 0, 0, 0, 0, 8],
              [0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0]]),
      np.array([[3, 0, 3, 0, 3, 8],
               [0, 3, 0, 3, 0, 3],
               [3, 0, 3, 0, 3, 0],
               [0, 3, 0, 3, 0, 3],
               [3, 0, 3, 0, 3, 0],
               [0, 3, 0, 3, 0, 3]])
    )
]

# Test each example
for i, (input_grid, output_grid) in enumerate(train_examples):
    predicted_grid = transform(input_grid.copy())  # Use a copy to avoid modifying the original
    metrics = calculate_metrics(input_grid, output_grid, predicted_grid)
    print(f"--- Example {i + 1} ---")
    # show_grid(input_grid, 'Input')
    # show_grid(output_grid, 'Expected Output')
    # show_grid(predicted_grid, 'Predicted Output')
    for key, value in metrics.items():
        print(f"{key}: {value}")