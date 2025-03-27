import numpy as np
from typing import List, Tuple

"""
Transformation Rule:

1.  Initialize the `output_grid` as a copy of the `input_grid`.
2.  Identify all non-white pixels (color != 0) in the input grid as "source pixels". Store their row, column, and color.
3.  For each source pixel `(r, c, color)`:
    a. Fill the cells in the `output_grid` in the same row `r` from column `c + 1` to the rightmost column (`width - 1`) with the source pixel's `color`.
4.  Determine the color for the rightmost column (`width - 1`) for each row `i` from top to bottom (0 to `height - 1`):
    a. Find all source pixels `(sr, sc, scolor)` whose row `sr` is strictly less than the current row `i` (`sr < i`).
    b. If no such source pixels exist above row `i`, the rightmost cell `output_grid[i, width - 1]` remains unchanged by this step.
    c. If source pixels exist above row `i`:
        i. Find the maximum row index (`max_r`) among these source pixels.
        ii. Identify all source pixels located at this `max_r`.
        iii. Among those source pixels at `max_r`, find the one with the maximum column index (`max_c`).
        iv. Set the color of the cell `output_grid[i, width - 1]` to the color of this selected source pixel (the one at `max_r`, `max_c`). This overwrites any previous value in that cell, including values set by the horizontal projection step.
5.  Return the modified `output_grid`.
"""

def find_source_pixels(grid: np.ndarray) -> List[Tuple[int, int, int]]:
    """Finds all non-background pixels and returns their coordinates and color."""
    sources = []
    height, width = grid.shape
    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            if color != 0:
                sources.append((r, c, color))
    return sources

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule to the input grid.
    Projects colors horizontally to the right from each source pixel.
    Projects colors vertically down the rightmost column based on the lowest, rightmost source pixel above.
    """
    # Convert input to numpy array for easier processing
    input_np = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input
    output_grid = input_np.copy()
    height, width = output_grid.shape
    
    if height == 0 or width == 0:
        return [] # Handle empty grid case

    # Find all source pixels (non-white)
    sources = find_source_pixels(input_np)

    # --- Horizontal Projection ---
    # For each source pixel, fill the row to its right with its color
    for r, c, color in sources:
        if c + 1 < width: # Check if there's space to the right
            output_grid[r, c + 1:] = color

    # --- Vertical Projection (Rightmost Column) ---
    max_col_idx = width - 1
    for i in range(height): # Iterate through each row of the output grid
        # Find sources located strictly above the current row 'i'
        relevant_sources = [src for src in sources if src[0] < i]

        if not relevant_sources:
            # No sources above this row, the last column pixel remains as is (or as set by horizontal projection)
            continue 

        # Find the maximum row index among the relevant sources
        max_r = -1
        for sr, sc, scolor in relevant_sources:
             if sr > max_r:
                 max_r = sr
        
        # Filter sources that are at this maximum row 'max_r'
        sources_at_max_r = [src for src in relevant_sources if src[0] == max_r]

        # Among those at max_r, find the one with the maximum column index
        max_c = -1
        selected_source_color = -1 # Initialize with a value indicating no source found yet
        for sr, sc, scolor in sources_at_max_r:
            if sc > max_c:
                max_c = sc
                selected_source_color = scolor # Keep track of the color of the rightmost source

        # Set the color of the pixel in the rightmost column of the current row 'i'
        # This check ensures we only write if a valid source was determined
        if selected_source_color != -1: 
            output_grid[i, max_col_idx] = selected_source_color

    # Convert the result back to a list of lists
    return output_grid.tolist()