```python
"""
Moves green (3) pixels to the last available spot before an azure (8) pixel in their respective row,
provided they are not already adjacent to an azure.
"""

import numpy as np

def get_indices(grid, value):
    """Helper function to find indices of a specific value in the grid."""
    return np.where(grid == value)

def is_adjacent(grid, row, col, target_value):
    """Helper function to check if a cell is adjacent to a cell with the target_value."""
    rows, cols = grid.shape
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < rows and 0 <= new_col < cols and grid[new_row, new_col] == target_value:
                return True
    return False

def transform(input_grid):
    """Transforms the input grid according to the specified rule."""
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    for row_index in range(rows):
        row = output_grid[row_index]
        threes = np.where(row == 3)[0]
        eights = np.where(row == 8)[0]
        
        # If there are no 3s in this row, continue
        if threes.size == 0:
            continue

        #Find the rightmost 3
        rightmost_three_index = threes[-1]

        # check if this 3 is next to an 8
        adjacent_to_eight = False
        if eights.size > 0:
            for eight_index in eights:
                if abs(rightmost_three_index - eight_index) <= 1:
                     adjacent_to_eight = True

        if adjacent_to_eight:
            continue

        # Find the last 0 before an 8, if 8 exists
        insert_index = -1
        if eights.size > 0:
          for i in reversed(range(eights[0])):
              if row[i] == 0:
                insert_index = i
              else:
                break #stop at the last string of zeros

        #Move the right most 3,
        if insert_index != -1 :
            # Remove the 3 from its current position
            output_grid[row_index, rightmost_three_index] = 0
            output_grid[row_index, insert_index] = 3

    return output_grid
```