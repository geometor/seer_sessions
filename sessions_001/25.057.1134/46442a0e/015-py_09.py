import numpy as np

def get_metrics(input_grid, output_grid, predicted_output_grid):
    """
    Calculates metrics comparing the expected output and the predicted output.
    """
    
    input_pixels = input_grid.size
    output_pixels = output_grid.size
    
    input_colors = np.unique(input_grid)
    output_colors = np.unique(output_grid)
    
    correct_pixels = np.sum(output_grid == predicted_output_grid)
    incorrect_pixels = np.sum(output_grid != predicted_output_grid)
    accuracy = correct_pixels / output_pixels if output_pixels > 0 else 0.0
    
    return {
      'input_pixels': int(input_pixels),
      'output_pixels': int(output_pixels),
      'input_colors': [int(c) for c in input_colors],
      'output_colors': [int(c) for c in output_colors],
      'correct_pixels': int(correct_pixels),
        'incorrect_pixels': int(incorrect_pixels),
        'accuracy': float(accuracy),

    }

def calculate_metrics_for_all(task):
  metrics = []

  for i, example in enumerate(task['train']):
    input_grid = np.array(example['input'])
    output_grid = np.array(example['output'])
    predicted_output_grid = transform(input_grid.copy())
    example_metrics = get_metrics(input_grid, output_grid, predicted_output_grid)
    example_metrics['example_index'] = i
    metrics.append(example_metrics)

  for m in metrics:
    print(m)

task = {
  "train": [
    {
      "input": [[9, 0, 9], [0, 4, 0], [9, 0, 9]],
      "output": [[6, 6, 6, 6, 6, 6], [6, 6, 4, 4, 9, 6], [6, 4, 4, 4, 4, 6], [6, 4, 4, 4, 4, 6], [6, 9, 4, 4, 6, 9], [6, 6, 9, 6, 9, 6]]
    },
    {
      "input": [[0, 9, 0], [9, 4, 9], [0, 9, 0]],
      "output": [[6, 6, 6, 6, 6, 6], [6, 6, 4, 4, 6, 9], [6, 9, 4, 4, 9, 6], [6, 6, 4, 4, 6, 9], [6, 9, 4, 4, 6, 6], [9, 6, 9, 6, 6, 6]]
    },
        {
      "input": [[9,0,0,9],[0,4,4,0],[0,4,4,0],[9,0,0,9]],
      "output": [[6,6,6,6,6,6,6,6],[6,6,4,4,4,4,9,6],[6,4,4,4,4,4,4,6],[6,4,4,4,4,4,4,6],[6,4,4,4,4,4,4,6],[6,4,4,4,4,4,4,6],[6,9,4,4,4,4,6,6],[6,6,9,6,6,6,9,6]]
    }
  ]
}

calculate_metrics_for_all(task)