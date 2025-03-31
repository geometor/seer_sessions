
Previous Code:
```python
"""
Moves an Orange object (7) to the location of a Maroon object (9) and adds 
Red pixels (2) based on the relative alignment (Horizontal/Vertical) of the 
two objects and the positions of White pixels/objects (0) in the input grid. 
The background color is Magenta (6).

If alignment is Horizontal:
Red pixels replace White pixels located on the shared row(s) and strictly 
between the column spans of the Maroon and Orange objects. The specific columns 
are identified by finding White pixels within the 'between' range on any shared 
row, and then applying Red to those columns across all shared rows.

If alignment is Vertical:
Red pixels are added on rows that contain at least two distinct horizontal 
segments of White pixels. On each such row, Red pixels are placed in two columns:
1. The leftmost column shared by the original Maroon and Orange objects.
2. The column immediately to the left of the starting column of the 
   rightmost White segment on that row.
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
    """Applies the transformation rules to the input grid."""
    
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

    # Determine alignment
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

    # Clear original locations of both objects in output_grid
    for r, c in maroon_coords:
        output_grid[r, c] = MAGENTA
    for r, c in orange_coords:
        # Check if the orange pixel wasn't already overwritten by Magenta
        # (in case Maroon and Orange objects touched or overlapped)
        if output_grid[r, c] == ORANGE:
            output_grid[r, c] = MAGENTA

    # Place Orange color at Maroon's original location
    for r, c in maroon_coords:
        output_grid[r, c] = ORANGE

    # Apply alignment-specific rules for placing Red pixels
    if is_horizontal_alignment:
        # Identify shared rows
        shared_rows = list(range(max(maroon_min_r, orange_min_r), min(maroon_max_r, orange_max_r) + 1))
        
        # Define the column range strictly *between* the objects
        between_start_col = min(maroon_max_c, orange_max_c) + 1
        between_end_col = max(maroon_min_c, orange_min_c) # Exclusive end

        target_cols: Set[int] = set()
        # Check if there is actually space between the objects
        if between_start_col < between_end_col:
            # Iterate through shared rows to find white pixels in the 'between' zone
            for r in shared_rows:
                 # Ensure row index is valid
                 if 0 <= r < height:
                    for c in range(between_start_col, between_end_col):
                         # Check bounds for column and check color in INPUT grid
                         if 0 <= c < width and input_grid[r, c] == WHITE:
                             target_cols.add(c)

        # Place Red pixels on shared rows in the identified target columns
        for r in shared_rows:
             if 0 <= r < height: # Check row bounds
                for c in target_cols:
                    if 0 <= c < width: # Check column bounds
                        output_grid[r, c] = RED

    elif is_vertical_alignment:
        # Identify shared columns and the leftmost one
        shared_cols = list(range(max(maroon_min_c, orange_min_c), min(maroon_max_c, orange_max_c) + 1))
        
        # Handle case where alignment detected but no columns technically shared (e.g., touching corners)
        # Use the minimum of the start columns as a fallback
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
                if 0 <= r < height and 0 <= col_left_of_rightmost_white < width:
                     output_grid[r, col_left_of_rightmost_white] = RED

    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 9 9 6 6 6 6
6 6 6 6 6 6 9 9 6 6 6 6
6 6 6 6 0 0 6 6 0 0 6 6
6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 0 0 6 6 0 0 6 6
6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 0 0 6 6 0 0 6 6
6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 7 7 6 6 6 6
6 6 6 6 6 6 7 7 6 6 6 6
```
Expected Output:
```
6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 7 7 6 6 6 6
6 6 6 6 6 6 7 7 6 6 6 6
6 6 6 6 0 0 2 2 0 0 6 6
6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 0 0 2 2 0 0 6 6
6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 0 0 2 2 0 0 6 6
6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6
```
Transformed Output:
```
6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 7 7 6 6 6 6
6 6 6 6 6 6 7 7 6 6 6 6
6 6 6 6 0 0 2 2 0 0 6 6
6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 0 0 2 2 0 0 6 6
6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 0 0 2 2 0 0 6 6
6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0

## Example 2:
Input:
```
6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6
6 6 6 0 6 0 6 6
6 6 6 0 6 0 6 6
6 7 6 6 6 6 6 9
6 6 6 0 6 0 6 6
6 6 6 0 6 0 6 6
6 6 6 6 6 6 6 6
```
Expected Output:
```
6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6
6 6 6 0 6 0 6 6
6 6 6 0 6 0 6 6
6 6 6 2 6 2 6 7
6 6 6 0 6 0 6 6
6 6 6 0 6 0 6 6
6 6 6 6 6 6 6 6
```
Transformed Output:
```
6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6
6 6 6 0 6 0 6 6
6 6 6 0 6 0 6 6
6 6 6 6 6 6 6 7
6 6 6 0 6 0 6 6
6 6 6 0 6 0 6 6
6 6 6 6 6 6 6 6
```
Match: False
Pixels Off: 2
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 6.25

## Example 3:
Input:
```
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 0 6 0 6 0 6 0 6 6 0 6 6 6 6 6
6 0 6 0 6 0 6 0 6 6 0 6 6 6 6 6
6 6 6 6 9 9 6 6 6 6 6 6 7 7 6 6
6 6 6 6 9 9 6 6 6 6 6 6 7 7 6 6
6 0 6 0 6 0 6 0 6 6 0 6 6 6 6 6
6 0 6 0 6 0 6 0 6 6 0 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
```
Expected Output:
```
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 0 6 0 6 0 6 0 6 6 0 6 6 6 6 6
6 0 6 0 6 0 6 0 6 6 0 6 6 6 6 6
6 6 6 6 7 7 6 2 6 6 2 6 6 6 6 6
6 6 6 6 7 7 6 2 6 6 2 6 6 6 6 6
6 0 6 0 6 0 6 0 6 6 0 6 6 6 6 6
6 0 6 0 6 0 6 0 6 6 0 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
```
Transformed Output:
```
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 0 6 0 6 0 6 0 6 6 0 6 6 6 6 6
6 0 6 0 6 0 6 0 6 6 0 6 6 6 6 6
6 6 6 6 7 7 6 6 6 6 6 6 6 6 6 6
6 6 6 6 7 7 6 6 6 6 6 6 6 6 6 6
6 0 6 0 6 0 6 0 6 6 0 6 6 6 6 6
6 0 6 0 6 0 6 0 6 6 0 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
```
Match: False
Pixels Off: 4
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 3.125
