# 760b3cac • 004 • example_1 • investigate_coder

---
```python
"""
Transforms an input grid by moving vertically stacked azure (8) pixels to a horizontal line at the top of the output grid, preserving yellow (4) and white (0) pixels.
"""

import numpy as np

def get_vertical_stacks(grid, color):
    """
    Finds contiguous vertical stacks of a specified color.

    Args:
        grid: The input grid.
        color: The color to search for.

    Returns:
        A list of tuples, where each tuple contains (start_row, start_col, height).
    """
    stacks = []
    visited = set()
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and (r, c) not in visited:
                height = 0
                for r2 in range(r, rows):
                    if grid[r2, c] == color:
                        height += 1
                        visited.add((r2, c))
                    else:
                        break
                if height > 0:
                  stacks.append((r, c, height))
    return stacks

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = input_grid.copy()
    rows, cols = output_grid.shape

    # Identify vertical stacks of azure (8) pixels
    azure_stacks = get_vertical_stacks(input_grid, 8)

    # Calculate total height of azure stacks
    total_height = sum(stack[2] for stack in azure_stacks)

    # Construct horizontal line at the top
    
    col_index = 0
    
    for r, c, h in azure_stacks:
        #remove stacks from output grid
        for i in range(r,r+h):
          output_grid[i,c] = 0

    
    for r, c, h in azure_stacks:
      
      if (col_index + h) <= cols:
        #add to line from left to right
        for i in range(h):
          output_grid[0, col_index] = 8
          col_index+=1
      else:
          #add to line from right to left
          second_col_index = cols - 1
          for i in range(h):
            if output_grid[0,second_col_index] != 8:
              output_grid[0, second_col_index] = 8
            second_col_index -= 1

    return output_grid
```
