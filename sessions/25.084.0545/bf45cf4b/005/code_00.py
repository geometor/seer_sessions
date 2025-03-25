"""
The transformation identifies "seed" objects, which are the regions that change between the input and output. The bounding box of the seed objects in the *input* defines a region that will be replaced in the output. The replacement pattern is extracted by finding objects that change from input to output, using those to define a rectangular area in the output. This rectangular area from output is repeated across the dimensions of the input seed bounding box. Regions in the input that do not contain the seed are copied to the output unchanged.
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

def find_changing_objects(input_objects, output_objects):
    """Identifies objects that change between input and output."""
    changing_objects = []
    input_object_list = list(input_objects.values())
    output_object_list = list(output_objects.values())
   
    # make sure to do a deep comparison
    for i_obj in input_object_list:
      found = False
      for o_obj in output_object_list:
        if i_obj == o_obj:
          found = True
          break
      if not found:
        changing_objects.append(i_obj)

    return changing_objects

def get_seed_bounds(changing_objects):
  """
  gets the overall bounds that contain all the seed objects
  """
  min_row = min(obj['min_row'] for obj in changing_objects)
  max_row = max(obj['max_row'] for obj in changing_objects)
  min_col = min(obj['min_col'] for obj in changing_objects)
  max_col = max(obj['max_col'] for obj in changing_objects)
  return min_row, max_row, min_col, max_col

def extract_seed_pattern(output_grid, changing_objects):
    """Extracts seed pattern from output, using changed objects bounds."""

    if not changing_objects:
        return None

    min_row, max_row, min_col, max_col = get_seed_bounds(changing_objects)

    seed_pattern = [row[min_col:max_col+1] for row in output_grid[min_row:max_row+1]]
    return np.array(seed_pattern)

def transform(input_grid):
  # initialize grids
  input_grid = np.array(input_grid)
  output_grid = np.copy(input_grid)
  rows, cols = len(input_grid), len(input_grid[0])
    
  # get bounding box for each object in input
  input_objects = get_object_bounds(input_grid)

  # use training pairs to define the seed pattern and target area
  for train_input, train_output in zip(train_inputs, train_outputs):
        
        t_in = np.array(train_input)
        t_out = np.array(train_output)
        
        # bounding boxes for input and output
        t_input_objects = get_object_bounds(t_in)
        t_output_objects = get_object_bounds(t_out)

        # Find objects that change from the training input to output
        t_changing_input_objects = find_changing_objects(t_input_objects, t_output_objects)
        t_changing_output_objects = find_changing_objects(t_output_objects, t_input_objects)


        if not t_changing_input_objects: # if no change, continue
            continue
                
        # Get the seed pattern from the training *output*
        seed_pattern = extract_seed_pattern(t_out,t_changing_output_objects)
        
        # Get the bounds of seed objects from the training *input*
        seed_min_row, seed_max_row, seed_min_col, seed_max_col = get_seed_bounds(t_changing_input_objects)
        
        # get size of output seed
        seed_rows, seed_cols = seed_pattern.shape

        # apply the output seed pattern
        for i in range(seed_min_row, seed_max_row + 1):
            for j in range(seed_min_col, seed_max_col + 1):
                output_grid[i, j] = seed_pattern[(i - seed_min_row) % seed_rows, (j - seed_min_col) % seed_cols]

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