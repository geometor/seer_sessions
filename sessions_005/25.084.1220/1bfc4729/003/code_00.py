"""
Create an output grid by drawing horizontal lines based on input pixel rows and grid edges, and vertical lines only at grid edges, with colors determined by the input pixels' colors and relative vertical positions.

1. Identify the two non-white pixels in the input grid. Record their colors and row/column coordinates.
2. Determine the height (H) and width (W) of the input grid.
3. Sort the two pixels based on their row index. Let P1 = (r1, c1, color1) be the pixel with the smaller row index, and P2 = (r2, c2, color2) be the pixel with the larger row index. If row indices are equal, the order doesn't strictly matter for the final output based on the drawing logic, but a consistent sort (e.g., by column next) is good practice.
4. Create a new output grid of dimensions H x W, initially filled with white (0).
5. Calculate the vertical midpoint row index: `mid_row = floor(H / 2)`.
6. Draw the left vertical edge line (column 0): For each row `r` from 0 to H-1, set the color of cell (r, 0) to `color1` if `r < mid_row`, otherwise set it to `color2`.
7. Draw the right vertical edge line (column W-1): For each row `r` from 0 to H-1, set the color of cell (r, W-1) to `color1` if `r < mid_row`, otherwise set it to `color2`.
8. Draw the top horizontal edge line: Set all cells in row 0 to `color1`.
9. Draw the bottom horizontal edge line: Set all cells in row H-1 to `color2`.
10. Draw the horizontal line corresponding to P1: Set all cells in row `r1` to `color1`.
11. Draw the horizontal line corresponding to P2: Set all cells in row `r2` to `color2`. (Note: This step ensures P2's color takes precedence if r1 == r2, consistent with P2 being the 'lower' pixel). The order of drawing horizontal lines after vertical lines ensures horizontal lines overwrite intersections correctly.
12. The resulting grid is the final output.
"""

import numpy as np
import math

def find_non_white_pixels(grid):
    """Finds the coordinates and colors of non-white pixels."""
    pixels = []
    for r, row in enumerate(grid):
        for c, color in enumerate(row):
            if color != 0:
                pixels.append(((r, c), color))
    return pixels

def transform(input_grid):
    """
    Transforms the input grid based on drawing horizontal and vertical edge lines,
    and horizontal lines corresponding to the rows of the two non-white input pixels.
    """
    # Convert input list of lists to numpy array
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # 1. Identify the two non-white pixels
    non_white_pixels = find_non_white_pixels(input_np)

    # Check if exactly two non-white pixels were found
    if len(non_white_pixels) != 2:
        # If not, return an empty grid of the same size as a fallback.
        # This case shouldn't occur based on the provided examples, but it's safer to handle.
        print(f"Warning: Expected 2 non-white pixels, found {len(non_white_pixels)}. Returning empty grid.")
        return np.zeros_like(input_np).tolist()

    # 3. Sort pixels based on row index (ascending)
    # If rows are equal, sorting order doesn't impact the final result due to drawing order.
    non_white_pixels.sort(key=lambda item: item[0][0]) 
    (r1, c1), color1 = non_white_pixels[0] # Pixel P1 (smaller row index)
    (r2, c2), color2 = non_white_pixels[1] # Pixel P2 (larger row index)

    # 4. Initialize output grid with white (0)
    output_np = np.zeros_like(input_np)

    # 5. Calculate vertical midpoint row index
    # Note: integer division `//` performs floor automatically in Python 3
    mid_row = height // 2 

    # 6. Draw the left vertical edge line (column 0)
    output_np[:mid_row, 0] = color1  # Top part
    output_np[mid_row:, 0] = color2  # Bottom part (includes mid_row itself)

    # 7. Draw the right vertical edge line (column W-1)
    output_np[:mid_row, width - 1] = color1 # Top part
    output_np[mid_row:, width - 1] = color2 # Bottom part

    # 8. Draw the top horizontal edge line (row 0)
    output_np[0, :] = color1

    # 9. Draw the bottom horizontal edge line (row H-1)
    output_np[height - 1, :] = color2

    # 10. Draw the horizontal line corresponding to P1 (row r1)
    output_np[r1, :] = color1

    # 11. Draw the horizontal line corresponding to P2 (row r2)
    # This will overwrite row r1 if r1 == r2, using color2, which is consistent
    # if we consider P2 the 'dominant' pixel in case of a tie in row index.
    # More importantly, it correctly overwrites the vertical edge lines at intersections.
    output_np[r2, :] = color2

    # 12. Return the result as a list of lists
    return output_np.tolist()