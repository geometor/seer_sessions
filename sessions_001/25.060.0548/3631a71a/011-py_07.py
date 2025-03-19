import numpy as np

def calculate_accuracy(predicted_grid, output_grid):
    """Calculates the pixel-wise accuracy between two grids."""
    return np.sum(predicted_grid == output_grid) / predicted_grid.size

def compare_grids(input_grid, predicted_grid, output_grid):
    """Identifies differences between predicted and expected output grids."""
    diff = np.where(predicted_grid != output_grid)
    
    diff_details = []
    for row, col in zip(diff[0], diff[1]):
        diff_details.append({
            'location': (row, col),
            'input_value': input_grid[row, col],
            'predicted_value': predicted_grid[row, col],
            'output_value': output_grid[row, col]
        })
    return diff_details

def report(task, transform_func):
  results = []
  for i, example in enumerate(task['train']):
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        predicted_grid = transform_func(input_grid)
        accuracy = calculate_accuracy(predicted_grid, output_grid)
        differences = compare_grids(input_grid, predicted_grid, output_grid)
        results.append({
            'example': i,
            'accuracy': accuracy,
            'differences': differences
        })
  return results