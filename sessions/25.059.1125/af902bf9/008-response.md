# af902bf9 • 008 • refine_coder

---
```python
"""
1.  **Identify Markers:** Find all yellow (4) pixels in the input grid. These pixels act as markers.
2.  **Find Center:** Calculate the center point of the *yellow markers*.
    *   If no yellow markers are present, the output is identical to the input.
3.  **Place Red Pixel:** Add a red (2) pixel to the output grid at the calculated center coordinate.
4.  **Output:** The output is a copy of the input with a red pixel added at the center of the shape defined by yellow markers, unless no yellow markers are present, in which case output and input are identical.
"""

import numpy as np

def find_pixels_by_value(grid, value):
    """Finds coordinates of pixels with a specific value."""
    return np.argwhere(grid == value)

def calculate_center(coordinates):
    """Calculates the center point based on a set of coordinates."""
    return np.mean(coordinates, axis=0).astype(int)

def transform(input_grid):
    """Transforms the input grid according to the described rule."""

    # initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)

    # Find marker pixels (value 4)
    marker_pixels = find_pixels_by_value(input_grid, 4)

    # Calculate center point
    if len(marker_pixels) > 0:  # Proceed only if markers are present
        center_point = calculate_center(marker_pixels)

        # Add center pixel (value 2)
        output_grid[center_point[0], center_point[1]] = 2

    return output_grid
```

