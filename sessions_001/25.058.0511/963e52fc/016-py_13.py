"""
The transformation rule involves identifying colored bands (alternating blue (1) and red (2) pixels) and stretching them. Horizontal bands are stretched horizontally, and vertical bands are stretched vertically. The stretching factor is 2x, meaning each column in a horizontal band is duplicated, and each row in a vertical band is duplicated.
"""

import numpy as np

def find_colored_bands(grid):
    rows, cols = grid.shape
    horizontal_bands = []
    vertical_bands = []

    # Find horizontal bands
    for r in range(rows):
        row = grid[r]
        is_horizontal_band = False
        if row[0] == 1 or row[0] == 2:  # Check start of band
            is_horizontal_band = True
            for i in range(cols - 1):
                if row[i] == row[i + 1] or (row[i] != 1 and row[i] != 2):
                    is_horizontal_band = False
                    break
        if is_horizontal_band:
            horizontal_bands.append(r)

    # Find vertical bands (transpose the grid for easier processing)
    transposed_grid = grid.T
    rows_t, cols_t = transposed_grid.shape
    for r in range(rows_t):
        row = transposed_grid[r]
        is_vertical_band = False

        if row[0] == 1 or row[0] == 2:  # Check start of band
            is_vertical_band = True
            for i in range(cols_t - 1):
                if row[i] == row[i+1] or (row[i]!=1 and row[i] != 2):
                    is_vertical_band = False
                    break

        if is_vertical_band:
            vertical_bands.append(r)
    return horizontal_bands, vertical_bands
def transform(input_grid):
    rows, cols = input_grid.shape

    horizontal_bands, vertical_bands = find_colored_bands(input_grid)

    # Initialize output_grid based on whether there are horizontal or vertical bands
    if horizontal_bands:
      output_grid = np.zeros((rows, cols * 2), dtype=int)
    elif vertical_bands:
      output_grid = np.zeros((rows*2, cols), dtype=int)
    else: # handles edge case if not band is found - no stretching
      return input_grid


    # Handle horizontal stretching
    if horizontal_bands:
        for r in range(rows):
            if r not in horizontal_bands:
              # Copy background rows directly, doubling the width
              for c in range(cols):
                output_grid[r, c*2] = input_grid[r,c]
                output_grid[r, c*2 + 1] = input_grid[r,c]
            else:
                # Stretch the colored band rows
                for c in range(cols):
                    output_grid[r, 2 * c] = input_grid[r, c]
                    output_grid[r, 2 * c + 1] = input_grid[r, c]

    # Handle vertical stretching
    if vertical_bands:
      for c in range(cols):
        if c not in vertical_bands:
          for r in range(rows):
            output_grid[r*2,c] = input_grid[r,c]
            output_grid[r*2+1, c] = input_grid[r,c]
        else:
          for r in range(rows):
            output_grid[2*r, c] = input_grid[r,c]
            output_grid[2*r + 1, c] = input_grid[r,c]


    return output_grid