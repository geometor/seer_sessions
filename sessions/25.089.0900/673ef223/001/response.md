```python
import numpy as np
from typing import List, Tuple

"""
Transformation Rule:

1.  Identify the two vertical red (2) line segments in the input grid. Record their column indices and row ranges.
2.  Identify all azure (8) marker pixels in the input grid.
3.  Initialize the output grid as a copy of the input grid, but replace all azure (8) pixels with white (0).
4.  For each azure marker pixel at input coordinates (r, c):
    a. Determine which red line segment ('source') its row 'r' belongs to and identify the other segment ('target').
    b. On the output grid, place a yellow (4) pixel at the marker's original coordinates (r, c).
    c. Draw a horizontal azure (8) line segment in row 'r' starting from the column adjacent to the source red line and extending up to (but not including) column 'c'.
    d. Calculate the corresponding row 'r_target' in the target red line segment based on the relative position of 'r' within the source segment.
    e. Draw a horizontal azure (8) line segment in row 'r_target' that spans the full width between the two red lines (exclusive of the red line columns).
5.  The final output grid contains the original red lines, the generated yellow markers, and the two types of generated azure horizontal lines.
"""

def find_vertical_lines(grid: np.ndarray, color: int) -> List[Tuple[int, int, int]]:
    """
    Finds contiguous vertical line segments of a specific color.

    Args:
        grid: The input grid (numpy array).
        color: The color value to search for.

    Returns:
        A list of tuples, where each tuple represents a line:
        (column_index, start_row_index, end_row_index).
    """
    lines = []
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)

    for c in range(cols):
        for r in range(rows):
            if grid[r, c] == color and not visited[r, c]:
                start_r = r
                end_r = r
                visited[r, c] = True
                # Extend downwards
                curr_r = r + 1
                while curr_r < rows and grid[curr_r, c] == color:
                    visited[curr_r, c] = True
                    end_r = curr_r
                    curr_r += 1
                # Check if it's just a single point or a line segment
                # For this task, we consider single points as lines of length 1
                lines.append((c, start_r, end_r))
    return lines

def find_pixels(grid: np.ndarray, color: int) -> List[Tuple[int, int]]:
    """Finds all pixels of a specific color."""
    pixels = np.argwhere(grid == color)
    # Convert numpy array rows to tuples: [(r1, c1), (r2, c2), ...]
    return [tuple(p) for p in pixels]

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A 2D list representing the input grid.

    Returns:
        A 2D list representing the output grid.
    """
    input_arr = np.array(input_grid, dtype=int)
    output_arr = np.array(input_grid, dtype=int)
    rows, cols = input_arr.shape

    # Initialize output grid by removing azure markers
    output_arr[output_arr == 8] = 0

    # 1. Identify the two vertical red (2) line segments
    red_lines = find_vertical_lines(input_arr, 2)
    if len(red_lines) != 2:
        # Fallback or error handling if assumption is wrong
        # For now, return the initialized grid if structure isn't as expected
        print(f"Warning: Expected 2 red lines, found {len(red_lines)}. Returning initial state.")
        return output_arr.tolist()

    # Sort lines by column index to identify left and right
    red_lines.sort(key=lambda x: x[0])
    col_left, row_start_left, row_end_left = red_lines[0]
    col_right, row_start_right, row_end_right = red_lines[1]

    # 2. Identify all azure (8) marker pixels in the *original* input
    azure_markers = find_pixels(input_arr, 8)

    # 3 & 4. Process each azure marker
    for r, c in azure_markers:
        # a. Determine Source/Target
        source_col, target_col = -1, -1
        source_row_start, target_row_start = -1, -1
        is_left_source = False

        if row_start_left <= r <= row_end_left:
            source_col, target_col = col_left, col_right
            source_row_start, target_row_start = row_start_left, row_start_right
            is_left_source = True
        elif row_start_right <= r <= row_end_right:
            source_col, target_col = col_right, col_left
            source_row_start, target_row_start = row_start_right, row_start_left
            is_left_source = False
        else:
            # Marker not aligned with any red line's row range - skip?
            # Based on examples, this shouldn't happen.
            continue

        # b. Place yellow marker
        if 0 <= r < rows and 0 <= c < cols:
             output_arr[r, c] = 4

        # c. Draw same-side azure line
        if is_left_source:
            # Source is left red line
            fill_start_col = source_col + 1
            fill_end_col = c # Exclusive end for slicing
            if fill_start_col < fill_end_col:
                 output_arr[r, fill_start_col:fill_end_col] = 8
        else:
            # Source is right red line
            fill_start_col = c + 1
            fill_end_col = source_col # Exclusive end for slicing
            if fill_start_col < fill_end_col:
                 output_arr[r, fill_start_col:fill_end_col] = 8

        # d. Calculate target row
        relative_row = r - source_row_start
        r_target = target_row_start + relative_row

        # Check if target row is valid (should be if red lines have same height,
        # but good to check)
        # Also need to check if the corresponding target red line segment exists
        # at that row. Let's refine target row check:
        target_row_start_check, target_row_end_check = -1, -1
        if is_left_source: # Target is right
            target_row_start_check, target_row_end_check = row_start_right, row_end_right
        else: # Target is left
            target_row_start_check, target_row_end_check = row_start_left, row_end_left
            
        if not (target_row_start_check <= r_target <= target_row_end_check):
             # If the calculated target row is outside the bounds of the target red line, skip drawing
             # This might happen if red lines have different lengths - examples suggest they match up
             continue


        # e. Draw opposite-side azure line
        fill_start_col_opp = min(col_left, col_right) + 1
        fill_end_col_opp = max(col_left, col_right) # Exclusive end for slicing
        if 0 <= r_target < rows and fill_start_col_opp < fill_end_col_opp:
            output_arr[r_target, fill_start_col_opp:fill_end_col_opp] = 8

    # 5. Return the final grid
    return output_arr.tolist()
```