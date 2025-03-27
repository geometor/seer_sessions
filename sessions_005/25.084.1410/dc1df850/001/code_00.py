import numpy as np
import copy

"""
Transforms the input grid based on the following rule:
1. Initialize the output grid as a copy of the input grid.
2. Find all pixels in the input grid with the color Red (2).
3. Iterate through each pixel in the input grid.
4. If a pixel is White (0), check if it is adjacent (horizontally, vertically, or diagonally) to any of the Red pixels found in step 2.
5. If a White pixel is adjacent to at least one Red pixel, change its color to Blue (1) in the output grid.
6. All other pixels retain their original color from the input grid.
"""

def find_pixels_by_color(grid, color_code):
    """
    Finds the coordinates of all pixels with a specific color.

    Args:
        grid (np.array): The input grid.
        color_code (int): The color code to search for.

    Returns:
        list: A list of tuples, where each tuple is the (row, col) coordinate
              of a pixel with the specified color.
    """
    locations = []
    height, width = grid.shape
    for r in range(height):
        for c in range(width):
            if grid[r, c] == color_code:
                locations.append((r, c))
    return locations

def is_adjacent(r, c, target_locations):
    """
    Checks if a given coordinate (r, c) is adjacent (8-connectivity) to any
    coordinate in the target_locations list.

    Args:
        r (int): Row of the current pixel.
        c (int): Column of the current pixel.
        target_locations (list): A list of (row, col) tuples to check adjacency against.

    Returns:
        bool: True if (r, c) is adjacent to any location in target_locations, False otherwise.
    """
    for tr, tc in target_locations:
        # Check horizontal, vertical, and diagonal adjacency
        # max(abs(r - tr), abs(c - tc)) == 1 covers all 8 neighbours
        if max(abs(r - tr), abs(c - tc)) == 1:
            return True
    return False

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list): A list of lists representing the input grid.

    Returns:
        list: A list of lists representing the transformed output grid.
    """
    # Convert input to numpy array for easier processing
    grid_np = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a deep copy of the input grid
    output_grid = grid_np.copy()
    
    height, width = grid_np.shape
    
    # Define color codes
    WHITE = 0
    BLUE = 1
    RED = 2
    
    # 1. Find the locations of all Red pixels in the input grid
    red_pixel_locations = find_pixels_by_color(grid_np, RED)
    
    # 2. Iterate through each pixel of the input grid
    for r in range(height):
        for c in range(width):
            # 3. Check if the current pixel is White
            if grid_np[r, c] == WHITE:
                # 4. Check if this White pixel is adjacent to any Red pixel
                if is_adjacent(r, c, red_pixel_locations):
                    # 5. If adjacent, change the corresponding pixel in the output grid to Blue
                    output_grid[r, c] = BLUE
                    
    # Convert the numpy array back to a list of lists for the final output format
    return output_grid.tolist()
