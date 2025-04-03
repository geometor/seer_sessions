```python
import numpy as np
from typing import List, Tuple

"""
Transformation Rule:

1. Identify the locations of all blue (1) pixels and magenta (6) pixels in the input grid.
2. Create a copy of the input grid for the output.
3. Determine the line drawing mode:
    a. If magenta pixels exist, draw lines from each magenta pixel to every blue pixel.
    b. If no magenta pixels exist, draw lines between every unique pair of blue pixels.
4. For each line segment determined in step 3:
    a. Calculate the integer coordinates of all pixels lying on the straight line connecting the start and end points of the segment.
    b. For each calculated pixel coordinate *except* the start and end points themselves:
        i. Change the color of the corresponding pixel in the output grid to blue (1).
5. Return the modified output grid.
"""

def find_pixels_by_color(grid: np.ndarray, color: int) -> List[Tuple[int, int]]:
    """Finds all pixels of a specific color in the grid."""
    rows, cols = np.where(grid == color)
    return list(zip(rows, cols))

def bresenham_line(r1: int, c1: int, r2: int, c2: int) -> List[Tuple[int, int]]:
    """
    Generates the integer coordinates of pixels forming a line between (r1, c1) and (r2, c2)
    using a Bresenham-like algorithm suitable for grid coordinates.
    Includes both start and end points.
    """
    points = []
    dr = abs(r2 - r1)
    dc = abs(c2 - c1)
    sr = 1 if r1 < r2 else -1
    sc = 1 if c1 < c2 else -1
    err = dr - dc

    r, c = r1, c1

    while True:
        points.append((r, c))
        if r == r2 and c == c2:
            break
        e2 = 2 * err
        if e2 > -dc:
            err -= dc
            r += sr
        if e2 < dr:
            err += dr
            c += sc
            
    # Ensure the exact endpoint is included if the loop terminates slightly early due to integer math
    # Although the standard Bresenham should handle this, double-check for grid contexts.
    # The standard implementation above correctly includes endpoints.
            
    return points

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the line drawing transformation based on blue and magenta pixels.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)

    # Find the locations of blue and magenta pixels
    blue_pixels = find_pixels_by_color(input_grid, 1)
    magenta_pixels = find_pixels_by_color(input_grid, 6)

    # Determine line drawing pairs
    line_pairs = []
    if magenta_pixels:
        # Mode 1: Connect each magenta to every blue
        for m_pos in magenta_pixels:
            for b_pos in blue_pixels:
                line_pairs.append((m_pos, b_pos))
    elif len(blue_pixels) > 1:
        # Mode 2: Connect every unique pair of blue pixels
        for i in range(len(blue_pixels)):
            for j in range(i + 1, len(blue_pixels)):
                line_pairs.append((blue_pixels[i], blue_pixels[j]))

    # Draw the lines by coloring intermediate path pixels blue
    for start_pos, end_pos in line_pairs:
        r1, c1 = start_pos
        r2, c2 = end_pos

        # Get all points on the line segment
        line_points = bresenham_line(r1, c1, r2, c2)

        # Color the intermediate points blue (skip start and end points)
        if len(line_points) > 2:  # Ensure there are intermediate points
            for r, c in line_points[1:-1]:
                # Only change background pixels, don't overwrite existing blue/magenta points
                # Although the description implies coloring regardless, example 1 output shows
                # a blue path pixel overlapping where an input blue pixel was, remaining blue.
                # The safest interpretation is to just set the path pixels to blue.
                # If a path pixel happens to be where an original blue/magenta pixel was,
                # setting it to blue again doesn't change anything important.
                output_grid[r, c] = 1

    return output_grid
```