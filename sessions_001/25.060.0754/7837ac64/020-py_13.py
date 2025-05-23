"""
The program identifies rows in the input grid that contain magenta (6) or green (3) pixels.
It extracts these colored pixels and represents them in a 3x3 output grid.
Magenta rows are represented by magenta, green rows by green, and rows without 6 or 3 appear before those in the input are white.
"""

import numpy as np

def extract_key_pixels(row):
    # Extract magenta(6) and green(3) pixels from a row
    key_pixels = []
    for pixel in row:
        if pixel == 6 or pixel == 3:
            key_pixels.append(pixel)
    return key_pixels

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((3, 3), dtype=int)
    rows, _ = input_grid.shape
    
    key_rows = []
    # Find rows and pixels
    for r in range(rows):
       extracted = extract_key_pixels(input_grid[r])
       if (len(extracted) > 0):
          key_rows.append( (r, extracted) )

    # fill first row
    if len(key_rows) >= 1:
        first_row_pixels = key_rows[0][1]
        if all(pixel == 6 for pixel in first_row_pixels):
           output_grid[0,:] = 6
        elif all(pixel == 3 for pixel in first_row_pixels):
           output_grid[0,:] = 3

    # fill the second row.
    output_grid[1,:] = 0

    # fill third row
    if len(key_rows) >= 2:
        second_row_pixels = key_rows[1][1]
        if all(pixel == 6 for pixel in second_row_pixels):
           output_grid[2,:] = 6
        elif all(pixel == 3 for pixel in second_row_pixels):
           output_grid[2,:] = 3

    return output_grid