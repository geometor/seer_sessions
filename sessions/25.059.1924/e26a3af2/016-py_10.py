"""
The transformation rule is to retain only the largest horizontal stripes of colors 3 (green), 7 (orange), 8 (azure), and 1 (blue) from the input grid, and remove all other colors/details. The output grid is a simplified version of the input, containing only these specific horizontal bands.
"""

import numpy as np

def get_horizontal_bands(input_grid):
    """
    Identifies and returns horizontal bands of specified colors with lengths > 3.
    """
    rows, cols = input_grid.shape
    target_colors = [3, 7, 8, 1]
    bands = []

    for r in range(rows):
        count = 0
        current_color = -1  # Initialize with a non-target color
        for c in range(cols):
            if input_grid[r, c] in target_colors:
                if input_grid[r, c] == current_color:
                    count += 1
                else:
                    if count > 3:
                         bands.append( (r, c - count, count, current_color) ) # (row, start_col, length, color)
                    current_color = input_grid[r,c]
                    count = 1
            else:
                if count > 3:
                    bands.append( (r, c - count, count, current_color) )
                current_color = -1
                count = 0
        if count > 3:
            bands.append((r, cols - count, count, current_color))
    return bands
                

def transform(input_grid):
    """
    Transforms the input grid by retaining only the major horizontal bands of specific colors (3, 7, 8, and 1)
    and removing other colors, effectively simplifying the grid.
    """
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows, cols), dtype=int)

    # Get horizontal bands
    bands = get_horizontal_bands(input_grid)
    
    # reconstruct based on bands
    for r in range(rows):
        for band_row, band_col, band_len, band_color in bands:
            if r == band_row:
                 output_grid[r, band_col:band_col+band_len] = band_color
        
        
    # fill colors
    for r in range(rows):
        for c in range(cols):
             if output_grid[r,c] == 0:
                  # find closest non zero above
                  for r_scan in range(r -1, -1, -1):
                       if output_grid[r_scan, c] != 0:
                            output_grid[r,c] = output_grid[r_scan, c]
                            break

    return output_grid