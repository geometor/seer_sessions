"""
Identify all non-zero (colored) pixels in the input grid.
For each non-zero pixel, shift its position diagonally down and to the left.
The amount of left shift is determined by the number of non-zero pixels above it.
Create the output grid with the shifted pixels, maintaining original colors.
"""

import numpy as np

def get_nonzero_pixels(grid):
    # Find the indices of non-zero elements
    rows, cols = np.nonzero(grid)
    # Create a list of (row, col, value) tuples
    return [(r, c, grid[r, c]) for r, c in zip(rows, cols)]

def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = np.zeros_like(input_grid)
    input_pixels = get_nonzero_pixels(input_grid)

    # Build a map of original row to list of non-zero colors in that row
    row_to_colors = {}
    for r, c, val in input_pixels:
        if r not in row_to_colors:
          row_to_colors[r] = []
        row_to_colors[r].append(val)

    # calculate the shifts
    shifts = {}
    for row_index in sorted(row_to_colors.keys()):
      colors = row_to_colors[row_index]
      for color in colors:
          if color not in shifts:
            shifts[color] = 0
          else:
             shifts[color] +=1

    #print(f"Shifts: {shifts}")

    # Apply the shifts.
    for r, c, val in input_pixels:
      shift = shifts[val]
      #print(f"val {val} r {r} c {c} shift {shift}")
      new_r = r + shift
      new_c = c - shift
      #print(f"  new_r {new_r} new_c {new_c}")

      output_grid[new_r, new_c] = val


    return output_grid