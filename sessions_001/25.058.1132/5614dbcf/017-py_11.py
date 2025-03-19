import numpy as np

def calculate_metrics(input_grid, output_grid, predicted_output_grid):
    """Calculates evaluation metrics for a single example."""
    correct_pixels = np.sum(output_grid == predicted_output_grid)
    total_pixels = output_grid.size
    accuracy = correct_pixels / total_pixels if total_pixels > 0 else 0.0
    return accuracy

def report_metrics(task, transform_func):
    train_examples = task['train']
    num_examples = len(train_examples)
    print(f"Number of Examples: {num_examples}")
    for i in range(num_examples):
      input_grid = np.array(train_examples[i]['input'])
      output_grid = np.array(train_examples[i]['output'])
      predicted_output_grid = transform_func(input_grid)
      accuracy = calculate_metrics(input_grid, output_grid, predicted_output_grid)
      print(f"Example {i+1}:")
      print(f"  Input shape: {input_grid.shape}")
      print(f"  Output shape: {output_grid.shape}")
      print(f"  Predicted Output shape: {predicted_output_grid.shape}")
      print(f"  Accuracy: {accuracy:.4f}")