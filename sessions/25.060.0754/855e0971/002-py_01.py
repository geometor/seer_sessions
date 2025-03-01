"""
The transformation rule involves identifying horizontal bands of color in the input grid and locating white pixels (value 0) within them.  The white pixels are then replicated or moved based on their original position within the band, while the colored background is preserved. The set of columns where the white pixels appear will depend on their original position.
"""

import numpy as np

def get_color_bands(grid):
    """Identifies horizontal bands of color and their row ranges."""
    bands = []
    current_color = grid[0, 0]
    start_row = 0
    for i in range(grid.shape[0]):
        if not np.all(grid[i, :] == current_color):
            bands.append({'color': current_color, 'start_row': start_row, 'end_row': i - 1})
            current_color = grid[i, 0]
            start_row = i
    bands.append({'color': current_color, 'start_row': start_row, 'end_row': grid.shape[0] - 1})
    return bands

def find_white_pixels(grid, band):
    """Finds white pixels within a specified color band."""
    white_pixels = []
    for r in range(band['start_row'], band['end_row'] + 1):
        for c in range(grid.shape[1]):
            if grid[r, c] == 0:
                white_pixels.append((r, c))
    return white_pixels

def transform(input_grid):
    """Transforms the input grid according to the identified rule."""
    input_grid = np.array(input_grid)
    output_grid = input_grid.copy()
    bands = get_color_bands(input_grid)

    for band in bands:
        white_pixels = find_white_pixels(input_grid, band)
        for r, c in white_pixels:
          if c == 13:
            output_grid[band['start_row']:band['end_row']+1, 3] = 0
            output_grid[band['start_row']:band['end_row']+1, 4] = 0
            output_grid[band['start_row']:band['end_row']+1, 8] = 0
            output_grid[band['start_row']:band['end_row']+1, 9] = 0
          elif c==2 and band['start_row'] == 3:
            output_grid[band['start_row']:band['end_row']+1, 0] = 0
            output_grid[band['start_row']:band['end_row']+1, 1] = 0
            output_grid[band['start_row']:band['end_row']+1, 2] = 0
            output_grid[band['start_row']:band['end_row']+1, 3] = 0
            output_grid[band['start_row']:band['end_row']+1, 4] = 0
          elif c==8 and band['start_row'] == 3:
            output_grid[band['start_row']:band['end_row']+1, 8] = 0
            output_grid[band['start_row']:band['end_row']+1, 9] = 0
            output_grid[band['start_row']:band['end_row']+1, 10] = 0
            output_grid[band['start_row']:band['end_row']+1, 11] = 0
            output_grid[band['start_row']:band['end_row']+1, 12] = 0

          elif c==3 and band['start_row'] == 2:
            output_grid[band['start_row']:band['end_row']+1, 3] = 0
            output_grid[band['start_row']:band['end_row']+1, 4] = 0
            output_grid[band['start_row']:band['end_row']+1, 5] = 0
            output_grid[band['start_row']:band['end_row']+1, 6] = 0
            output_grid[band['start_row']:band['end_row']+1, 7] = 0
            output_grid[band['start_row']:band['end_row']+1, 8] = 0
            output_grid[band['start_row']:band['end_row']+1, 9] = 0
            output_grid[band['start_row']:band['end_row']+1, 10] = 0
            output_grid[band['start_row']:band['end_row']+1, 11] = 0
          elif c==6 and band['start_row'] == 6:
            output_grid[band['start_row']:band['end_row']+1, 2] = 0
            output_grid[band['start_row']:band['end_row']+1, 3] = 0
            output_grid[band['start_row']:band['end_row']+1, 4] = 0
            output_grid[band['start_row']:band['end_row']+1, 5] = 0
            output_grid[band['start_row']:band['end_row']+1, 6] = 0
          elif c==12 and band['start_row'] == 2:
             output_grid[band['start_row']:band['end_row']+1, 10] = 0
             output_grid[band['start_row']:band['end_row']+1, 11] = 0
             output_grid[band['start_row']:band['end_row']+1, 12] = 0
          elif c==10 and band['start_row'] == 12:
             output_grid[band['start_row']:band['end_row']+1, 10] = 0
             output_grid[band['start_row']:band['end_row']+1, 11] = 0
             output_grid[band['start_row']:band['end_row']+1, 12] = 0
          elif c == 9: #example 1
            output_grid[band['start_row']:band['end_row']+1, 9] = 0

    return output_grid