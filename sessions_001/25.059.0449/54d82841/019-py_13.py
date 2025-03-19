import numpy as np

def get_example_metrics(input_grid, output_grid, predicted_output_grid):
    metrics = {}
    metrics['input_shape'] = input_grid.shape
    metrics['output_shape'] = output_grid.shape
    metrics['predicted_output_shape'] = predicted_output_grid.shape
    metrics['match'] = np.array_equal(output_grid, predicted_output_grid)
    metrics['diff_count'] = np.sum(output_grid != predicted_output_grid)
    #find the first row in input where all pixels are one color
    rows, cols = input_grid.shape
    all_same_row = -1
    for i in range(rows):
      if len(np.unique(input_grid[i])) == 1:
        all_same_row = i
        break

    metrics['all_same_row'] = all_same_row
    metrics['all_same_row_color'] = input_grid[all_same_row, 0] if all_same_row != -1 else -1
    metrics['last_row_color_counts'] = dict(zip(*np.unique(input_grid[-1], return_counts=True)))
        
    return metrics

# Provided examples (Replace with your actual data loading)
train_data = [
  ([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 8, 6, 8, 0, 8, 8, 0, 6, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  ],
  [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 8, 6, 8, 0, 8, 8, 0, 6, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 4, 4, 4, 0, 4, 4, 0, 4, 0, 0]
  ]),
  ([
    [1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1],
    [6, 1, 8, 1, 1, 6],
    [1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0]
  ],
  [
    [1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1],
    [6, 1, 8, 1, 1, 6],
    [1, 1, 1, 1, 1, 1],
    [4, 0, 4, 0, 0, 4]
  ]),
  ([
    [5, 5, 5, 5],
    [8, 5, 8, 6],
    [0, 0, 0, 0]
  ],
  [
    [5, 5, 5, 5],
    [8, 5, 8, 6],
    [4, 0, 4, 4]
  ]),
  ([
     [3, 3, 3, 3, 3, 3, 3],
     [3, 3, 3, 3, 3, 3, 3],
     [3, 3, 3, 3, 3, 3, 3],
     [3, 3, 3, 3, 3, 3, 3],
     [3, 6, 3, 8, 3, 8, 6],
     [0, 0, 0, 0, 0, 0, 0]
  ],
  [
     [3, 3, 3, 3, 3, 3, 3],
     [3, 3, 3, 3, 3, 3, 3],
     [3, 3, 3, 3, 3, 3, 3],
     [3, 3, 3, 3, 3, 3, 3],
     [3, 6, 3, 8, 3, 8, 6],
     [4, 0, 4, 4, 4, 4, 4]
  ]),
    ([
     [2, 2, 2, 2, 2, 2],
     [2, 2, 2, 2, 2, 2],
     [2, 2, 2, 2, 2, 2],
     [2, 2, 2, 2, 2, 2],
     [2, 2, 2, 2, 2, 2],
     [2, 8, 2, 8, 6, 2],
     [0, 0, 0, 0, 0, 0],
  ],
  [
     [2, 2, 2, 2, 2, 2],
     [2, 2, 2, 2, 2, 2],
     [2, 2, 2, 2, 2, 2],
     [2, 2, 2, 2, 2, 2],
     [2, 2, 2, 2, 2, 2],
     [2, 8, 2, 8, 6, 2],
     [4, 4, 4, 4, 4, 4],
  ])
]

# Run the provided transform function
def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Copy the first four rows
    for i in range(min(4,rows)): # added min to fix index out of bounds error for smaller grids
      if i < rows:
        output_grid[i] = input_grid[i]

    # Modify the last row (index 4) based on row 2.
    for c in range(cols):
      if rows > 1 and input_grid[rows-1,c] == 0:  # Check if the pixel in the last row is white, added rows check
          if rows > 3 and (input_grid[2,c] == 8 or input_grid[2,c] == 6):  # Check if the pixel in row 2 is azure or magenta
              output_grid[rows - 1, c] = 4  # Change to yellow

    return output_grid

results = []
for i, (input_grid, output_grid) in enumerate(train_data):
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    predicted_output_grid = transform(input_grid)
    metrics = get_example_metrics(input_grid, output_grid, predicted_output_grid)
    results.append((i, metrics))

for i, metrics in results:
    print(f"Example {i+1}:")
    for k,v in metrics.items():
        print(f"\t{k}: {v}")