"""
1.  **Identify "Filler" Colors and Rows:** Find all colors present in the input grid, and the rows in which they appear.
2.  **Fill Rows:** For each identified color (excluding color 0, which represents blank cells), fill the *entire* row(s) where it appears in the *input* grid with that color in the *output* grid.
3.  **Identify Replicating Colors:** Identify colors and rows that are replicated multiple times in the output.
4.  **Replicate Rows and Columns Conditionally**: If the row and column contains color c, then replicate the column in the output grid for all of the rows that contain color c, if there are multiple rows, replicate all.
"""

import numpy as np

def find_colors_and_rows(grid):
    """Finds all colors and their row indices in the grid."""
    grid = np.array(grid)
    height, _ = grid.shape
    color_rows = {}
    for r in range(height):
        for c in range(grid.shape[1]):
            color = grid[r, c]
            if color != 0:
                if color not in color_rows:
                    color_rows[color] = []
                if r not in color_rows[color]:
                    color_rows[color].append(r)
    return color_rows

def find_replicating_colors_and_rows(grid):
    """Finds colors and rows that appear multiple times."""
    grid = np.array(grid)
    height, _ = grid.shape
    color_counts = {}
    row_counts = {}

    for r in range(height):
        for c in range(grid.shape[1]):
           color = grid[r,c]
           if color != 0:
                if color not in color_counts:
                    color_counts[color] = 0
                color_counts[color] +=1

    replicating = {}
    for color, count in color_counts.items():
      if count > 1:
        rows = []
        for r in range(height):
          if color in grid[r,:]:
            rows.append(r)

        if len(rows) > 1:
          replicating[color] = rows

    return replicating

def find_replicating_colors_and_columns(grid, rows_with_color):
    """Finds colors and rows that appear multiple times."""
    grid = np.array(grid)
    _, width = grid.shape

    replicating_cols = {}

    for color in rows_with_color.keys():
      cols = []
      for c in range(width):
        for r in rows_with_color[color]:
            if grid[r,c] == color:
              if c not in cols:
                cols.append(c)
      replicating_cols[color] = cols

    return replicating_cols

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)
    height, width = input_grid.shape

    # Identify "Filler" Colors and Rows
    color_rows = find_colors_and_rows(input_grid)

    # Fill Rows
    for color, rows in color_rows.items():
        for row in rows:
            output_grid[row, :] = color

    #find replicating colors
    replicating_colors = find_replicating_colors_and_rows(output_grid)

    #find replicating columns
    replicating_columns = find_replicating_colors_and_columns(input_grid, replicating_colors)

    # replicate rows based on replicating colors
    for color, rows in replicating_colors.items():
      cols = replicating_columns[color]

      for row in rows:
        for col in cols:
           output_grid[row, col] = input_grid[row,col] if any(input_grid[row, col] == color for row in rows) else output_grid[row,col]



    return output_grid.tolist()