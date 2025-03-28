import numpy as np
import math

"""
Transforms a grid containing exactly two non-white pixels (aligned horizontally or vertically) into a grid with two 13-pixel diamond shapes.

The transformation rule is as follows:
1. Initialize an output grid of the same dimensions as the input grid, filled with white (0).
2. Locate the two non-white pixels in the input grid. Sort them by row, then column, to get P1 = ((r1, c1), color1) and P2 = ((r2, c2), color2).
3. Determine the alignment (horizontal if r1 == r2, vertical if c1 == c2).
4. Calculate the distance between the points along the axis of alignment (dist = c2 - c1 or dist = r2 - r1).
5. Calculate the inward movement amount: move = (dist - 3) // 2.
6. Calculate the center coordinate (center1_r, center1_c) for the first shape (color1):
    - Horizontal: center1_r = r1, center1_c = c1 + move
    - Vertical: center1_r = r1 + move, center1_c = c1
7. Calculate the center coordinate (center2_r, center2_c) for the second shape (color2):
    - Horizontal: center2_r = r2, center2_c = c2 - move
    - Vertical: center2_r = r2 - move, center2_c = c2
8. Define the 13-pixel "diamond" shape using relative coordinates from a center point (cr, cc): [(-2,0), (-1,-1),(-1,0),(-1,1), (0,-2),(0,-1),(0,0),(0,1),(0,2), (1,-1),(1,0),(1,1), (2,0)].
9. Draw the first diamond shape on the output grid using color1, centered at (center1_r, center1_c).
10. Draw the second diamond shape on the output grid using color2, centered at (center2_r, center2_c). Handle boundary clipping.
11. Return the modified output grid.
"""

# Helper function to find the two non-white pixels
def find_non_white_pixels(grid):
    """
    Finds the coordinates and colors of the two non-white pixels in the grid.

    Args:
        grid (np.array): The input grid.

    Returns:
        tuple: A tuple containing two elements, each a tuple of ((row, col), color).
               Returns (None, None) if exactly two non-white pixels are not found.
               The pixels are sorted by row index, then column index.
    """
    pixels = []
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0:
                pixels.append(((r, c), grid[r, c]))

    if len(pixels) != 2:
        # This shouldn't happen based on task description but good practice to check
        print(f"Warning: Expected 2 non-white pixels, found {len(pixels)}")
        return None, None

    # Sort by row, then column to ensure consistent order P1, P2
    pixels.sort(key=lambda x: x[0])
    return pixels[0], pixels[1]

# Helper function to draw a 13-pixel diamond shape
def draw_diamond_shape(grid, center_r, center_c, color):
    """
    Draws a 13-pixel diamond shape onto the grid centered at (center_r, center_c).
    The shape is a 5x5 square minus the four corner pixels.

    Args:
        grid (np.array): The grid to draw on (mutable).
        center_r (int): The row index of the center of the shape.
        center_c (int): The column index of the center of the shape.
        color (int): The color to use for drawing the shape.
    """
    rows, cols = grid.shape
    # Relative coordinates for the 13 pixels forming the diamond shape
    shape_coords_relative = [
        (-2, 0),
        (-1, -1), (-1, 0), (-1, 1),
        (0, -2), (0, -1), (0, 0), (0, 1), (0, 2),
        (1, -1), (1, 0), (1, 1),
        (2, 0)
    ]
    for dr, dc in shape_coords_relative:
        r, c = center_r + dr, center_c + dc
        # Check grid boundaries before drawing
        if 0 <= r < rows and 0 <= c < cols:
            grid[r, c] = color

def transform(input_grid):
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape

    # Step 1: Initialize output grid with background color (white, 0)
    output_grid = np.zeros_like(input_np)

    # Step 2: Find the two non-white pixels and their colors, sorted by position
    pixel1, pixel2 = find_non_white_pixels(input_np)

    # If exactly two pixels weren't found, return the empty grid
    if pixel1 is None or pixel2 is None:
       return output_grid.tolist()

    # Extract coordinates and colors
    (r1, c1), color1 = pixel1
    (r2, c2), color2 = pixel2

    # Initialize center coordinates (defaults not strictly needed but good practice)
    center1_r, center1_c = -1, -1 # Center for shape derived from pixel1
    center2_r, center2_c = -1, -1 # Center for shape derived from pixel2

    # Steps 3-7: Determine orientation, calculate distance, movement, and center points
    if r1 == r2:  # Horizontal alignment (Step 3)
        dist = c2 - c1 # Step 4
        move = (dist - 3) // 2 # Step 5 (Corrected formula)
        center1_r = r1 # Step 6
        center1_c = c1 + move # Step 6
        center2_r = r2 # Step 7
        center2_c = c2 - move # Step 7

    elif c1 == c2:  # Vertical alignment (Step 3)
        dist = r2 - r1 # Step 4
        move = (dist - 3) // 2 # Step 5 (Corrected formula)
        center1_r = r1 + move # Step 6
        center1_c = c1 # Step 6
        center2_r = r2 - move # Step 7
        center2_c = c2 # Step 7
    else:
        # This case is not expected based on the training examples
        print("Error: Input pixels are not aligned horizontally or vertically.")
        return output_grid.tolist() # Return empty grid if alignment is invalid

    # Step 8 is implicit in draw_diamond_shape definition

    # Step 9: Draw the first diamond shape
    draw_diamond_shape(output_grid, center1_r, center1_c, color1)

    # Step 10: Draw the second diamond shape
    draw_diamond_shape(output_grid, center2_r, center2_c, color2)

    # Step 11: Return the result as a list of lists
    return output_grid.tolist()