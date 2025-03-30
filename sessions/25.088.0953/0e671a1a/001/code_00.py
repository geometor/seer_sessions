import numpy as np
import math

# Color constants
RED = 2
GREEN = 3
YELLOW = 4
GRAY = 5
WHITE = 0

"""
Connect three specific colored points (Red=2, Yellow=4, Green=3) with gray (5) 
L-shaped paths in a fixed order: Red -> Yellow, then Yellow -> Green.
The L-shape path consists of a horizontal segment along the starting point's 
row until the ending point's column, and then a vertical segment along the 
ending point's column until the ending point's row.
"""

def find_pixel(grid, color):
    """
    Finds the coordinates (row, column) of the first pixel with the given color.

    Args:
        grid (np.array): The input grid.
        color (int): The color value to find.

    Returns:
        tuple: (row, column) coordinates, or None if not found.
    """
    coords = np.argwhere(grid == color)
    if len(coords) > 0:
        return tuple(coords[0]) # Return the first occurrence
    return None

def draw_l_path(grid, start_coords, end_coords, path_color):
    """
    Draws an L-shaped path (horizontal then vertical) between two points.
    The path consists of gray pixels (5).
    The path starts adjacent to the start point and ends adjacent to the end point.

    Args:
        grid (np.array): The grid to draw on (modified in-place).
        start_coords (tuple): (row, col) of the starting pixel.
        end_coords (tuple): (row, col) of the ending pixel.
        path_color (int): The color to use for the path.
    """
    r1, c1 = start_coords
    r2, c2 = end_coords

    # Draw horizontal segment from (r1, c1) to (r1, c2)
    # Excludes the start pixel (r1, c1)
    if c1 < c2: # Move right
        for c in range(c1 + 1, c2 + 1):
            if grid[r1, c] == WHITE: # Only draw over background
                 grid[r1, c] = path_color
    elif c1 > c2: # Move left
        for c in range(c1 - 1, c2 - 1, -1):
             if grid[r1, c] == WHITE: # Only draw over background
                 grid[r1, c] = path_color
    # If c1 == c2, no horizontal segment needed besides the corner potentially

    # Draw vertical segment from (r1, c2) to (r2, c2)
    # Excludes the corner pixel (r1, c2) if it was drawn horizontally,
    # and excludes the end pixel (r2, c2)
    if r1 < r2: # Move down
        for r in range(r1 + 1, r2 + 1):
             if grid[r, c2] == WHITE: # Only draw over background
                 grid[r, c2] = path_color
    elif r1 > r2: # Move up
        for r in range(r1 - 1, r2 - 1, -1):
             if grid[r, c2] == WHITE: # Only draw over background
                 grid[r, c2] = path_color
    # If r1 == r2, no vertical segment needed

def transform(input_grid):
    """
    Connects Red(2) -> Yellow(4) -> Green(3) pixels with gray(5) L-paths.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert to numpy array for easier manipulation
    grid_np = np.array(input_grid, dtype=int)
    output_grid = grid_np.copy()

    # Find the coordinates of the key pixels
    red_coords = find_pixel(grid_np, RED)
    yellow_coords = find_pixel(grid_np, YELLOW)
    green_coords = find_pixel(grid_np, GREEN)

    # Check if all points were found (should always be true based on task description)
    if not (red_coords and yellow_coords and green_coords):
        # Handle error case if needed, though not expected for ARC
        print("Error: Could not find all required pixels (Red, Yellow, Green).")
        return input_grid # Return original grid or handle appropriately

    # Draw the first L-path: Red -> Yellow
    draw_l_path(output_grid, red_coords, yellow_coords, GRAY)

    # Draw the second L-path: Yellow -> Green
    draw_l_path(output_grid, yellow_coords, green_coords, GRAY)

    # Convert back to list of lists for the ARC standard
    return output_grid.tolist()