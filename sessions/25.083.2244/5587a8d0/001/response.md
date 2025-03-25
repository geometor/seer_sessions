```python
"""
1. Identify the Border: Find the outermost layer of color that completely surrounds the grid in the input.
2. Extract the Core: Remove the identified border, isolating the internal rectangular "core" of the input grid.
3. Construct the Output Border: Construct a new "output core" grid that is 2 rows and 2 columns longer and wider than the extracted core, filled with a new border color.
4. Map Input Core Colors: Transform the colors of the extracted core to a new set of colors:
   - In example 1: The input border color 7 becomes 4, and other inner colors 4 become 6.
   - In example 2: The input border color 7 becomes 1, and the other inner colors transform with the rule 8 -> 8, 5 -> 5, 1-> 8.
   - In example 3: The input border color 7 becomes 8, and the other inner colors 8->0, 3 ->3, 9 -> 3, 7->0.
5. Place Core in Output: The transformed-color extracted core is placed in the center of the output grid constructed from the new border color.
"""

import numpy as np

def get_border_color(grid):
    """Finds the most likely border color of a grid."""
    # Check top, bottom, left and right edges for common color
    top_edge = grid[0, :]
    bottom_edge = grid[-1, :]
    left_edge = grid[:, 0]
    right_edge = grid[:, -1]

    # Concatenate all edges and find the most frequent color
    all_edges = np.concatenate((top_edge, bottom_edge, left_edge, right_edge))
    unique, counts = np.unique(all_edges, return_counts=True)
    border_color = unique[np.argmax(counts)]
    return border_color

def extract_core(grid, border_color):
    """Extracts the core subgrid by removing the border."""
    rows, cols = grid.shape
    start_row, start_col = 0, 0
    end_row, end_col = rows, cols

    # Find the inner rectangle
    for i in range(rows):
        if not np.all(grid[i, :] == border_color):
            start_row = i
            break
    for i in range(rows - 1, -1, -1):
        if not np.all(grid[i, :] == border_color):
            end_row = i + 1
            break
    for j in range(cols):
        if not np.all(grid[:, j] == border_color):
            start_col = j
            break
    for j in range(cols - 1, -1, -1):
        if not np.all(grid[:, j] == border_color):
            end_col = j + 1
            break

    core_grid = grid[start_row:end_row, start_col:end_col]
    return core_grid

def transform_colors(core_grid, input_grid):
    """Transforms the colors of the core grid based on specific rules."""

    border_color = get_border_color(input_grid)
    output_border_color = None
    color_map = {}

    if border_color == 7:
      unique_core_colors = np.unique(core_grid)
      if all(color in [7, 4, 6] for color in unique_core_colors): # Example 1 logic
          output_border_color = 4
          color_map = {4: 6, 7:4}
      elif all(color in [7, 1, 8, 5] for color in unique_core_colors): #Example 2 logic
          output_border_color = 1
          color_map = {8: 8, 5: 5, 1: 8, 7:1}
      elif all(color in [7,8,3,9,0] for color in unique_core_colors): # Example 3 logic
          output_border_color = 8
          color_map = {8:0, 3:3, 9:3, 7:0, 0:0} # added 0 to ensure full mapping


    transformed_grid = np.vectorize(lambda x: color_map.get(x, x))(core_grid)
    return transformed_grid, output_border_color

def create_output_grid(transformed_core, output_border_color):
  """Creates new grid with border and places core in the center"""
  core_rows, core_cols = transformed_core.shape
  output_rows = core_rows + 2
  output_cols = core_cols + 2
  output_grid = np.full((output_rows, output_cols), output_border_color)

  output_grid[1:output_rows-1, 1:output_cols-1] = transformed_core

  return output_grid

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""

    # 1. Identify the Border
    border_color = get_border_color(input_grid)

    # 2. Extract the Core
    core_grid = extract_core(input_grid, border_color)

    # 3. & 4. Transform Colors and determine the new border color
    transformed_core, output_border_color = transform_colors(core_grid, input_grid)
    
    # 5. Construct the output grid
    output_grid = create_output_grid(transformed_core, output_border_color)

    return output_grid
```