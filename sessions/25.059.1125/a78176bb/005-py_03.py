import numpy as np

def get_grid_metrics(grid):
    """Calculates and returns metrics for a given grid."""
    metrics = {}
    metrics['shape'] = grid.shape
    metrics['unique_colors'] = np.unique(grid).tolist()
    metrics['color_counts'] = {color: int(np.sum(grid == color)) for color in metrics['unique_colors']}
    return metrics

#Provided code for transform.
def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Remove non-diagonal elements (specifically the 2x2 block)
    for i in range(rows):
        for j in range(cols):
            if i != j and output_grid[i, j] != 0:
                output_grid[i,j] = 0

    # Add the top-right to bottom-left diagonal
    for i in range(rows):
        for j in range(cols):
          if i + j == rows -1:
            output_grid[i,j] = 7

    return output_grid

# Example grids and results (replace with actual data from prompt)

# Example 1
input_grid_1 = np.array([[7, 5, 5], [5, 7, 5], [5, 5, 7]])
output_grid_1 = np.array([[7, 0, 7], [0, 7, 0], [7, 0, 7]])
result_grid_1 = transform(input_grid_1)

# Example 2
input_grid_2 = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
output_grid_2 = np.array([[7, 0, 0, 7], [0, 7, 7, 0], [0, 7, 7, 0], [7, 0, 0, 7]])
result_grid_2 = transform(input_grid_2)

# Example 3
input_grid_3 = np.array([[0, 0, 0, 0, 2], [0, 0, 0, 2, 0], [0, 0, 2, 0, 0], [0, 2, 0, 0, 0], [2, 0, 0, 0, 0]])
output_grid_3 = np.array([[0, 0, 0, 0, 7], [0, 0, 0, 7, 0], [0, 0, 7, 0, 0], [0, 7, 0, 0, 0], [7, 0, 0, 0, 0]])
result_grid_3 = transform(input_grid_3)

examples = [
      (input_grid_1, output_grid_1, result_grid_1),
      (input_grid_2, output_grid_2, result_grid_2),
      (input_grid_3, output_grid_3, result_grid_3),
]
print ("Example, Input Metrics, Output Metrics, Result Metrics")

for i, grids in enumerate(examples):
  input_metrics = get_grid_metrics(grids[0])
  output_metrics = get_grid_metrics(grids[1])
  result_metrics = get_grid_metrics(grids[2])

  print (f"Example {i + 1}:")
  print (f"{input_metrics=}")
  print (f"{output_metrics=}")
  print (f"{result_metrics=}")
