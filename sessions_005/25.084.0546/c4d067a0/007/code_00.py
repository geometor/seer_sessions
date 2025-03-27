"""
The transformation duplicates rows that have a three-section pattern: starting and ending with 1, with two distinct sections of other colors in between. These rows are duplicated multiple times and placed at the end of the grid.
"""

import numpy as np

def is_three_section_pattern(row):
    """Checks if a row follows the three-section pattern (e.g., 1 3 3 1 1 1 4 4 1)."""
    if len(row) < 5 or row[0] != 1 or row[-1] != 1:  # Must start and end with 1
        return False

    # Find the first section boundary
    first_section_end = -1
    for i in range(1, len(row)):
        if row[i] == 1 and row[i-1] != 1:
            first_section_end = i
            break
    if first_section_end == -1: return False

    #find the second section boundary
    second_section_end = -1
    for i in range(first_section_end+1,len(row)):
        if row[i] != 1:
          second_section_end = i
          break

    if second_section_end == -1: return False #all 1's

    first_color = -1
    #check colors are different
    for i in range(0, first_section_end):
      if row[i] != 1:
        first_color = row[i]
        break

    second_color = -1
    for i in range(second_section_end, len(row)):
      if row[i] != 1:
        second_color = row[i]
        break

    if first_color == second_color or first_color == -1 or second_color == -1: return False

    return True

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    height, width = output_grid.shape

    #find three section pattern rows
    pattern_rows = []
    for i in range(height):
        if is_three_section_pattern(input_grid[i]):
            pattern_rows.append(i)


    #Append duplicates to the bottom of the grid
    for row_index in pattern_rows:
        output_grid = np.vstack([output_grid, input_grid[row_index]])

    return output_grid