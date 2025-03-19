# a68b268e • 028 • example_5 • investigate_coder

---
```python
"""
The transformation extracts the color arrangement of the 4 quadrants, defined by blue lines, 
and eliminates the inner lines and zeros that might be considered background or separators.
"""

import numpy as np

def get_quadrant_colors(grid):
    """
    Extracts prominent colors from each quadrant of the grid, excluding blue (1) and white (0).
    """
    height, width = grid.shape
    mid_x = width // 2
    mid_y = height // 2

    quadrant_colors = {
      'top_left': [],
      'top_right': [],
      'bottom_left': [],
      'bottom_right': []
    }

    # Top-left quadrant
    for y in range(mid_y):
        for x in range(mid_x):
          if grid[y][x] != 1 and grid[y][x] !=0:
            quadrant_colors['top_left'].append(grid[y][x])

    # Top-right quadrant
    for y in range(mid_y):
        for x in range(mid_x + 1, width):
            if grid[y][x] != 1 and grid[y][x] !=0:
                quadrant_colors['top_right'].append(grid[y][x])

    # Bottom-left quadrant
    for y in range(mid_y + 1, height):
        for x in range(mid_x):
            if grid[y][x] != 1 and grid[y][x] !=0:
                quadrant_colors['bottom_left'].append(grid[y][x])


    # Bottom-right quadrant
    for y in range(mid_y + 1, height):
        for x in range(mid_x + 1, width):
            if grid[y][x] != 1 and grid[y][x] !=0:
                quadrant_colors['bottom_right'].append(grid[y][x])
    
    return quadrant_colors

def transform(input_grid):
    # Convert input grid to numpy array
    grid = np.array(input_grid)

    # Extract color of each quadrant
    quadrant_colors = get_quadrant_colors(grid)

    # initialize output_grid
    output_grid = np.zeros((4, 4), dtype=int)

    # Fill in output grid using values of each quadrant
    output_grid[0,0] = quadrant_colors['top_left'][0] if quadrant_colors['top_left'] else 0
    output_grid[0,1] = quadrant_colors['top_left'][-1] if len(quadrant_colors['top_left']) > 1 else (quadrant_colors['top_left'][0] if quadrant_colors['top_left'] else 0)
    output_grid[0,2] = quadrant_colors['top_right'][0] if quadrant_colors['top_right'] else 0
    output_grid[0,3] = quadrant_colors['top_right'][-1] if len(quadrant_colors['top_right']) > 1 else (quadrant_colors['top_right'][0] if quadrant_colors['top_right'] else 0)
    output_grid[1,0] = quadrant_colors['top_left'][1] if len(quadrant_colors['top_left']) > 2 else (quadrant_colors['top_left'][0] if quadrant_colors['top_left'] else 0)
    output_grid[1,1] = quadrant_colors['top_left'][-2] if len(quadrant_colors['top_left']) > 2 else (quadrant_colors['top_left'][-1] if len(quadrant_colors['top_left']) > 1 else (quadrant_colors['top_left'][0] if quadrant_colors['top_left'] else 0))

    output_grid[1,2] = quadrant_colors['top_right'][1] if len(quadrant_colors['top_right']) > 2 else (quadrant_colors['top_right'][0] if quadrant_colors['top_right'] else 0)
    output_grid[1,3] = quadrant_colors['top_right'][-2] if len(quadrant_colors['top_right']) > 2 else (quadrant_colors['top_right'][-1] if len(quadrant_colors['top_right']) > 1 else (quadrant_colors['top_right'][0] if quadrant_colors['top_right'] else 0))

    output_grid[2,0] = quadrant_colors['bottom_left'][0] if quadrant_colors['bottom_left'] else 0
    output_grid[2,1] = quadrant_colors['bottom_left'][-1] if len(quadrant_colors['bottom_left']) > 1 else (quadrant_colors['bottom_left'][0] if quadrant_colors['bottom_left'] else 0)
    output_grid[2,2] = quadrant_colors['bottom_right'][0] if quadrant_colors['bottom_right'] else 0
    output_grid[2,3] = quadrant_colors['bottom_right'][-1] if len(quadrant_colors['bottom_right']) > 1 else (quadrant_colors['bottom_right'][0] if quadrant_colors['bottom_right'] else 0)
    output_grid[3,0] = quadrant_colors['bottom_left'][1] if len(quadrant_colors['bottom_left']) > 2 else (quadrant_colors['bottom_left'][0] if quadrant_colors['bottom_left'] else 0)
    output_grid[3,1] = quadrant_colors['bottom_left'][-2] if len(quadrant_colors['bottom_left']) > 2 else (quadrant_colors['bottom_left'][-1] if len(quadrant_colors['bottom_left']) > 1 else (quadrant_colors['bottom_left'][0] if quadrant_colors['bottom_left'] else 0))

    output_grid[3,2] = quadrant_colors['bottom_right'][1] if len(quadrant_colors['bottom_right']) > 2 else (quadrant_colors['bottom_right'][0] if quadrant_colors['bottom_right'] else 0)
    output_grid[3,3] = quadrant_colors['bottom_right'][-2] if len(quadrant_colors['bottom_right']) > 2 else (quadrant_colors['bottom_right'][-1] if len(quadrant_colors['bottom_right']) > 1 else (quadrant_colors['bottom_right'][0] if quadrant_colors['bottom_right'] else 0))
    return output_grid.tolist()
```
