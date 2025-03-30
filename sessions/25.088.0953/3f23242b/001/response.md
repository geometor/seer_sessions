```python
import numpy as np
from typing import List, Tuple, Set

"""
Transformation Rule Description:

1.  Identify all green (3) pixels in the input grid. These are trigger points.
2.  Initialize the output grid as a copy of the input grid.
3.  Define a fixed 5x5 stamp pattern centered around a trigger point.
    The pattern uses colors: white (0), red (2), green (3), gray (5), azure (8).
    The pattern relative to the center (0,0) is:
        Row -2: Gray, Gray, Gray, Gray, Gray
        Row -1: Red, White, Gray, White, Red
        Row 0 : Red, White, Green, White, Red  (Original trigger pixel is here)
        Row +1: Red, White, White, White, Red
        Row +2: Azure, Azure, Azure, Azure, Azure
4.  Keep track of the coordinates of all azure (8) pixels placed by any stamp.
5.  Keep track of the row indices where horizontal red (2) lines should be drawn. A line should be drawn at `row + 2` for each trigger pixel found at `row`.
6.  For each identified green pixel location (r, c):
    a.  Place the 5x5 stamp pattern onto the output grid, centered at (r, c). Handle boundary conditions (parts of the stamp outside the grid are ignored).
    b.  Record the coordinates of any azure (8) pixels placed by this stamp.
    c.  Record the row index `r + 2` as needing a horizontal red line.
7.  After placing all stamps, draw the horizontal red lines:
    a.  For each unique row index `R` identified in step 5c:
        i.  Iterate through all columns `C` of the grid.
        ii. Check if the coordinate (R, C) corresponds to an azure pixel placed by *any* stamp (recorded in step 6b).
        iii. If (R, C) is within the grid bounds and is *not* a recorded azure pixel location, set the pixel at `output_grid[R, C]` to red (2). This overwrites any existing pixel value (including parts of stamps other than azure, or the original background).
8.  Return the modified output grid.
"""

def find_pixels(grid: np.ndarray, color: int) -> List[Tuple[int, int]]:
    """Finds all coordinates (row, col) of pixels with a specific color."""
    rows, cols = np.where(grid == color)
    return list(zip(rows, cols))

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the stamping and line-drawing transformation to the input grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_np)
    height, width = input_np.shape

    # Define the stamp pattern relative to the center (0,0)
    # (dr, dc) -> color
    stamp_pattern_relative = {
        # Row -2
        (-2, -2): 5, (-2, -1): 5, (-2, 0): 5, (-2, 1): 5, (-2, 2): 5,
        # Row -1
        (-1, -2): 2, (-1, -1): 0, (-1, 0): 5, (-1, 1): 0, (-1, 2): 2,
        # Row 0
        (0, -2): 2, (0, -1): 0, (0, 0): 3, (0, 1): 0, (0, 2): 2,
        # Row +1
        (1, -2): 2, (1, -1): 0, (1, 0): 0, (1, 1): 0, (1, 2): 2,
        # Row +2
        (2, -2): 8, (2, -1): 8, (2, 0): 8, (2, 1): 8, (2, 2): 8,
    }

    # Find coordinates of all green pixels (triggers)
    green_pixel_locations = find_pixels(input_np, 3)

    # Sets to track where azure pixels are placed and which rows need red lines
    azure_pixel_coordinates: Set[Tuple[int, int]] = set()
    red_line_rows: Set[int] = set()

    # --- Phase 1: Place stamps and record azure locations/red line rows ---
    for r_center, c_center in green_pixel_locations:
        # Record the row for the horizontal red line
        red_line_row_index = r_center + 2
        if 0 <= red_line_row_index < height:
            red_line_rows.add(red_line_row_index)

        # Apply the stamp centered at (r_center, c_center)
        for (dr, dc), color in stamp_pattern_relative.items():
            r_abs = r_center + dr
            c_abs = c_center + dc

            # Check if the absolute coordinate is within the grid bounds
            if 0 <= r_abs < height and 0 <= c_abs < width:
                # Place the stamp pixel
                output_grid[r_abs, c_abs] = color
                # If it's an azure pixel, record its coordinate
                if color == 8:
                    azure_pixel_coordinates.add((r_abs, c_abs))

    # --- Phase 2: Draw horizontal red lines, avoiding azure pixels ---
    for r_line in red_line_rows:
        for c in range(width):
            coord = (r_line, c)
            # Only draw red if the coordinate is not an azure pixel location
            if coord not in azure_pixel_coordinates:
                 output_grid[r_line, c] = 2 # Red color

    # Convert back to list of lists for the expected output format
    return output_grid.tolist()
```