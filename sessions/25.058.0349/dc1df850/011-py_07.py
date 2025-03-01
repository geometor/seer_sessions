import numpy as np

def analyze_grid(grid):
    """Analyzes a grid and returns relevant metrics."""
    height, width = grid.shape
    unique, counts = np.unique(grid, return_counts=True)
    color_counts = dict(zip(unique, counts))
    red_count = color_counts.get(2, 0)
    blue_count = color_counts.get(1, 0)
    return {
        'height': height,
        'width': width,
        'red_count': red_count,
        'blue_count': blue_count,
        'color_counts': color_counts
    }

def calculate_iou(predicted_grid, ground_truth_grid):
    """Calculates the Intersection over Union (IoU) for two grids."""
    intersection = np.sum((predicted_grid == ground_truth_grid) & (predicted_grid != 0))
    union = np.sum((predicted_grid != 0) | (ground_truth_grid != 0))
    if union==0:
        return 1.0
    return intersection / union if union > 0 else 0.0

def analyze_results(task):
  results = []
  for example in task['train']:
    input_grid = np.array(example['input'])
    output_grid = np.array(example['output'])    
    predicted_grid = transform(input_grid.copy())
    iou = calculate_iou(predicted_grid, output_grid)
    results.append({
        'input': analyze_grid(input_grid),
        'output': analyze_grid(output_grid),
        'predicted': analyze_grid(predicted_grid),
        'iou': iou
    })
  return results