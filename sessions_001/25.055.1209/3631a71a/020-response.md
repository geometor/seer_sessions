# 3631a71a • 020 • example_4 • investigate_coder

---
```python
"""
Iterate through each pixel of the input grid. Examine each pixel and its
immediate 8 neighbors (up, down, left, right, and diagonals). Identify
regions composed from one color, with more than 1 neighbor with the same
color. Filter the areas in the grid: if a pixel has less than a certain
number of neighbors of the same color, and is bordered by neighbors with
colors different from it, change that pixel color, setting to most present
color in the neighborhood. Output the modified grid.
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
    """Applies a noise reduction/simplification filter to the input grid."""
    input_grid = np.array(input_grid)  # Ensure numpy array
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each pixel
    for row in range(rows):
        for col in range(cols):
            # Get the neighbors' colors
            neighbors = get_neighbors(input_grid, row, col)
            my_color = input_grid[row,col]

            # Count neighbors of same color
            same_color_count = neighbors.count(my_color)

            # Apply the filter rule
            # using threshold = 1, will modify threshold if does not work correctly
            if same_color_count <= 1:
                # change to most common neighbor
                output_grid[row,col] = most_common_neighbor(input_grid,row,col)

    return output_grid.tolist()
```
