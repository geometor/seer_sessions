# 239be575 • 006 • refine_coder

---
```python
"""
1. Count Red Pixels: Determine the number of red pixels in the input grid.
2. Count Azure Pixels: Determine the number of azure pixels in the input grid.
3. Check for any solid, rectangular blocks of red pixels.
4. If a solid block exists and there is also at least one azure, count six if the block is equal to or greater than 3x2, else the difference between the total count of red and azure, or else 0.
"""

import numpy as np

def _is_solid_rectangle(grid, color):
    """Checks if a grid contains a solid rectangle of the given color."""
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color:
                # Found a starting pixel. Check for rectangle.
                for height in range(1, rows - r + 1):
                    for width in range(1, cols - c + 1):
                        sub_grid = grid[r:r+height, c:c+width]
                        if np.all(sub_grid == color):
                            if height >= 3 and width >= 2:
                                 return height, width, True
    return 0, 0, False
                            

def transform(input_grid):
    # Count the number of red (2) pixels.
    red_count = np.sum(input_grid == 2)
    
    # Count the number of azure (8) pixels.
    azure_count = np.sum(input_grid == 8)
    
    # Check for solid red rectangle
    height, width, is_rectangle = _is_solid_rectangle(input_grid, 2)

    # Calculate output based on the new rule
    if is_rectangle and azure_count > 0:
        if height >= 3 and width >= 2 :
          result = 5
        else:
          result = abs(red_count - azure_count)
    elif azure_count == 0 and red_count > 0:
        result = abs(red_count - azure_count)          
    else:
        result = 0

    
    # Create a 1x1 output grid.
    output_grid = np.array([[result]])
    
    return output_grid
```
