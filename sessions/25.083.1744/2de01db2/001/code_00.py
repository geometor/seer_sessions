"""
1.  **Reflect:** Horizontally reflect the input grid. This means swapping the positions of elements across the central vertical axis. For example, the first element becomes the last, the second becomes the second-to-last, and so on.
2.  **Color Replacement, phase 1:** Scan every cell of the input grid, if the original number is a `7` or a `2`, then the reflected number should become `0`.
3.  **Color Replacement, phase 2:** If a cell originally contained a `7` or a `2`, the color will change to `0` after the reflection.
4. return the reflected output grid after color replacement.
"""

import numpy as np

def reflect_horizontally(grid):
    """Reflects a grid horizontally."""
    return np.fliplr(grid)

def replace_colors(grid, original_grid):
    """Replaces colors based on the original grid."""
    new_grid = np.copy(grid)
    for i in range(original_grid.shape[0]):
        for j in range(original_grid.shape[1]):
            if original_grid[i, j] == 7 or original_grid[i, j] == 2:
                new_grid[i, j] = 0
    return new_grid
    

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)

    # Reflect the grid horizontally
    output_grid = reflect_horizontally(output_grid)
    
    # change pixels based on original numbers
    output_grid = replace_colors(output_grid, input_grid)

    return output_grid.tolist()