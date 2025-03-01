# e9614598 • 004 • example_1 • investigate_coder

---
```python
"""
1.  **Identify** the two blue pixels (value 1) in the input grid.
2.  **Calculate** the midpoint between the two blue pixels.
3.  **Create** a green pixel (value 3) at the calculated midpoint.
4.  **Create** four additional green pixels (value 3) directly adjacent (above, below, left, and right) to the central green pixel, forming a cross shape.
5. **Preserve** all other pixels, including the original two blue, as they were in their original positions.
"""

import numpy as np

def find_pixels_by_color(grid, color):
    """Finds the coordinates of all pixels of a specified color."""
    return np.argwhere(grid == color)

def calculate_midpoint(coords):
    """Calculates the midpoint between two coordinates."""
    return np.mean(coords, axis=0).astype(int)

def transform(input_grid):
    """Transforms the input grid according to the defined rule."""

    # Initialize output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Find the coordinates of the blue pixels (color 1).
    blue_pixels = find_pixels_by_color(input_grid, 1)

    # If there are exactly two blue pixels, proceed.
    if len(blue_pixels) == 2:
        # Calculate the midpoint between the two blue pixels.
        midpoint = calculate_midpoint(blue_pixels)

        # Create the central green pixel.
        output_grid[midpoint[0], midpoint[1]] = 3

        # Create the surrounding green pixels (cross shape).
        row, col = midpoint
        output_grid[row - 1, col] = 3  # Above
        output_grid[row + 1, col] = 3  # Below
        output_grid[row, col - 1] = 3  # Left
        output_grid[row, col + 1] = 3  # Right

    return output_grid
```
