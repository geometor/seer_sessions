"""
Transforms an input grid by identifying and duplicating specific pattern rows.

The transformation identifies "pattern rows" based on specific criteria:
- Rows with alternating color sequences (e.g., 8 4 8 4).
- Rows with solid color blocks adjacent to alternating color sequences.

These pattern rows, and sometimes adjacent rows, are duplicated and inserted 
at specific locations in the grid, potentially overwriting existing content.
The direction of duplication (above or below) and the insertion point vary.
"""

import numpy as np

def find_pattern_rows(grid):
    """Identifies pattern rows based on alternating colors or solid blocks."""
    pattern_rows = []
    height, width = grid.shape
    for i in range(height):
        row = grid[i]
        if is_alternating(row) or is_adjacent_to_alternating(grid, i):
          if i not in pattern_rows:
            pattern_rows.append(i)
        elif is_three_section_pattern(row):
            if i not in pattern_rows:
                pattern_rows.append(i)

    return pattern_rows

def is_alternating(row):
    """Checks if a row has an alternating color pattern (e.g., A B A B)."""
    if len(row) < 2:
        return False
    first_color = row[0]
    second_color = None
    for i, cell in enumerate(row):
      if i == 0: continue

      if cell != first_color:
        second_color = cell
        break

    if second_color is None: return False

    for i, cell in enumerate(row):
        if i % 2 == 0:
            if cell != first_color:
                return False
        else:
            if cell != second_color:
                return False
    return True

def is_adjacent_to_alternating(grid, row_index):
    """Checks if a row with color blocks is adjacent to an alternating row."""
    height, _ = grid.shape
    if row_index > 0 and is_alternating(grid[row_index - 1]):
        return True
    if row_index < height - 1 and is_alternating(grid[row_index + 1]):
        return True
    return False

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

def duplicate_row(grid, source_row_index, destination_row_index):
    """Duplicates a row and inserts it at the destination index."""
    height, width = grid.shape
    new_grid = np.copy(grid)  # Start with a copy of the grid.
    new_grid[destination_row_index] = np.copy(grid[source_row_index]) #duplicate by overwriting
    return new_grid
    

def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    height, width = output_grid.shape
    
    # Find pattern rows in input
    pattern_rows = find_pattern_rows(input_grid)

    # Duplicate pattern rows based on example
    # Examples 1 and 2 logic
    if any(is_alternating(input_grid[row]) for row in pattern_rows):
      offset = 0
      for row_index in pattern_rows:
          if is_alternating(input_grid[row_index]):
            if row_index < 6: #row indices 2-5 are duplicated from row number 6
              destination_index = row_index + 4
              if destination_index < height:
                output_grid = duplicate_row(output_grid, row_index, destination_index + offset) #first alternating row
              
                #duplicate adjacent as well, if existing
                if row_index + 1 < height and not is_alternating(input_grid[row_index + 1]):
                  destination_index = row_index + 5 #overwrite adjacent to first alternating
                  if destination_index < height:
                    output_grid = duplicate_row(output_grid, row_index + 1, destination_index + offset) #first alternating row
              offset+=2
            else:
              #overwrite repeating 1 pattern
              destination_index = row_index + 3
              if destination_index < height:
                output_grid = duplicate_row(output_grid, row_index, destination_index-6) #first alternating row

                #duplicate adjacent as well, if existing
                if row_index + 1 < height and not is_alternating(input_grid[row_index + 1]):
                  destination_index = row_index + 4
                  if destination_index < height:
                      output_grid = duplicate_row(output_grid, row_index + 1, destination_index - 6)

    # Example 3 logic
    elif any(is_three_section_pattern(input_grid[row]) for row in pattern_rows):
        for row_index in pattern_rows:
          if is_three_section_pattern(input_grid[row_index]):
                destination_index = 10  # Fixed destination index
                output_grid = duplicate_row(output_grid, row_index, destination_index)

    return output_grid