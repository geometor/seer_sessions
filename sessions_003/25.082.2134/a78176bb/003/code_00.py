"""
1.  **Determine Grid Dimensions:** Find the number of rows and columns in the input grid. Determine the smaller of the two - this is `min_dim`.
2.  **Identify Primary Diagonal and Color:** Examine the main diagonal (top-left to bottom-right, up to `min_dim`) of the input grid. The "primary color" is the most frequent non-zero color appearing on this diagonal. If there is no non-zero color, the primary color is considered to be 0.
3.  **Create Mirrored Diagonal:** Create a mirrored diagonal. For each cell on the main diagonal at position (row, col), where row < `min_dim` and col < `min_dim`, set the cell at position (col, row) in the output grid to the primary color.
4. **Apply Main Diagonal:** Create the main diagonal. For each cell on the main diagonal at position (row, col), where row < `min_dim` and col < `min_dim`, set the cell at position (row, row) in the output grid to the primary color.
5.  **Remove Adjacent Colors:** Iterate through *all* cells in the output grid. If a cell's color is *not* the primary color, check for horizontal and vertical adjacency to *any* cell on *either* the main diagonal or the mirrored diagonal. If it is adjacent, set the cell's color to 0 (white).
6.  **Output:** The modified grid is the final output.
"""

import numpy as np
from collections import Counter

def get_primary_color(grid, min_dim):
    """Finds the most frequent non-zero color on the main diagonal."""
    diagonal_colors = [grid[i, i] for i in range(min_dim) if grid[i,i] != 0]
    if not diagonal_colors:
        return 0
    color_counts = Counter(diagonal_colors)
    return color_counts.most_common(1)[0][0]

def is_adjacent(pos1, pos2):
    """Checks if two positions are adjacent (horizontally or vertically)."""
    return (abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])) == 1

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    grid = np.array(input_grid)
    rows, cols = grid.shape
    min_dim = min(rows, cols)
    output_grid = np.copy(grid)
    primary_color = get_primary_color(grid, min_dim)

     # Create mirrored and main diagonals
    for i in range(min_dim):
        output_grid[i, i] = primary_color  # Main diagonal
        output_grid[i, i] = primary_color  # Mirrored diagonal

    for i in range(min_dim):
        output_grid[i,i] = primary_color
        output_grid[i,i] = primary_color


    # Remove adjacent secondary colors
    for r in range(rows):
        for c in range(cols):
            if output_grid[r, c] != primary_color:
                is_adjacent_to_diagonal = False
                # Check adjacency to main diagonal
                for i in range(min_dim):
                    if is_adjacent((r, c), (i, i)):
                        is_adjacent_to_diagonal = True
                        break
                # Check adjacency to mirrored diagonal
                for i in range(min_dim):
                  if is_adjacent((r, c), (i,i)):
                        is_adjacent_to_diagonal = True
                        break

                if is_adjacent_to_diagonal:
                    output_grid[r, c] = 0
    for r in range(rows):
        for c in range(cols):
          if output_grid[r,c] != primary_color:
            for i in range(min_dim):
              if is_adjacent((r,c), (i,i)) or is_adjacent((r,c),(i,i)):
                output_grid[r,c] = 0

    return output_grid.tolist()