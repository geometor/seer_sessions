import numpy as np

def analyze_example(input_grid, output_grid):
    input_nonzero_count = np.count_nonzero(input_grid)
    output_nonzero_count = np.count_nonzero(output_grid)
    input_rows, input_cols = input_grid.shape
    output_rows, output_cols = output_grid.shape
    input_nonzero_coords = np.argwhere(input_grid != 0)
    output_nonzero_coords = np.argwhere(output_grid != 0)
    input_nonzero_values = [input_grid[r,c] for r,c in input_nonzero_coords]
    output_nonzero_values = [output_grid[r,c] for r,c in output_nonzero_coords]

    return {
        'input_nonzero_count': input_nonzero_count,
        'output_nonzero_count': output_nonzero_count,
        'input_shape': (input_rows, input_cols),
        'output_shape': (output_rows, output_cols),
        'input_nonzero_coords': input_nonzero_coords.tolist(),
        'output_nonzero_coords': output_nonzero_coords.tolist(),
        'input_nonzero_values': input_nonzero_values,
        'output_nonzero_values': output_nonzero_values,

    }

# Example Input/Output Grids (Replace with actual data from the task)
example_data = [
  (np.array([[0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 1]]),
   np.array([[0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 1]])),

  (np.array([[0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 2, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 3, 0, 0, 0, 0]]),
  np.array([[0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [3, 0, 0, 0, 2, 0]])),

  (np.array([[0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [4, 5, 6, 7, 8, 9]]),
  np.array([[0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [4, 5, 6, 7, 8, 9]])),
 (np.array([[1, 0, 0, 0, 0, 0],
           [0, 2, 0, 0, 0, 0],
           [0, 0, 3, 0, 0, 0],
           [0, 0, 0, 4, 0, 0],
           [0, 0, 0, 0, 5, 0]]),
  np.array([[0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0],
           [1, 2, 3, 4, 5, 0]]))
]

results = [analyze_example(inp, out) for inp, out in example_data]

for i, r in enumerate(results):
  print(f"Example {i+1}:")
  print(r)