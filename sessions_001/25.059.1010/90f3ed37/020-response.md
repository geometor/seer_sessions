# 90f3ed37 • 020 • refine_coder

---
```python
"""
The input grid is divided into two regions. The top region has a checkerboard pattern.
The bottom region is mostly white. The checkerboard pattern is extended into the
bottom region, replacing white pixels with a color determined by the top region.
Other colors are preserved.
"""

import numpy as np

def get_checkerboard_colors(input_grid, transition_row):
    """
    Identifies the two colors used in the checkerboard pattern.
    Assumes the checkerboard pattern is present in the rows above transition_row.
    """
    colors = set()
    for r in range(min(2, transition_row)):  # Check first two rows, or fewer if transition_row is small
        for c in range(input_grid.shape[1]):
            color = input_grid[r, c]
            if color != 0:  # Ignore white
                colors.add(color)
            if len(colors) == 2:
                return list(colors)
    return list(colors)  # Return whatever colors were found

def get_opposite_color(grid, r, c, colors):
    """
    Determines the opposite color in a checkerboard pattern.
    """
    if r > 0:
        above_color = grid[r-1, c]
        if above_color in colors:
          return colors[0] if above_color == colors[1] else colors[1]

    if c > 0:
      left_color = grid[r,c-1]
      if left_color in colors:
        return colors[0] if left_color == colors[1] else colors[1]
        
    return colors[0]
    

def find_transition_row(input_grid):
    """
    Finds the row where the checkerboard pattern ends.
    """
    rows, cols = input_grid.shape
    for r in range(rows - 1):
        # Check if the current row has a checkerboard pattern, but the next one doesn't.  This is
        # a simplification, but captures the essence of the transition.
        checkerboard_row = True
        for c in range(cols - 1):
            if input_grid[r, c] == input_grid[r, c + 1] and input_grid[r,c] != 0:
                checkerboard_row = False
                break
        
        next_row_mostly_white = True
        non_white_count = 0
        for c in range(cols):
            if input_grid[r+1,c] != 0:
                non_white_count +=1
        if non_white_count > cols//2: # check if mostly not white
            next_row_mostly_white = False

        if checkerboard_row and next_row_mostly_white:
            return r + 1
    return rows  # If no transition found, assume it's the last row


def transform(input_grid):
    """
    Transforms the input grid by extending a checkerboard pattern from the top
    region to the bottom region, replacing white pixels.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Determine the transition row.
    transition_row = find_transition_row(input_grid)

    # Get the checkerboard colors
    checkerboard_colors = get_checkerboard_colors(input_grid, transition_row)
    if len(checkerboard_colors) != 2:
      # default if can't determine - use previous
      checkerboard_colors = [1,8]

    # Iterate through the bottom region and apply the checkerboard pattern.
    for r in range(transition_row, rows):
        for c in range(cols):
            # Check for white pixels and propagate the checkerboard.
            if output_grid[r, c] == 0:
                output_grid[r, c] = get_opposite_color(output_grid, r, c, checkerboard_colors)

    return output_grid
```
