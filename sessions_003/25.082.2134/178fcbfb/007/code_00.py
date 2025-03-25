"""
1.  **Identify Colors and Positions:** For each color (excluding 0) in the input grid, record the rows and columns in which it appears.
2.  **Fill Rows:** For each identified color, fill the *entire* row(s) where it appears in the *input* grid with that color in the *output* grid.
3. **Identify rows that contain more than one instance of any color**: Record these colors.
4. **Stretch:** If there are multiple rows with color c, then replicate columns from the original grid that contains color c in any of the identified rows into *all* rows in the output identified.
"""

import numpy as np

def find_colors_and_positions(grid):
    """Finds all colors and their row/column indices in the grid."""
    grid = np.array(grid)
    height, width = grid.shape
    color_positions = {}
    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            if color != 0:
                if color not in color_positions:
                    color_positions[color] = {"rows": [], "columns": []}
                if r not in color_positions[color]["rows"]:
                    color_positions[color]["rows"].append(r)
                if c not in color_positions[color]["columns"]:
                    color_positions[color]["columns"].append(c)
    return color_positions

def find_replicating_colors(grid):
    """Find colors present in multiple rows."""
    color_positions = find_colors_and_positions(grid)
    replicating_colors = {}

    for color, positions in color_positions.items():
        if len(positions["rows"]) > 1:
          replicating_colors[color] = positions["rows"]
    return replicating_colors
    

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)
    height, width = input_grid.shape

    # Identify Colors and Positions
    color_positions = find_colors_and_positions(input_grid)

    # Fill Rows
    for color, positions in color_positions.items():
        for row in positions["rows"]:
            output_grid[row, :] = color

    #Find replicating colors
    replicating = find_replicating_colors(input_grid)

    # Stretch
    for color, rows in replicating.items():
      for r in rows:
        for c in color_positions[color]["columns"]:
          for row_to_fill in rows:
              output_grid[row_to_fill,c] = input_grid[r,c]

    return output_grid.tolist()