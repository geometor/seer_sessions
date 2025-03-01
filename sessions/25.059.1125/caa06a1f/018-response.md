# caa06a1f • 018 • refine_coder

---
```python
"""
The transformation identifies two primary colors that form rectangular shapes, with a third, background color. If the two primary colors appear in equal numbers, the last row is removed, changing some instances of the first primary color to the other. If the counts of the primary colors are unequal, a single pixel of the more frequent primary color is removed, and the other primary color and background are left intact.
"""

import numpy as np

def get_primary_colors(grid):
    """
    Identifies the two most frequent colors, excluding a potential background color (least frequent).
    """
    unique_colors, counts = np.unique(grid, return_counts=True)
    
    # Sort colors by frequency in descending order
    sorted_indices = np.argsort(counts)[::-1]
    
    # Handle edge case where there might be only 1 or 2 colors.
    if len(sorted_indices) >= 2:
      color1 = unique_colors[sorted_indices[0]]
      color2 = unique_colors[sorted_indices[1]]
      return color1, color2
    elif len(sorted_indices) == 1:
        return unique_colors[sorted_indices[0]], None  # Only one color
    else:
        return None, None  # Empty grid

def transform(input_grid):
    """
    Transforms the input grid based on the rules described above.
    """
    output_grid = np.copy(input_grid)
    color1, color2 = get_primary_colors(input_grid)

    if color1 is None:  # Handle cases with fewer than 2 colors
        return output_grid
      
    if color2 is None:
        return output_grid
    
    count1 = np.sum(input_grid == color1)
    count2 = np.sum(input_grid == color2)

    if count1 == count2:
        # Remove the last row
        output_grid = output_grid[:-1]

        # Recalculate counts after removing the row to ensure correctness
        count1 = np.sum(output_grid == color1)
        count2 = np.sum(output_grid == color2)
        
        # Swap to equalize
        if(count1 > count2):
          diff = count1 - count2
          indices = np.where(output_grid == color1)
          
          # change from color1 to color2 until diff == 0
          for i in range(min(diff, len(indices[0]))):
            output_grid[indices[0][i],indices[1][i]] = color2
            
        elif(count2 > count1):
          diff = count2 - count1
          indices = np.where(output_grid == color2)
          for i in range(min(diff, len(indices[0]))):
            output_grid[indices[0][i],indices[1][i]] = color1
        
    elif count1 > count2:
        # Remove one pixel of color1
        indices = np.where(output_grid == color1)
        output_grid[indices[0][0], indices[1][0]] = input_grid[indices[0][0], indices[1][0]] % 10  # set to different value, wrap around
        output_grid[indices[0][0], indices[1][0]] = get_primary_colors(output_grid)[1] #set to color2

    else:  # count2 > count1
        # Remove one pixel of color2
        indices = np.where(output_grid == color2)
        output_grid[indices[0][0], indices[1][0]] = input_grid[indices[0][0], indices[1][0]] % 10 # set to different value, wrap around
        output_grid[indices[0][0], indices[1][0]] = get_primary_colors(output_grid)[0]
    return output_grid
```
