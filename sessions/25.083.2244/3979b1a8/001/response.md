```python
"""
Transforms a 5x5 input grid into a 10x10 output grid based on observed patterns.
The transformation involves expanding the grid, replicating a modified version of the input,
creating a cross-shaped structure, and combining these elements.
"""

import numpy as np

def get_colors(input_grid):
    border_color = input_grid[0, 0]
    center_color = input_grid[2, 2]
     # Find a color different from border and center, assuming it's the inner square color
    for i in range(5):
      for j in range(5):
        if input_grid[i,j] != border_color and input_grid[i, j] != center_color:
          inner_color = input_grid[i,j]
          break
    return border_color, inner_color, center_color

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((10, 10), dtype=int)

    border_color, inner_color, center_color = get_colors(input_grid)

    #Plane of original input grid
    plane1 = np.copy(input_grid)

    #Plane of value 2 in example 1, 9 in example 2
    if border_color == 2:
       additional_color = 5
    else: additional_color = 2

    plane2 = np.full((5, 1), additional_color, dtype=int)

    #Plane of center color
    plane3 = np.full((5, 1), center_color, dtype=int)

    # Combine first and second planes
    combined_plane1 = np.concatenate((plane1, plane2, plane3, plane2, plane3), axis=1)
    output_grid[0:5, 0:5] = combined_plane1[0:5, 0:5]

    #Fill output grid based on combined and extra planes
    output_grid[5:10, 0] = plane3
    output_grid[5:10, 1] = plane3
    output_grid[5:10, 2] = plane3
    output_grid[5:10, 3] = plane2
    output_grid[5:10, 4] = plane3
    output_grid[5, 5] = plane2
    output_grid[6, 5] = plane2
    output_grid[7, 5] = plane2
    output_grid[8, 5] = plane2
    output_grid[9, 5] = plane3
    output_grid[7, 6] = plane2
    output_grid[8, 6] = plane2
    output_grid[9, 6] = plane2
    output_grid[8, 7] = plane2
    output_grid[9, 7] = plane2
    output_grid[9, 8] = plane2
    output_grid[9, 9] = plane3

    return output_grid
```