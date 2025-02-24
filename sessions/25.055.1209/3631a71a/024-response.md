# 3631a71a • 024 • refine_coder

---
```python
"""
Iterate through each pixel in the input grid. If a pixel is white (color 0)
and has at most one neighbor of the same color (white), change its color to
the most frequent color among its neighbors (excluding the pixel's own color,
if there are other colors). If the pixel is not white or has more than one
white neighbor, keep its original color. The output is the modified grid.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Gets the 8 neighbors of a pixel, handling boundary conditions."""
    rows, cols = grid.shape
    neighbors = []
    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(cols, col + 2)):
            if (i, j) != (row, col):
                neighbors.append(grid[i, j])
    return neighbors

def most_common_neighbor(grid, row, col):
    """Finds most frequent color among neighbors, excluding the pixel's own color."""
    neighbors = get_neighbors(grid, row, col)
    if not neighbors:
       return grid[row,col]

    counts = {}
    my_color = grid[row,col]

    for color in neighbors:
        if color != my_color:
            counts[color] = counts.get(color,0) + 1
    
    if not counts:
        return grid[row,col]

    most_common = max(counts, key=counts.get)
    return most_common

def transform(input_grid):
    """Applies the transformation rule to the input grid."""
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each pixel
    for row in range(rows):
        for col in range(cols):
            my_color = input_grid[row, col]
            neighbors = get_neighbors(input_grid, row, col)
            same_color_count = neighbors.count(my_color)

            # Check if the pixel is white and has at most one white neighbor
            if my_color == 0 and same_color_count <= 1:
                # Change color to the most frequent neighbor color
                output_grid[row, col] = most_common_neighbor(input_grid, row, col)

    return output_grid.tolist()
```
