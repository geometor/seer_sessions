"""
Transforms an input grid by expanding connected regions of foreground pixels horizontally to the right, until a background color or the edge of the grid is encountered. Overwrites any foreground color with the starting pixel of the current run
"""

import numpy as np

def get_foreground_colors(grid):
    """
    Determines the foreground colors by excluding the most frequent (background) color.
    """
    unique_colors, counts = np.unique(grid, return_counts=True)
    background_color = unique_colors[np.argmax(counts)]
    foreground_colors = [color for color in unique_colors if color != background_color]
    return foreground_colors

def transform(input_grid):
    """
    Expands connected regions of foreground colors horizontally to the right within a grid,
    until a background color or the edge is reached.
    """
    grid = np.array(input_grid)
    output_grid = np.copy(grid)
    rows, cols = grid.shape
    
    foreground_colors = get_foreground_colors(grid)

    # Iterate through each row.
    for r in range(rows):
        in_run = False
        start_run_col = -1
        start_run_color = -1

        for c in range(cols):
            # Check if the current pixel is a foreground color.
            if grid[r, c] in foreground_colors:
                if not in_run:
                    # Start a new run.
                    in_run = True
                    start_run_col = c
                    start_run_color = grid[r, c]
            else:
                # Background color or edge encountered.  End the run if any.
                if in_run:
                    for i in range(start_run_col + 1, c):
                        output_grid[r, i] = start_run_color
                    in_run = False
                    start_run_col = -1

        # Handle the case where a run extends to the end of the row.
        if in_run:
            for i in range(start_run_col + 1, cols):
                output_grid[r, i] = start_run_color

    return output_grid.tolist()