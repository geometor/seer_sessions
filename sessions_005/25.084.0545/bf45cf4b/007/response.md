```python
"""
The transformation identifies a region of change in the input and replaces it with a pattern extracted from the output. For the special case where the changed region is the bottom-right quadrant, it performs a 2x upscale of that quadrant. Otherwise, it identifies a repeating pattern from output change region and repeats.
"""

import numpy as np

def get_object_bounds(grid):
    """
    Find bounding boxes of connected regions

    returns a dictionary
    """

    visited = set()
    objects = {}

    rows, cols = len(grid), len(grid[0])

    def dfs(row, col, color, object_id):
        if (
            row < 0
            or row >= rows
            or col < 0
            or col >= cols
            or (row, col) in visited
            or grid[row][col] != color
        ):
            return []

        visited.add((row, col))
        coords = [(row, col)]

        coords.extend(dfs(row + 1, col, color, object_id))
        coords.extend(dfs(row - 1, col, color, object_id))
        coords.extend(dfs(row, col + 1, color, object_id))
        coords.extend(dfs(row, col - 1, color, object_id))

        return coords

    object_id_counter = 0
    for row in range(rows):
        for col in range(cols):
            if (row, col) not in visited:
                color = grid[row][col]
                object_coords = dfs(row, col, color, object_id_counter)

                min_row = min(object_coords, key=lambda x: x[0])[0]
                max_row = max(object_coords, key=lambda x: x[0])[0]
                min_col = min(object_coords, key=lambda x: x[1])[1]
                max_col = max(object_coords, key=lambda x: x[1])[1]

                objects[object_id_counter] = {
                    "color": color,
                    "min_row": min_row,
                    "max_row": max_row,
                    "min_col": min_col,
                    "max_col": max_col,
                }
                object_id_counter += 1

    return objects

def find_changing_pixels(input_grid, output_grid):
    """Finds coordinates of pixels that change between input and output."""
    changing_pixels = []
    for i in range(len(input_grid)):
        for j in range(len(input_grid[0])):
            if input_grid[i][j] != output_grid[i][j]:
                changing_pixels.append((i, j))
    return changing_pixels

def get_bounds(coords):
    """Gets the bounding box of a list of coordinates."""
    if not coords:
        return None
    min_row = min(coords, key=lambda x: x[0])[0]
    max_row = max(coords, key=lambda x: x[0])[0]
    min_col = min(coords, key=lambda x: x[1])[1]
    max_col = max(coords, key=lambda x: x[1])[1]
    return min_row, max_row, min_col, max_col

def quadrant_replication(input_grid):
  """
  replicates the bottom-right quadrant
  """
  input_grid = np.array(input_grid)
  rows, cols = input_grid.shape
  mid_row, mid_col = rows // 2, cols // 2
  quadrant = input_grid[mid_row:, mid_col:]
  return np.kron(quadrant, np.ones((2, 2))).tolist()

def get_output_dimensions(input_grid, seed_region_input, seed_pattern_output):
    """Calculates output dimensions."""
    
    in_rows, in_cols = len(input_grid), len(input_grid[0])
    pattern_h = len(seed_pattern_output)
    out_rows =  seed_region_input[0] + pattern_h
   
    return out_rows, in_cols


def transform(input_grid):
  # initialize output_grid
  input_grid = np.array(input_grid)
  in_rows, in_cols = input_grid.shape

  # use training pairs to define the seed pattern and target area
  for train_input, train_output in zip(train_inputs, train_outputs):
        
        t_in = np.array(train_input)
        t_out = np.array(train_output)

        # Find changing pixels
        t_changing_pixels_input = find_changing_pixels(t_in, t_out)
        t_changing_pixels_output = find_changing_pixels(t_out, t_in)

        # Get bounds of changing pixels
        t_in_seed_min_row, t_in_seed_max_row, t_in_seed_min_col, t_in_seed_max_col = get_bounds(t_changing_pixels_input)
        t_out_seed_min_row, t_out_seed_max_row, t_out_seed_min_col, t_out_seed_max_col = get_bounds(t_changing_pixels_output)
                
        # check for quadrant repl
        if (t_in_seed_min_row == in_rows // 2 and t_in_seed_min_col == in_cols // 2 and
            t_in_seed_max_row == in_rows - 1 and t_in_seed_max_col == in_cols - 1):
          return quadrant_replication(input_grid)

  # extract sub_grid, get dimensions and calc output size
  t_seed_pattern = t_out[t_out_seed_min_row:t_out_seed_max_row+1, t_out_seed_min_col:t_out_seed_max_col+1]

  # output size
  out_rows, out_cols = get_output_dimensions(t_in,(t_in_seed_min_row, t_in_seed_max_row, t_in_seed_min_col, t_in_seed_max_col), t_seed_pattern)  
  output_grid = np.full((out_rows, out_cols), -1, dtype=int)  # Initialize with -1
 
  # copy unchanged
  for i in range(min(in_rows, out_rows)):
        for j in range(min(in_cols,out_cols)):
          if i < t_in_seed_min_row or i > t_in_seed_max_row or j < t_in_seed_min_col or j > t_in_seed_max_col:
            if i < out_rows and j < out_cols: # Check output bounds
              output_grid[i,j] = input_grid[i,j]


    # replicate pattern
  seed_h, seed_w = t_seed_pattern.shape
  for i in range(t_in_seed_min_row, min(t_in_seed_max_row + 1,out_rows)): # Limit by output rows
      for j in range(t_in_seed_min_col, min(t_in_seed_max_col + 1, out_cols)): # Limit by output cols
          output_grid[i, j] = t_seed_pattern[(i - t_in_seed_min_row) % seed_h, (j - t_in_seed_min_col) % seed_w]


  return output_grid.tolist()

# store training pairs globally
train_inputs = [
    [
        [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        [4, 4, 4, 4, 4, 4, 2, 2, 4, 2, 4, 4],
        [4, 4, 4, 4, 4, 4, 2, 4, 2, 2, 4, 4],
        [4, 4, 4, 4, 4, 4, 4, 2, 4, 2, 4, 4],
        [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        [4, 8, 3, 8, 4, 4, 4, 4, 4, 4, 4, 4],
        [4, 3, 4, 3, 4, 4, 4, 4, 4, 4, 4, 4],
        [4, 8, 3, 8, 4, 4, 4, 4, 4, 4, 4, 4],
        [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
    ],
    [
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 1, 1, 1, 3, 3, 3, 8, 8, 8, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 8, 2, 8, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 8, 8, 8, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
    ],
[
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 6, 6, 6, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 6, 1, 6, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 8, 9, 9, 8, 1, 1, 1],
        [1, 1, 1, 1, 1, 9, 4, 4, 9, 1, 1, 1],
        [1, 1, 1, 1, 1, 9, 4, 4, 9, 1, 1, 1],
        [1, 1, 1, 1, 1, 8, 9, 9, 8, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]
]

train_outputs = [
  [
    [8, 3, 8, 8, 3, 8, 4, 4, 4, 8, 3, 8],
    [3, 4, 3, 3, 4, 3, 4, 4, 4, 3, 4, 3],
    [8, 3, 8, 8, 3, 8, 4, 4, 4, 8, 3, 8],
    [8, 3, 8, 4, 4, 4, 8, 3, 8, 8, 3, 8],
    [3, 4, 3, 4, 4, 4, 3, 4, 3, 3, 4, 3],
    [8, 3, 8, 4, 4, 4, 8, 3, 8, 8, 3, 8],
    [4, 4, 4, 8, 3, 8, 4, 4, 4, 8, 3, 8],
    [4, 4, 4, 3, 4, 3, 4, 4, 4, 3, 4, 3],
    [4, 4, 4, 8, 3, 8, 4, 4, 4, 8, 3, 8],
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
],
  [
        [8, 8, 8, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [8, 2, 8, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [8, 8, 8, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 8, 8, 8, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 8, 2, 8, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 8, 8, 8, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 8, 8, 8, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 8, 2, 8, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 8, 8, 8, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
    ],
[
        [8, 9, 9, 8, 8, 9, 9, 8, 8, 9, 9, 8],
        [9, 4, 4, 9, 9, 4, 4, 9, 9, 4, 4, 9],
        [9, 4, 4, 9, 9, 4, 4, 9, 9, 4, 4, 9],
        [8, 9, 9, 8, 8, 9, 9, 8, 8, 9, 9, 8],
        [8, 9, 9, 8, 1, 1, 1, 1, 8, 9, 9, 8],
        [9, 4, 4, 9, 1, 1, 1, 1, 9, 4, 4, 9],
        [9, 4, 4, 9, 1, 1, 1, 1, 9, 4, 4, 9],
        [8, 9, 9, 8, 1, 1, 1, 1, 8, 9, 9, 8],
        [1, 1, 1, 1, 8, 9, 9, 8, 1, 1, 1, 1],
        [1, 1, 1, 1, 9, 4, 4, 9, 1, 1, 1, 1],
        [1, 1, 1, 1, 9, 4, 4, 9, 1, 1, 1, 1],
        [1, 1, 1, 1, 8, 9, 9, 8, 1, 1, 1, 1]
    ]

]
```