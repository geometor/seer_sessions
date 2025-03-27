"""
Transforms an input grid based on the interaction between gray (5) and azure (8) pixels.

1.  Iterate through each pixel of the input grid.
2.  For each pixel, examine its 8 neighbors (including diagonals) in the input grid.
3.  If the current pixel is gray (5) and has at least one azure (8) neighbor, change its color to azure (8) in the output grid.
4.  If the current pixel is azure (8) and has at least one gray (5) neighbor, change its color to gray (5) in the output grid.
5.  If neither of the above conditions is met (i.e., the pixel is not gray or azure, or it is gray/azure but lacks the triggering neighbor color), keep its original color in the output grid.
6.  The transformation is applied simultaneously, meaning all decisions are based on the original input grid state.
"""

import numpy as np

def _get_neighbor_colors(grid, r, c):
    """
    Gets the colors of the 8 neighbors for a given cell (r, c).

    Args:
        grid (np.array): The input grid.
        r (int): The row index of the cell.
        c (int): The column index of the cell.

    Returns:
        list: A list of colors of the valid neighbors.
    """
    height, width = grid.shape
    neighbor_colors = []
    # Iterate through the 8 possible neighbor offsets (dr, dc)
    for dr in range(-1, 2):
        for dc in range(-1, 2):
            # Skip the cell itself
            if dr == 0 and dc == 0:
                continue
            
            nr, nc = r + dr, c + dc
            
            # Check if the neighbor coordinates are within the grid bounds
            if 0 <= nr < height and 0 <= nc < width:
                neighbor_colors.append(grid[nr, nc])
                
    return neighbor_colors

def transform(input_grid):
    """
    Applies the transformation rules to the input grid.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # Initialize output_grid as a copy of the input grid.
    # This handles cases where pixels don't change.
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape
    
    gray_color = 5
    azure_color = 8

    # Iterate through each cell of the input grid
    for r in range(height):
        for c in range(width):
            current_color = input_grid[r, c]
            
            # Get the colors of the neighbors from the *input* grid
            neighbor_colors = _get_neighbor_colors(input_grid, r, c)

            # Apply transformation rules based on the input grid state
            if current_color == gray_color:
                # Check if any neighbor is azure
                if azure_color in neighbor_colors:
                    output_grid[r, c] = azure_color
            elif current_color == azure_color:
                # Check if any neighbor is gray
                if gray_color in neighbor_colors:
                    output_grid[r, c] = gray_color
            # No else needed: if the color is not gray or azure, or if the 
            # neighbor condition isn't met, the output_grid already holds 
            # the original color from the initial copy.

    return output_grid
