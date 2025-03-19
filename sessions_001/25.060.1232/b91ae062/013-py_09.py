import numpy as np

def describe_grid(grid):
    """Provides a concise description of a grid."""
    return {
        'shape': grid.shape,
        'unique_colors': np.unique(grid).tolist(),
        'size': grid.size,
    }

def compare_grids(grid1, grid2):
    """Compares two grids and highlights differences."""
    if grid1.shape != grid2.shape:
        return "Shapes are different"
    else:
        diff = grid1 != grid2
        if np.any(diff):
            diff_indices = np.where(diff)
            diff_details = []
            for i in range(len(diff_indices[0])):
                row, col = diff_indices[0][i], diff_indices[1][i]
                diff_details.append({
                    'location': (row, col),
                    'grid1_value': grid1[row, col],
                    'grid2_value': grid2[row, col]
                })

            return {
               'message': "values are different",
               'differences': diff_details
            }

        else:
            return "Grids are identical"

# Load the training data
task_data = {
    "train": [
        {
            "input": np.array([[1, 2], [3, 4]]),
            "output": np.array([[1, 1, 2, 2], [1, 1, 2, 2], [3, 3, 4, 4], [3, 3, 4, 4]]),
        },
        {
            "input": np.array([[5, 6, 7], [8, 9, 0]]),
            "output": np.array([[5, 5, 6, 6, 7, 7], [5, 5, 6, 6, 7, 7], [8, 8, 9, 9, 0, 0], [8, 8, 9, 9, 0, 0]]),
        },
        {
            "input": np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]]),
            "output": np.array([[1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1]]),
        },
        {
            "input": np.array([[2, 2], [2, 2]]),
            "output": np.array([[2, 2, 2, 2], [2, 2, 2, 2], [2, 2, 2, 2], [2, 2, 2, 2]]),
        }

    ]
}

# Existing transform function
def transform(input_grid):
    input_height, input_width = input_grid.shape
    output_height, output_width = input_height * 2, input_width * 2
    output_grid = np.zeros((output_height, output_width), dtype=int)
    for row in range(input_height):
        for col in range(input_width):
            color = input_grid[row, col]
            output_grid[2*row:2*row+2, 2*col:2*col+2] = color
    return output_grid

results = []
for i, example in enumerate(task_data['train']):
  input_grid = example['input']
  expected_output = example['output']
  predicted_output = transform(input_grid)
  comparison = compare_grids(predicted_output, expected_output)
  results.append(
      {
         'example': i,
         'input': describe_grid(input_grid),
         'expected_output': describe_grid(expected_output),
         'predicted_output': describe_grid(predicted_output),
         'comparison_result': comparison
      }
  )

print(results)
