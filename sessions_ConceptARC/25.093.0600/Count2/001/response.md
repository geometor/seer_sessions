Warning: Response generation stopped. Finish Reason: MAX_TOKENS (2)
Partial text available:
---
```python
import sys
import numpy as np # numpy might be useful for grid operations if needed, but sticking to basic lists for now.

"""
Identifies the shape formed by '1's in the input grid, traces its perimeter, 
counts the number of distinct straight line segments (horizontal, vertical, or diagonal) 
forming the perimeter, and returns a list of '7's with length equal to the segment count.
"""

# Directions for Moore Neighbor Tracing (N, NE, E, SE, S, SW, W, NW)
# Ordered clockwise, starting North. Used for neighbor checking.
DIRECTIONS = [
    (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)
]

def find_pixels(grid, value=1):
    """Finds all coordinates (row, col) of cells with the given value."""
    pixels = []
    for r, row in enumerate(grid):
        # Ensure row is iterable (handle potential numpy arrays if used later)
        try:
            iter(row)
        except TypeError:
            # Handle non-iterable rows if necessary, though input spec suggests list of lists
            continue 
        for c, val in enumerate(row):
            if val == value:
                pixels.append((r, c))
    return pixels

def moore_neighbor_trace(start_pixel, pixels_set):
    """
    Performs Moore Neighbor Tracing to find the ordered boundary pixels of a shape.
    Args:
        start_pixel: The starting pixel (r, c) for tracing (e.g., top-most, left-most).
        pixels_set: A set containing coordinates (r, c) of all '1' pixels for fast lookup.
    Returns:
        A list of boundary pixel coordinates (r, c) in order, starting and ending near the start_pixel.
        Returns an empty list if tracing fails or the shape is invalid.
    """
    if not start_pixel or start_pixel not in pixels
---
