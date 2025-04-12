import numpy as np
from copy import deepcopy

"""
The transformation rule identifies maximal contiguous rectangular areas 'W' composed entirely of white pixels (color 0).
For each identified white rectangle W:
1. A size constraint is applied: If the height H > 2 AND width W > 2, the rectangle is skipped.
2. If the size constraint is met, a 'Vertical Bridge Below' check is performed:
   a. Search downwards from W's bottom edge (within W's columns) for the first row 'r_below' containing a non-white pixel.
   b. If found, check if the segment 'S_below' at r_below (within W's columns) is monochromatic non-white (color C).
   c. Check if the rectangular gap 'G' between W and S_below is entirely white.
   d. If all conditions are met, fill W in the output grid with color C.
3. If the Vertical Bridge check did not result in a fill, a 'Horizontal Extension Left' check is performed:
   a. Check if a column exists immediately left of W.
   b. Check if the vertical segment 'S_left' adjacent to W's left edge is monochromatic non-white (color C).
   c. If yes, fill W in the output grid with color C.
4. If neither of the above checks resulted in a fill, a 'Horizontal Extension Right' check is performed:
   a. Check if a column exists immediately right of W.
   b. Check if the vertical segment 'S_right' adjacent to W's right edge is monochromatic non-white (color C).
   c. If yes, fill W in the output grid with color C.
The checks are prioritized: Vertical Below > Horizontal Left > Horizontal Right. Only the first matching rule triggers a fill for a given rectangle W.
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
            # Start search if pixel is white and not already part of a found rectangle
            if grid[r, c] == 0 and not visited[r, c]:
                start_r, start_c = r, c
                
                # Find max width starting from (r, c) in the current row
                current_width = 0
                while start_c + current_width < cols and \
                      grid[start_r, start_c + current_width] == 0 and \
                      not visited[start_r, start_c + current_width]:
                    current_width += 1
                
                if current_width == 0: continue # Should not happen based on initial check

                # Find max height for this width, ensuring all rows are contiguous white rectangles
                current_height = 0
                possible_height = True
                while start_r + current_height < rows and possible_height:
                    # Check if the entire segment in this row matches the width and is white/unvisited
                    all_white_and_unvisited = True
                    for w_offset in range(current_width):
                        if start_c + w_offset >= cols or \
                           grid[start_r + current_height, start_c + w_offset] != 0 or \
                           visited[start_r + current_height, start_c + w_offset]:
                            all_white_and_unvisited = False
                            break
                    
                    if all_white_and_unvisited:
                        current_height += 1
                    else:
                        possible_height = False # Stop extending height

                # If a valid rectangle is found, store it and mark visited
                if current_height > 0 and current_width > 0:
                    r1, c1 = start_r, start_c
                    r2, c2 = start_r + current_height - 1, start_c + current_width - 1
                    rectangles.append((r1, c1, r2, c2))
                    # Mark pixels within this maximal rectangle as visited
                    visited[r1:r2+1, c1:c2+1] = True
    return rectangles

def is_monochromatic_non_white(segment: np.ndarray) -> tuple[bool, int]:
    """
    Checks if a numpy array segment is monochromatic (all same color) and not white (0).

    Args:
        segment: The numpy array segment to check.

    Returns:
        A tuple (is_mono_non_white, color).
        is_mono_non_white is True if the conditions are met, False otherwise.
        color is the monochromatic color if conditions are met, otherwise -1 (or 0 if white).
    """
    if segment.size == 0:
        return False, -1 # Cannot be monochromatic if empty
    first_color = segment.flat[0]
    if first_color == 0:
        return False, 0 # It's white
    if np.all(segment == first_color):
        return True, int(first_color) # Monochromatic and non-white
    return False, -1 # Not monochromatic

def is_all_white(segment: np.ndarray) -> bool:
    """
    Checks if a numpy array segment contains only white pixels (0).

    Args:
        segment: The numpy array segment to check.

    Returns:
        True if all pixels are 0, False otherwise. An empty segment is considered all white.
    """
    if segment.size == 0: 
        return True # An empty gap between W and S is valid
    return np.all(segment == 0)


def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    # Convert input to numpy array for efficient operations
    grid = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(grid)
    rows, cols = grid.shape

    # Find all maximal white rectangles
    white_rectangles = find_maximal_white_rectangles(grid)

    # Iterate through each found white rectangle W
    for r1, c1, r2, c2 in white_rectangles:
        filled = False # Flag to track if this rectangle has been filled by a rule

        # Calculate height (H) and width (W)
        rect_h = r2 - r1 + 1
        rect_w = c2 - c1 + 1

        # 1. Apply Size Constraint Filter
        if rect_h > 2 and rect_w > 2:
            continue # Skip this rectangle if it's too large in both dimensions

        # 2. Perform Vertical Bridge Below Check
        # Search for the first row below W containing a non-white pixel within W's columns
        first_non_white_row_idx = -1
        for r_scan in range(r2 + 1, rows):
            segment_in_row = grid[r_scan, c1 : c2 + 1]
            if np.any(segment_in_row != 0):
                first_non_white_row_idx = r_scan
                break
        
        # If such a row was found within grid bounds
        if first_non_white_row_idx != -1:
            # Extract the segment S_below in that row
            segment_below = grid[first_non_white_row_idx, c1 : c2 + 1]
            # Check if S_below is monochromatic non-white
            is_mono, fill_color = is_monochromatic_non_white(segment_below)

            if is_mono:
                # Extract the gap region G between W and S_below
                gap_segment = grid[r2 + 1 : first_non_white_row_idx, c1 : c2 + 1]
                # Check if the gap G is entirely white
                if is_all_white(gap_segment):
                    # All conditions met: Fill W in the output grid
                    output_grid[r1 : r2 + 1, c1 : c2 + 1] = fill_color
                    filled = True # Mark as filled

        # 3. Perform Horizontal Extension Left Check (only if not filled yet)
        if not filled:
            # Check if a column exists to the left
            if c1 > 0:
                # Extract the vertical segment S_left immediately to the left of W
                segment_left = grid[r1 : r2 + 1, c1 - 1]
                # Check if S_left is monochromatic non-white
                is_mono, fill_color = is_monochromatic_non_white(segment_left)
                
                if is_mono:
                    # Conditions met: Fill W in the output grid
                    output_grid[r1 : r2 + 1, c1 : c2 + 1] = fill_color
                    filled = True # Mark as filled

        # 4. Perform Horizontal Extension Right Check (only if not filled yet)
        if not filled:
             # Check if a column exists to the right
             if c2 < cols - 1:
                # Extract the vertical segment S_right immediately to the right of W
                segment_right = grid[r1 : r2 + 1, c2 + 1]
                # Check if S_right is monochromatic non-white
                is_mono, fill_color = is_monochromatic_non_white(segment_right)

                if is_mono:
                    # Conditions met: Fill W in the output grid
                    output_grid[r1 : r2 + 1, c1 : c2 + 1] = fill_color
                    # No need to set filled=True as it's the last check

    # Convert the final output grid back to a list of lists
    return output_grid.tolist()