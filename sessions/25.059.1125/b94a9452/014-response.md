# b94a9452 • 014 • refine_coder

---
```python
"""
1.  **Identify Objects:** Find the horizontal line of blue (1) pixels and the single green (3) pixel.

2.  **Conditional Color Inversion:**
    *   If the green pixel is *below* the blue line (green pixel's row index is greater than the blue line's row index), swap the colors of the blue line and the green pixel. Blue pixels become green, and the green pixel becomes blue.
    *   Otherwise, do not change the colors.

3.  **Cropping:**
    *    If the colors were swapped (in step 2): Create a rectangle that tightly encloses all non-white pixels, extending the boundaries by one white pixel in every direction (top, bottom, left, and right) for padding.

    *    If no colors were swapped: Create a rectangle that includes only the row(s) containing the blue line and/or the green pixel.
        *   The top edge of this rectangle is the highest row index between the blue line and the green pixel.
        *   The bottom edge is the lowest row index between the blue line and the green pixel.
        *   The left edge is the smallest column index between the start of the blue line and the green pixel.
        *   The right edge is the largest column index between the end of the blue line and the green pixel. There is *no* padding added.
"""

import numpy as np

def find_horizontal_line(grid, color):
    """Finds the coordinates of a horizontal line of a specific color."""
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == color:
                line_coords = []
                col = c
                while col < len(grid[0]) and grid[r][col] == color:
                    line_coords.append((r, col))
                    col += 1
                if len(line_coords) > 1:  # Ensure it's a line, not a single pixel
                    return line_coords
    return []

def find_single_pixel(grid, color):
    """Finds the coordinates of a single pixel of a specific color."""
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == color:
                return (r, c)
    return None

def invert_colors(grid, blue_line_coords, green_pixel_coord):
    """Inverts the colors of the blue line and green pixel (1<->3)."""
    inverted_grid = [row[:] for row in grid]  # Deep copy
    for r, c in blue_line_coords:
        inverted_grid[r][c] = 3
    if green_pixel_coord:
        inverted_grid[green_pixel_coord[0]][green_pixel_coord[1]] = 1
    return inverted_grid

def crop_inverted(grid, non_white_coords):
    """Crops the grid to the smallest rectangle containing all non-white coords, plus padding."""
    if not non_white_coords:
        return []

    min_r = min(r for r, _ in non_white_coords)
    max_r = max(r for r, _ in non_white_coords)
    min_c = min(c for _, c in non_white_coords)
    max_c = max(c for _, c in non_white_coords)

    # Add padding
    min_r = max(0, min_r - 1)
    max_r = min(len(grid) - 1, max_r + 1)
    min_c = max(0, min_c - 1)
    max_c = min(len(grid[0]) - 1, max_c + 1)

    cropped_grid = []
    for r in range(min_r, max_r + 1):
        cropped_row = grid[r][min_c:max_c + 1]
        cropped_grid.append(cropped_row)
    return cropped_grid


def crop_non_inverted(grid, blue_line_coords, green_pixel_coord):
    """Crops to encompass blue line and green pixel."""
    min_r = min(blue_line_coords[0][0], green_pixel_coord[0])
    max_r = max(blue_line_coords[0][0], green_pixel_coord[0])
    min_c = min(blue_line_coords[0][1], green_pixel_coord[1])
    max_c = max(blue_line_coords[-1][1], green_pixel_coord[1])

    cropped_grid = []
    for r in range(min_r, max_r + 1):
        cropped_grid.append(grid[r][min_c:max_c+1])
    return cropped_grid

def transform(input_grid):
    # Find the blue horizontal line.
    blue_line_coords = find_horizontal_line(input_grid, 1)
    # Find the single green pixel.
    green_pixel_coord = find_single_pixel(input_grid, 3)

    if not blue_line_coords or green_pixel_coord is None:
      return input_grid

    # Conditional Color Inversion
    if green_pixel_coord[0] > blue_line_coords[0][0]:  # Green pixel is below
        inverted_grid = invert_colors(input_grid, blue_line_coords, green_pixel_coord)
        # calculate neighbors after inversion
        all_coords = []
        for r,c in blue_line_coords:
          all_coords.append((r,c))
        all_coords.append(green_pixel_coord)

        # Cropping (inverted case)
        output_grid = crop_inverted(inverted_grid, all_coords)
    else:  # Green pixel is within or above
        # Cropping (non-inverted case)
        output_grid = crop_non_inverted(input_grid, blue_line_coords, green_pixel_coord)

    return output_grid
```
