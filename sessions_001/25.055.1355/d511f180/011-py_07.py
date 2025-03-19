import numpy as np

def analyze_grid(grid):
    """Analyzes a grid and returns relevant metrics."""
    unique_colors = np.unique(grid)
    num_colors = len(unique_colors)
    color_counts = {color: np.sum(grid == color) for color in unique_colors}
    rows, cols = grid.shape
    return {
        'shape': (rows, cols),
        'unique_colors': unique_colors.tolist(),
        'num_colors': num_colors,
        'color_counts': color_counts
    }

def analyze_example(example):
  return {
      'input': analyze_grid(np.array(example['input'])),
      'output': analyze_grid(np.array(example['output'])),
      'predicted': analyze_grid(transform(np.array(example['input'])))

  }

examples = task['train']
analysis_results = [analyze_example(example) for example in examples]
print(analysis_results)
