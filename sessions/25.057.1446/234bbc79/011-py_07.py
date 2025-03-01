import numpy as np

def calculate_difference(grid1, grid2):
    """Calculates the number of differing pixels between two grids."""
    return np.sum(grid1 != grid2)

def analyze_results(examples, transform_function):
    results = []
    for i, (input_grid, expected_output) in enumerate(examples):
        input_grid = np.array(input_grid)
        expected_output = np.array(expected_output)
        transformed_grid = transform_function(input_grid)
        difference = calculate_difference(transformed_grid, expected_output)
        results.append({
            "example": i + 1,
            "input_shape": input_grid.shape,
            "output_shape": expected_output.shape,
            "transformed_shape": transformed_grid.shape,
            "difference": difference
        })
    return results

# example data (replace with actual data from the task)
examples = [
    ([[5, 0, 5, 5, 5, 5, 5, 5, 5],
  [0, 0, 0, 0, 0, 0, 0, 0, 0],
  [5, 5, 5, 5, 5, 5, 5, 5, 0],
  [5, 5, 5, 5, 5, 5, 5, 5, 0],
  [5, 5, 5, 5, 5, 5, 5, 5, 5]],
 [[5, 0, 5, 5, 5, 5, 5, 5, 5],
  [0, 0, 0, 0, 0, 0, 0, 0, 0],
  [5, 5, 5, 5, 5, 5, 5, 5, 0],
  [5, 5, 5, 5, 5, 5, 5, 5, 0],
  [1, 1, 1, 1, 1, 1, 1, 1, 5]]),

 ([[5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
  [5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 5, 0, 0],
  [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0],
  [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0],
  [5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 5, 0, 0],
  [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]],
 [[5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
  [5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 5, 0, 0],
  [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0],
  [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0],
  [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]),

 ([[5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
  [0, 0, 0, 5, 0, 5, 0, 0, 0, 0, 0, 5, 0, 0, 0],
  [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0],
  [5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0],
  [5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0],
  [5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 5, 0, 0, 0],
  [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]],
 [[5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
  [0, 0, 0, 5, 0, 5, 0, 0, 0, 0, 0, 5, 0, 0, 0],
  [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0],
  [5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0],
  [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
  [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0],
  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])
]

analysis = analyze_results(examples, transform)
for result in analysis:
    print(result)