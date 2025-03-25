```python
"""
1.  **Identify the "X" Shape:** In the input grid, identify the color that forms a diagonally connected "X" shape. This "X" may be slightly distorted but maintains diagonal connectivity. Note, not all grids contain an X.

2.  **Preserve the "X" Color:** If an "X" shape is present, keep all pixels of that color in the output grid, setting the remaining pixels to 0.

3. **Handle "+" shape:** If no "X" exists: locate the "+" shape in the input, preserve it in the output.
Set the remaining pixels to 0.
"""

import numpy as np

def find_x_shape(grid):
    """
    Finds the color forming an 'X' shape in the grid.
    Returns the color if found, otherwise returns None.
    """
    rows, cols = grid.shape
    colors = np.unique(grid)

    for color in colors:
        if color == 0:  # Skip background
            continue

        # Check for diagonal connectivity
        is_x = False
        for r in range(rows):
            for c in range(cols):
                if grid[r, c] == color:
                    # Check for diagonal neighbors
                    if (r > 0 and c > 0 and grid[r-1, c-1] == color) or \
                       (r > 0 and c < cols - 1 and grid[r-1, c+1] == color) or \
                       (r < rows - 1 and c > 0 and grid[r+1, c-1] == color) or \
                       (r < rows - 1 and c < cols - 1 and grid[r+1, c+1] == color):
                        is_x = True
                        break
            if is_x:
                break
        if is_x: return color

    return None
    
def find_plus_shape(grid):
    """
    Identifies a '+' shape in the grid.
    """
    rows, cols = grid.shape
    colors = np.unique(grid)

    for color in colors:
      if color == 0: continue
      
      for r in range(1, rows - 1):
          for c in range(1, cols - 1):
            if grid[r,c] == color:
              if (grid[r+1, c] == color and grid[r-1, c] == color and grid[r, c+1] == color and grid[r, c-1] == color):
                return color
    return None
    
def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # Find X shape color
    x_color = find_x_shape(input_grid)

    if x_color is not None:
        # Preserve X shape color
        for r in range(input_grid.shape[0]):
            for c in range(input_grid.shape[1]):
                if input_grid[r, c] == x_color:
                    output_grid[r, c] = x_color
    else:
      #look for plus
      plus_color = find_plus_shape(input_grid)
      
      if plus_color is not None:
        for r in range(input_grid.shape[0]):
          for c in range(input_grid.shape[1]):
            if input_grid[r, c] == plus_color:
              output_grid[r,c] = plus_color

    return output_grid
```