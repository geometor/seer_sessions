"""
1.  **Identify the Primary Diagonal:** Find the diagonal line of pixels running from the top-left corner to the bottom-right corner of the input grid. Note the color of these pixels (the "primary color").

2.  **Mirror the Diagonal:** Create a mirrored diagonal by placing pixels of the primary color at positions that are reflections of the original diagonal across the center of the grid. Specifically, if a pixel on the main diagonal is at position (row, column), place a pixel of the same color at (column, row).

3.  **Remove Adjacent Secondary Colors:** Any pixels *not* of the primary color that are *horizontally or vertically* adjacent to either the original diagonal or the mirrored diagonal are set to 0 (white). In other words, remove any secondary color pixels that "touch" the main diagonal or its reflection.

4. **Output result:** The resulting grid is the output.
"""

import numpy as np

def get_primary_diagonal_color(grid):
    """Finds the color of the primary diagonal."""
    for i in range(len(grid)):
        if grid[i][i] != 0:
            return grid[i][i]
    return 0  # Should not happen in well-formed inputs

def is_adjacent(pos1, pos2):
    """Checks if two positions are adjacent (horizontally or vertically)."""
    return (abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])) == 1

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    grid = np.array(input_grid)  # Use numpy for easier manipulation
    rows, cols = grid.shape
    output_grid = np.copy(grid)
    primary_color = get_primary_diagonal_color(grid)

    # Mirror the diagonal
    for i in range(rows):
        if grid[i,i] == primary_color:
            output_grid[i, i] = primary_color
            output_grid[i, i] = primary_color  # original
            output_grid[i,i] = primary_color
            output_grid[i,i] = primary_color
            output_grid[i, i] = primary_color #main diagonal
            output_grid[i,i] = primary_color
            output_grid[i, i] = primary_color

    for i in range(rows):
      output_grid[i,i] = primary_color
      output_grid[i, i] = primary_color  # original
      output_grid[i,i] = primary_color
      output_grid[i,i] = primary_color
      output_grid[i, i] = primary_color #main diagonal
      output_grid[i,i] = primary_color
      output_grid[i, i] = primary_color


    for r in range(rows):
        for c in range(cols):
            output_grid[c, r] = primary_color if grid[r,r] == primary_color else output_grid[c,r]


    # Remove adjacent secondary colors
    for r in range(rows):
        for c in range(cols):
            if output_grid[r, c] != primary_color:
                is_adjacent_to_diagonal = False
                # Check adjacency to main diagonal
                for i in range(rows):
                    if is_adjacent((r, c), (i, i)):
                        is_adjacent_to_diagonal = True
                        break
                # Check adjacency to mirrored diagonal
                for i in range(rows):
                    if is_adjacent((r, c), (i,i)):
                        is_adjacent_to_diagonal = True
                        break

                if is_adjacent_to_diagonal:
                    output_grid[r, c] = 0

    return output_grid.tolist()