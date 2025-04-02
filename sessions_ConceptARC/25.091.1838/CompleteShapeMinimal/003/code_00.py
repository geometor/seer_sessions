"""
Transforms the input grid by finding the dominant non-white color (C) and 
filling any white pixel (0) that has 3 or 4 neighbors of color C with that color C.
Neighbors are checked using 4-way adjacency (up, down, left, right).
"""

import numpy as np

def find_dominant_color(grid):
    """
    Finds the first non-background (non-zero) color in the grid.
    Assumes there is one dominant non-white color forming the shape.
    
    Args:
        grid (np.array): The input grid.
    
    Returns:
        int: The first non-zero color value found, or None if the grid is all zeros.
    """
    unique_colors = np.unique(grid)
    for color in unique_colors:
        if color != 0:
            return color
    return None # Return None if only background color (0) is found

def count_neighbors(grid, r, c, color):
    """
    Counts the number of 4-directionally adjacent neighbors of a pixel (r, c) 
    that have the specified color. Handles boundary conditions.

    Args:
        grid (np.array): The grid.
        r (int): Row index of the pixel.
        c (int): Column index of the pixel.
        color (int): The color to count neighbors for.

    Returns:
        int: The number of neighbors with the specified color.
    """
    height, width = grid.shape
    count = 0
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        # Check if neighbor is within grid boundaries
        if 0 <= nr < height and 0 <= nc < width:
            # Check if neighbor has the target color
            if grid[nr, nc] == color:
                count += 1
    return count

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list[list[int]]): The input grid represented as a list of lists.

    Returns:
        list[list[int]]: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape
    
    # Create a copy to modify
    output_grid = grid.copy()

    # Find the dominant non-white color
    dominant_color = find_dominant_color(grid)

    # If no dominant color found (e.g., all white grid), return the original grid
    if dominant_color is None:
        return output_grid.tolist()

    # Iterate through each pixel of the original grid
    for r in range(height):
        for c in range(width):
            # Check if the current pixel is white (0)
            if grid[r, c] == 0:
                # Count how many neighbors have the dominant color
                neighbor_count = count_neighbors(grid, r, c, dominant_color)
                
                # If the count is 3 or more, fill the pixel in the output grid
                if neighbor_count >= 3:
                    output_grid[r, c] = dominant_color

    # Convert the result back to a list of lists
    return output_grid.tolist()