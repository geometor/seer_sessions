import numpy as np

# Dummy results data (replace with actual data from execution)
# THIS BLOCK WILL BE REPLACED WITH ACTUAL DATA DURING CODE EXECUTION. I'M
# CREATING A BEST GUESS TO ALLOW THE PROCESS TO CONTINUE
# Example Data (assuming a simple stretching transformation for illustration)

task_data = {
    "train": [
        {
            "input": [[1, 1], [1, 1]],
            "output": [[1, 1, 1, 1], [1, 1, 1, 1]],
        },
        {
            "input": [[2,2,2],[2,2,2]],
            "output": [[2,2,2,2,2,2],[2,2,2,2,2,2]]
        },
         {
            "input": [[3],[3],[3]],
            "output": [[3,3],[3,3],[3,3]]
        }
    ]
}
def describe_grid(grid):
    """Provides a basic description of the grid."""
    return {
        "shape": np.array(grid).shape,
        "unique_colors": np.unique(grid).tolist(),
        "color_counts": {color: np.count_nonzero(grid == color) for color in np.unique(grid)},
    }

def compare_grids(grid1, grid2):
    """Compares two grids and returns differences."""
    if np.array(grid1).shape != np.array(grid2).shape:
        return "Different shapes"
    diff = np.array(grid1) != np.array(grid2)
    return {
        "different_pixels": np.argwhere(diff).tolist(),
        "num_different_pixels": np.count_nonzero(diff),
    }
# Placeholder transform function (initially an identity function).
def transform(grid):
  return grid

examples = task_data['train']

results = []
for i, ex in enumerate(examples):
    input_grid = np.array(ex['input'])
    expected_output_grid = np.array(ex['output'])
    predicted_output_grid = transform(input_grid)  # Use the current transform function
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
