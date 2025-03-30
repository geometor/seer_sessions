"""
Draw crosses and mark intersections based on source pixels.

1.  Initialize the output grid as a copy of the input grid.
2.  Identify all non-white pixels in the input grid (source pixels), storing their locations (row, column) and colors.
3.  For each source pixel (color C at R, L):
    a.  Fill row R of the output grid with color C.
    b.  Fill column L of the output grid with color C.
4.  Iterate through all unique pairs of *different* source pixels (A at Ra, Ca and B at Rb, Cb):
    a.  Set the output pixel at (Ra, Cb) to Red (2).
    b.  Set the output pixel at (Rb, Ca) to Red (2).
5.  Re-iterate through all original source pixels (color C at R, L):
    a.  Set the output pixel at (R, L) back to its original color C, overriding any intersection color.
6.  Return the modified output grid.
"""

import numpy as np
from typing import List, Tuple

def find_source_pixels(grid: np.ndarray) -> List[Tuple[int, int, int]]:
    """Finds all non-white pixels and returns their row, column, and color."""
    sources = []
    height, width = grid.shape
    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            if color != 0: # 0 is white/background
                sources.append((r, c, color))
    return sources

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid by drawing crosses from source pixels and marking intersections.
    """
    # Convert input_grid to numpy array if it's not already
    if not isinstance(input_grid, np.ndarray):
        input_grid = np.array(input_grid, dtype=int)

    # 1. Initialize output_grid as a copy of input_grid
    #    We'll modify it in place for simplicity
    output_grid = input_grid.copy()
    height, width = output_grid.shape

    # 2. Identify all source pixels
    source_pixels = find_source_pixels(input_grid)

    # Handle cases with no source pixels
    if not source_pixels:
        return output_grid # Return the original grid if no sources found

    # 3. Draw horizontal and vertical lines for each source pixel
    for r, c, color in source_pixels:
        # a. Fill the entire row R with color C
        output_grid[r, :] = color
        # b. Fill the entire column L with color C
        output_grid[:, c] = color

    # 4. Mark intersections of lines from *different* source pixels with Red (2)
    num_sources = len(source_pixels)
    for i in range(num_sources):
        for j in range(i + 1, num_sources): # Iterate through unique pairs
            r1, c1, _ = source_pixels[i]
            r2, c2, _ = source_pixels[j]

            # a. Intersection of source A's row and source B's column
            output_grid[r1, c2] = 2 # Red
            # b. Intersection of source B's row and source A's column
            output_grid[r2, c1] = 2 # Red

    # 5. Restore the original color at the location of each source pixel
    for r, c, original_color in source_pixels:
        output_grid[r, c] = original_color

    # 6. Return the final grid
    return output_grid