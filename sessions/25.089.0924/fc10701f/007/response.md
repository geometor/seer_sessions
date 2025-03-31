```python
"""
Replaces a Maroon object (9) with an Orange object (7), clears the original Orange 
location, and adds Red pixels (2) based on the relative alignment (Horizontal/Vertical) 
of the Maroon and Orange objects in the input grid. The background is Magenta (6).

Alignment Rules:
- Determined by bounding box overlap/identity. Horizontal preferred if ambiguous.

Red Pixel Placement Rules:
- If Horizontal Alignment:
  Red pixels are placed on the row(s) shared by the bounding boxes, in columns that 
  are strictly between the objects' column spans AND contain White (0) pixels anywhere
  in the input grid.
- If Vertical Alignment:
  Red pixels are placed on rows containing at least two distinct horizontal segments 
  of White pixels. On each such row, Red pixels replace Magenta pixels in two columns:
  1. The leftmost column shared by the original Maroon and Orange bounding boxes.
  2. The column immediately to the left of the starting column of the rightmost 
     White segment on that row.
"""

import numpy as np
from typing import List, Tuple, Set

# Define color constants
MAGENTA = 6
MAROON = 9
ORANGE = 7
WHITE = 0
RED = 2

def find_colored_pixels(grid: np.ndarray, color: int) -> List[Tuple[int, int]]:
    """Finds all coordinates (row, col) of pixels with a specific color."""
    rows, cols = np.where(grid == color)
    return list(zip(rows, cols))

def get_bounding_box(coords: List[Tuple[int, int]]) -> Tuple[int, int, int, int]:
    """Calculates the min_row, max_row, min_col, max_col for a set of coordinates."""
    if not coords:
        # Return invalid box if no coordinates
        return -1, -1, -1, -1
    rows = [r for r, c in coords]
    cols = [c for r, c in coords]
    return min(rows), max(rows), min(cols), max(cols)

def find_white_segments_on_row(row_slice: np.ndarray) -> List[Tuple[int, int]]:
    """Finds contiguous segments of White (0) on a single row slice.
       Returns a list of (start_col, end_col) tuples for each segment.
    """
    segments = []
    in_segment = False
    start_col = -1
    width = len(row_slice)
    for c, color in enumerate(row_slice):
        if color == WHITE and not in_segment:
            in_segment = True
            start_col = c
        elif color != WHITE and in_segment:
            in_segment = False
            segments.append((start_col, c - 1))
    # Handle segment ending at the edge
    if in_segment:
        segments.append((start_col, width - 1))
    return segments

def transform(input_grid: np.ndarray) -> np.ndarray:
    
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # Find coordinates of Maroon and Orange objects
    maroon_coords = find_colored_pixels(input_grid, MAROON)
    orange_coords = find_colored_pixels(input_grid, ORANGE)

    # If either object is missing, return the original grid copy
    if not maroon_coords or not orange_coords:
        return output_grid

    # Calculate bounding boxes
    maroon_min_r, maroon_max_r, maroon_min_c, maroon_max_c = get_bounding_box(maroon_coords)
    orange_min_r, orange_max_r, orange_min_c, orange_max_c = get_bounding_box(orange_coords)

    # Determine alignment based on bounding box properties
    rows_overlap = max(maroon_min_r, orange_min_r) <= min(maroon_max_r, orange_max_r)
    cols_overlap = max(maroon_min_c, orange_min_c) <= min(maroon_max_c, orange_max_c)

    is_horizontal_alignment = False
    is_vertical_alignment = False

    if maroon_min_r == orange_min_r and maroon_max_r == orange_max_r:
        is_horizontal_alignment = True
    elif maroon_min_c == orange_min_c and maroon_max_c == orange_max_c:
        is_vertical_alignment = True
    elif rows_overlap and not cols_overlap:
        is_horizontal_alignment = True
    elif cols_overlap and not rows_overlap:
        is_vertical_alignment = True
    elif rows_overlap and cols_overlap:
        # Default to horizontal if both overlap but spans are not identical
        is_horizontal_alignment = True
        
    # --- Perform Base Transformations ---
        
    # Clear original locations of both objects in output_grid (set to background)
    for r, c in maroon_coords:
        if 0 <= r < height and 0 <= c < width:
            output_grid[r, c] = MAGENTA
    for r, c in orange_coords:
         if 0 <= r < height and 0 <= c < width:
            # Check if the orange pixel wasn't already overwritten by Magenta
            # This handles cases where Maroon and Orange objects might touch or overlap.
            if output_grid[r, c] == ORANGE:
                output_grid[r, c] = MAGENTA

    # Place Orange color at Maroon's original location
    for r, c in maroon_coords:
        if 0 <= r < height and 0 <= c < width:
            output_grid[r, c] = ORANGE

    # --- Apply Alignment-Specific Rules for Placing Red Pixels ---
    if is_horizontal_alignment:
        # Identify shared rows using bounding boxes
        shared_rows = list(range(max(maroon_min_r, orange_min_r), min(maroon_max_r, orange_max_r) + 1))
        
        # Define the column range strictly *between* the objects
        between_start_col = min(maroon_max_c, orange_max_c) + 1
        between_end_col = max(maroon_min_c, orange_min_c) # Exclusive end (range is start to end-1)

        target_cols: Set[int] = set()
        # Check if there is actually space between the objects
        if between_start_col < between_end_col:
             # Find all columns containing any White pixel in the *input* grid
             white_pixels_coords = find_colored_pixels(input_grid, WHITE)
             white_cols = {c for r, c in white_pixels_coords}

             # Find the intersection of columns between objects and columns with white pixels
             for c in range(between_start_col, between_end_col):
                 if c in white_cols:
                     target_cols.add(c)

        # Place Red pixels on shared rows in the identified target columns
        for r in shared_rows:
             if 0 <= r < height: # Check row bounds
                for c in target_cols:
                    if 0 <= c < width: # Check column bounds
                        # Place Red, overwriting whatever is there (usually Magenta)
                        output_grid[r, c] = RED

    elif is_vertical_alignment:
        # Identify shared columns and the leftmost one
        shared_cols = list(range(max(maroon_min_c, orange_min_c), min(maroon_max_c, orange_max_c) + 1))
        
        # Handle potential edge case where alignment=vertical but no shared columns found
        # (e.g., touching corners). Use the leftmost of the two object starts as fallback.
        leftmost_shared_col = min(shared_cols) if shared_cols else min(maroon_min_c, orange_min_c) 
        
        # Iterate through all rows to check for multiple white segments
        for r in range(height):
            row_slice = input_grid[r, :]
            white_segments = find_white_segments_on_row(row_slice)

            # Check if the row contains two or more distinct white segments
            if len(white_segments) >= 2:
                # Find the rightmost white segment (the one with the largest start column)
                rightmost_segment = max(white_segments, key=lambda seg: seg[0])
                rightmost_segment_start_col = rightmost_segment[0]
                
                # Calculate the column immediately to the left of the rightmost segment's start
                col_left_of_rightmost_white = rightmost_segment_start_col - 1

                # Place Red pixel at the leftmost shared column on this row
                if 0 <= r < height and 0 <= leftmost_shared_col < width:
                     output_grid[r, leftmost_shared_col] = RED
                     
                # Place Red pixel at the column left of the rightmost white segment's start
                # Ensure the calculated column index is valid (>= 0)
                if 0 <= r < height and col_left_of_rightmost_white >= 0 and col_left_of_rightmost_white < width:
                     output_grid[r, col_left_of_rightmost_white] = RED

    return output_grid
```