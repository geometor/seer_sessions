import numpy as np

def describe_grid(grid):
    """Provides a basic description of the grid."""
    return {
        "shape": grid.shape,
        "unique_colors": np.unique(grid).tolist(),
        "color_counts": {color: np.count_nonzero(grid == color) for color in np.unique(grid)},
    }

def compare_grids(grid1, grid2):
    """Compares two grids and returns differences."""
    if grid1.shape != grid2.shape:
        return "Different shapes"
    diff = grid1 != grid2
    return {
        "different_pixels": np.argwhere(diff).tolist(),
        "num_different_pixels": np.count_nonzero(diff),
    }
examples = task_data['train']

results = []
for i, ex in enumerate(examples):
    input_grid = np.array(ex['input'])
    expected_output_grid = np.array(ex['output'])
    predicted_output_grid = transform(input_grid)
    results.append(
      {
          "example":i,
          "input": describe_grid(input_grid),
          "expected_output": describe_grid(expected_output_grid),
          "predicted_output": describe_grid(predicted_output_grid),
          "comparison_expected_predicted": compare_grids(expected_output_grid, predicted_output_grid),
      }
    )
print(results)
