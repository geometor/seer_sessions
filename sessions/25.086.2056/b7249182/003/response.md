```python
import numpy as np
import math

"""
Transforms an input grid containing exactly two non-white pixels (aligned horizontally or vertically) into an output grid featuring two 5x5 plus-shaped patterns.

The transformation rule is as follows:
1. Locate the two non-white pixels in the input grid. Sort them by row, then column, to get P1 = ((r1, c1), color1) and P2 = ((r2, c2), color2).
2. Determine the alignment (horizontal if r1 == r2, vertical if c1 == c2).
3. Calculate the midpoint along the axis of alignment:
    - Horizontal: mid_c = (c1 + c2) / 2.0
    - Vertical: mid_r = (r1 + r2) / 2.0
4. Calculate the center coordinate (center1_r, center1_c) for the first shape (color1):
    - Horizontal: center1_r = r1, center1_c = c1 + floor((floor(mid_c) - c1) / 2)
    - Vertical: center1_r = r1 + floor((floor(mid_r) - r1) / 2), center1_c = c1
5. Calculate the center coordinate (center2_r, center2_c) for the second shape (color2):
    - Horizontal: center2_r = r2, center2_c = c2 - floor((c2 - ceil(mid_c)) / 2)
    - Vertical: center2_r = r2 - floor((r2 - ceil(mid_r)) / 2), center2_c = c2
6. Draw two 5x5 plus shapes (+) on an initially white grid of the same dimensions as the input. Shape 1 uses color1 centered at (center1_r, center1_c), and Shape 2 uses color2 centered at (center2_r, center2_c). The plus shape consists of the center pixel and the pixels at distances 1 and 2 along the horizontal and vertical axes from the center.
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
        print(f"Warning: Expected 2 non-white pixels, found {len(pixels)}")
        return None, None

    # Sort by row, then column to ensure consistent order
    pixels.sort(key=lambda x: x[0])
    return pixels[0], pixels[1]

# Helper function to draw a 5x5 plus shape
def draw_plus_shape(grid, center_r, center_c, color):
    """
    Draws a 5x5 plus shape (+) onto the grid centered at (center_r, center_c).

    Args:
        grid (np.array): The grid to draw on (mutable).
        center_r (int): The row index of the center of the shape.
        center_c (int): The column index of the center of the shape.
        color (int): The color to use for drawing the shape.
    """
    rows, cols = grid.shape
    # Relative coordinates for the 9 pixels forming the 5x5 plus shape
    shape_coords_relative = [
        (0, 0), (0, 1), (0, -1), (0, 2), (0, -2),
        (1, 0), (-1, 0), (2, 0), (-2, 0)
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

    # Initialize output grid with background color (white, 0)
    output_grid = np.zeros_like(input_np)

    # Find the two non-white pixels and their colors, sorted by position
    pixel1, pixel2 = find_non_white_pixels(input_np)

    # If exactly two pixels weren't found, return the empty grid
    if pixel1 is None or pixel2 is None:
       return output_grid.tolist()

    # Extract coordinates and colors
    (r1, c1), color1 = pixel1
    (r2, c2), color2 = pixel2

    # Initialize center coordinates
    center1_r, center1_c = -1, -1 # Center for shape derived from pixel1
    center2_r, center2_c = -1, -1 # Center for shape derived from pixel2

    # Determine orientation and calculate the two center points using the refined logic
    if r1 == r2:  # Horizontal alignment
        mid_c = (c1 + c2) / 2.0 # Calculate midpoint column
        center1_r = r1
        # Calculate center column for shape 1
        center1_c = c1 + math.floor((math.floor(mid_c) - c1) / 2)
        center2_r = r2
        # Calculate center column for shape 2
        center2_c = c2 - math.floor((c2 - math.ceil(mid_c)) / 2)

    elif c1 == c2:  # Vertical alignment
        mid_r = (r1 + r2) / 2.0 # Calculate midpoint row
        # Calculate center row for shape 1
        center1_r = r1 + math.floor((math.floor(mid_r) - r1) / 2)
        center1_c = c1
        # Calculate center row for shape 2
        center2_r = r2 - math.floor((r2 - math.ceil(mid_r)) / 2)
        center2_c = c2
    else:
        # This case is not expected based on the training examples
        print("Error: Input pixels are not aligned horizontally or vertically.")
        return output_grid.tolist() # Return empty grid if alignment is invalid

    # Draw the first plus shape using color1 centered at the calculated (center1_r, center1_c)
    draw_plus_shape(output_grid, center1_r, center1_c, color1)

    # Draw the second plus shape using color2 centered at the calculated (center2_r, center2_c)
    draw_plus_shape(output_grid, center2_r, center2_c, color2)

    # Return the result as a list of lists
    return output_grid.tolist()
```