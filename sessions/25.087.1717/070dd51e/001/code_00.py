import numpy as np
from collections import defaultdict

"""
Connect pairs of same-colored pixels in the input grid by drawing a straight 
line (horizontal or vertical) between them using their color.

1. Create a copy of the input grid to serve as the initial output grid.
2. Identify all non-white pixels in the input grid and group them by their color.
3. Iterate through each color group.
4. If a color group contains exactly two pixels:
    a. Let the coordinates of the two pixels be (r1, c1) and (r2, c2).
    b. Check if the pixels are horizontally aligned (i.e., r1 equals r2). 
       If they are, fill the horizontal line segment between them with their color.
    c. Check if the pixels are vertically aligned (i.e., c1 equals c2). 
       If they are, fill the vertical line segment between them with their color.
5. Return the final modified output grid.
"""

def find_colored_pixels(grid):
    """Finds all non-white pixels and groups them by color."""
    colored_pixels = defaultdict(list)
    height, width = grid.shape
    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            if color != 0: # 0 is white (background)
                colored_pixels[color].append((r, c))
    return colored_pixels

def fill_line(grid, p1, p2, color):
    """Fills the line between two points p1 and p2 with the given color."""
    r1, c1 = p1
    r2, c2 = p2

    # Check for horizontal alignment
    if r1 == r2:
        start_col = min(c1, c2)
        end_col = max(c1, c2)
        for c in range(start_col, end_col + 1):
            grid[r1, c] = color
            
    # Check for vertical alignment
    elif c1 == c2:
        start_row = min(r1, r2)
        end_row = max(r1, r2)
        for r in range(start_row, end_row + 1):
            grid[r, c1] = color
    # Note: The problem description implies pairs are either horizontal or vertical,
    # so no diagonal or other cases are handled.

def transform(input_grid):
    """
    Connects pairs of same-colored pixels horizontally or vertically.
    """
    # Convert input_grid to a NumPy array for easier manipulation
    input_np = np.array(input_grid)
    
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_np)

    # Find all non-white pixels and group them by color
    colored_pixels_map = find_colored_pixels(input_np)

    # Iterate through each color group found
    for color, positions in colored_pixels_map.items():
        # Check if there are exactly two pixels of this color
        if len(positions) == 2:
            # Get the coordinates of the two pixels
            p1 = positions[0]
            p2 = positions[1]
            
            # Fill the line between the pair in the output grid
            fill_line(output_grid, p1, p2, color)

    # Convert the final NumPy array back to a list of lists
    return output_grid.tolist()
