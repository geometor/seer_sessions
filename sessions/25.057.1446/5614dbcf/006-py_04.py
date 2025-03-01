"""
1.  **Examine Corner Colors:** Determine the color of the pixel at each of the four corners of the input grid (top-left, top-right, bottom-left, bottom-right).
2.  **Create Output Grid:** Create a new 3x3 grid.
3.  **Uniform Corners:** If all four corner colors are identical:
    *   Fill all corner positions of the output grid with the same color.
    *   If the corner color is 1 (blue), set the center cell of the output grid to 2 (red).
    *   If the corner color is 2 (red), set the center cell to 8 (light blue) and all the cells directly adjacent to the center to 8.
    *   Otherwise, set the center cell to 0 (white).
4.  **Non-Uniform Corners:** If the four corner colors are not all identical:
    *   Place the color of each input corner pixel into the corresponding corner position in the output grid (e.g., top-left input corner color goes to top-left output corner).
    *   Set center cell to 0 (white)
"""

import numpy as np

def get_corner_color(grid, corner):
    """Gets the color of a specified corner."""
    rows, cols = grid.shape
    if corner == "top_left":
        return grid[0, 0]
    elif corner == "top_right":
        return grid[0, cols - 1]
    elif corner == "bottom_left":
        return grid[rows - 1, 0]
    elif corner == "bottom_right":
        return grid[rows - 1, cols - 1]
    else:
        raise ValueError("Invalid corner specified.")

def transform(input_grid):
    # Create a new 3x3 output grid, initialized to white (0)
    output_grid = np.zeros((3, 3), dtype=int)

    # Get the corner colors
    top_left = get_corner_color(input_grid, "top_left")
    top_right = get_corner_color(input_grid, "top_right")
    bottom_left = get_corner_color(input_grid, "bottom_left")
    bottom_right = get_corner_color(input_grid, "bottom_right")

    # Check if all corners are the same
    if top_left == top_right == bottom_left == bottom_right:
        # Fill all corner positions with the same color
        output_grid[:] = top_left

        # Handle specific corner color cases
        if top_left == 1:  # blue
            output_grid[1, 1] = 2  # red
        elif top_left == 2:  # red
            output_grid[1, 1] = 8 # azure
            output_grid[0, 1] = 8
            output_grid[1, 0] = 8
            output_grid[1, 2] = 8
            output_grid[2, 1] = 8
        else:  # Other colors
            output_grid[1, 1] = 0  # white

    else:  # Non-uniform corners
        # Place corner colors in the corresponding output positions
        output_grid[0, 0] = top_left
        output_grid[0, 2] = top_right
        output_grid[2, 0] = bottom_left
        output_grid[2, 2] = bottom_right
        output_grid[1,1] = 0

    return output_grid