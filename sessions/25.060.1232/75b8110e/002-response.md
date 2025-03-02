# 75b8110e • 002 • example_5 • investigate_coder

---
```python
"""
The transformation extracts non-white (non-0) colored pixels from the input grid, groups them in sets of four, and rearranges these colors into a 4x4 output grid. The arrangement follows a specific order based on the input, creating a condensed representation.
"""

import numpy as np

def get_color_groups(input_grid):
    """
    Extracts non-white colors and groups them.
    """
    groups = []
    current_group = []
    
    rows = input_grid.shape[0]
    cols = input_grid.shape[1]
    
    for r in range(rows):
        for c in range(cols):
           color = input_grid[r,c]
           if color != 0:
             current_group.append(color)
             if len(current_group) == 4:
               groups.append(current_group)
               current_group = []

    #handle a possible final group
    if(len(current_group) > 0):
      while(len(current_group) < 4) :
        current_group.append(0) #pad with white
      groups.append(current_group)
        
    return groups

def transform(input_grid):
    """
    Transforms the input grid into a 4x4 output grid based on color grouping and rearrangement.
    """
    # Initialize the 4x4 output grid with zeros (white).
    output_grid = np.zeros((4, 4), dtype=int)

    # Get color groups from the input grid
    color_groups = get_color_groups(input_grid)
    
    
    #rearrange to match color orderings in outputs
    if(len(color_groups) >= 4):
        output_grid[0, 0] = color_groups[0][0] if len(color_groups[0])>=1 else 0
        output_grid[0, 1] = color_groups[0][1] if len(color_groups[0])>=2 else 0
        output_grid[0, 2] = color_groups[0][2] if len(color_groups[0])>=3 else 0
        output_grid[0, 3] = color_groups[0][3] if len(color_groups[0])>=4 else 0

        output_grid[1, 0] = color_groups[1][0] if len(color_groups[1])>=1 else 0
        output_grid[1, 1] = color_groups[1][1] if len(color_groups[1])>=2 else 0
        output_grid[1, 2] = color_groups[1][2] if len(color_groups[1])>=3 else 0
        output_grid[1, 3] = color_groups[1][3] if len(color_groups[1])>=4 else 0
        
        output_grid[2, 0] = color_groups[2][0] if len(color_groups[2])>=1 else 0
        output_grid[2, 1] = color_groups[2][1] if len(color_groups[2])>=2 else 0
        output_grid[2, 2] = color_groups[2][2] if len(color_groups[2])>=3 else 0
        output_grid[2, 3] = color_groups[2][3] if len(color_groups[2])>=4 else 0
        
        output_grid[3, 0] = color_groups[3][0] if len(color_groups[3])>=1 else 0
        output_grid[3, 1] = color_groups[3][1] if len(color_groups[3])>=2 else 0
        output_grid[3, 2] = color_groups[3][2] if len(color_groups[3])>=3 else 0
        output_grid[3, 3] = color_groups[3][3] if len(color_groups[3])>=4 else 0

    return output_grid
```
