```python
import numpy as np
from copy import deepcopy

"""
The transformation rule identifies maximal contiguous rectangular areas of white pixels (color 0). 
For each such white rectangle 'W':
1. It checks for a 'Vertical Bridge Below': Is there a monochromatic, non-white horizontal segment 'S' directly below W (sharing the same columns)? Is the entire rectangular space between W and S composed only of white pixels? If yes, W is filled with the color of S.
2. If the vertical check doesn't apply, it checks for a 'Horizontal Bridge': Are there monochromatic, non-white vertical segments 'SL' and 'SR' immediately to the left and right of W, respectively (sharing the same rows)? Do SL and SR have the *same* color? If yes, W is filled with that color.
The vertical check takes priority. Only one fill operation is applied per white rectangle.
"""

def find_maximal_white_rectangles(grid: np.ndarray) -> list[tuple[int, int, int, int]]:
    """
    Finds all maximal contiguous rectangular areas of white pixels (0).

    Args:
        grid: The input grid as a numpy array.

    Returns:
        A list of tuples, where each tuple represents a rectangle
        as (r1, c1, r2, c2) (top-left and bottom-right coordinates, inclusive).
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    rectangles = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 0 and not visited[r, c]:
                start_r, start_c = r, c
                
                # Find max width
                max_width = 0
                while start_c + max_width < cols and grid[start_r, start_c + max_width] == 0 and not visited[start_r, start_c + max_width]:
                    max_width += 1
                
                if max_width == 0: continue

                # Find max height for this width
                max_height = 0
                possible_height = True
                while start_r + max_height < rows and possible_height:
                    # Check if the entire row segment is white and unvisited
                    for w_offset in range(max_width):
                        if grid[start_r + max_height, start_c + w_offset] != 0 or visited[start_r + max_height, start_c + w_offset]:
                            possible_height = False
                            break
                    if possible_height:
                        max_height += 1
                    else:
                        break 

                # Record rectangle and mark visited
                if max_height > 0 and max_width > 0:
                    r1, c1 = start_r, start_c
                    r2, c2 = start_r + max_height - 1, start_c + max_width - 1
                    rectangles.append((r1, c1, r2, c2))
                    visited[r1:r2+1, c1:c2+1] = True
    return rectangles

def is_monochromatic_non_white(segment: np.ndarray) -> tuple[bool, int]:
    """Checks if a segment is monochromatic and not white (0)."""
    if segment.size == 0:
        return False, -1
    first_color = segment.flat[0]
    if first_color == 0:
        return False, 0
    if np.all(segment == first_color):
        return True, first_color
    return False, -1

def is_all_white(segment: np.ndarray) -> bool:
    """Checks if a segment contains only white pixels (0)."""
    if segment.size == 0: # An empty gap is considered "all white"
        return True
    return np.all(segment == 0)


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rules to fill specific white rectangles
    based on vertical or horizontal bridging patterns.
    """
    grid = np.array(input_grid, dtype=int)
    output_grid = np.copy(grid)
    rows, cols = grid.shape

    # Find all potential white rectangles to fill
    white_rectangles = find_maximal_white_rectangles(grid)

    # Process each white rectangle
    for r1, c1, r2, c2 in white_rectangles:
        filled = False # Flag to track if this rectangle was filled

        # --- 1. Vertical Bridging Check (Below) ---
        r_below = r2 + 1
        
        # Search for the first non-white row below the rectangle within its columns
        first_non_white_row_idx = -1
        for r_scan in range(r_below, rows):
            if np.any(grid[r_scan, c1 : c2 + 1] != 0):
                first_non_white_row_idx = r_scan
                break
        
        if first_non_white_row_idx != -1:
            # Check if the segment in that first non-white row is monochromatic non-white
            segment_below = grid[first_non_white_row_idx, c1 : c2 + 1]
            is_mono, fill_color = is_monochromatic_non_white(segment_below)

            if is_mono:
                # Check if the gap between the rectangle and the segment is all white
                gap_segment = grid[r_below : first_non_white_row_idx, c1 : c2 + 1]
                if is_all_white(gap_segment):
                    # Conditions met: Fill the rectangle
                    output_grid[r1 : r2 + 1, c1 : c2 + 1] = fill_color
                    filled = True

        # --- 2. Horizontal Bridging Check (Left and Right) ---
        if not filled:
            # Check conditions for potential left and right segments
            has_left = c1 > 0
            has_right = c2 < cols - 1

            if has_left and has_right:
                segment_left = grid[r1 : r2 + 1, c1 - 1]
                segment_right = grid[r1 : r2 + 1, c2 + 1]

                is_mono_left, color_left = is_monochromatic_non_white(segment_left)
                is_mono_right, color_right = is_monochromatic_non_white(segment_right)

                # Check if both sides are monochromatic, non-white, and the *same* color
                if is_mono_left and is_mono_right and color_left == color_right:
                    # Conditions met: Fill the rectangle
                    output_grid[r1 : r2 + 1, c1 : c2 + 1] = color_left
                    # No need to set 'filled = True' as it's the last check for this rectangle

    # Convert back to list of lists for the final output
    return output_grid.tolist()
```