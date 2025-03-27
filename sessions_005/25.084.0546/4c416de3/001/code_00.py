"""
Transforms the input grid based on a set of color-change rules, primarily focusing on mirroring the transformations of specific colors within connected regions.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on observed color and adjacency rules.
    """
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Define the color transformation mapping
    color_map = {
        1: 3,
        2: 9,
        4: 6,
        9: 4,
        7: 2,
        6: 0,
        3: 1,
    }

    # Iterate through each pixel in the grid
    for r in range(rows):
        for c in range(cols):
            current_color = input_grid[r, c]

            # Apply color transformations based on the map, skipping unchanged colors
            if current_color in color_map:
                output_grid[r, c] = color_map[current_color]
            elif current_color not in [0,3,6,8]: #check for unchanged colors
                neighbors = []
                if r > 0:
                    neighbors.append(input_grid[r-1,c])
                if r < rows-1:
                    neighbors.append(input_grid[r+1, c])
                if c > 0:
                    neighbors.append(input_grid[r,c-1])
                if c < cols-1:
                    neighbors.append(input_grid[r, c+1])

                for neighbor_color in neighbors:
                    if neighbor_color == current_color:
                        if current_color in color_map:
                             output_grid[r,c] = color_map[current_color]




    return output_grid.tolist()