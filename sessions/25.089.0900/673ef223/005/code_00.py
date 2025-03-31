import numpy as np
from typing import List, Tuple

"""
Transformation Rule:

1.  Initialize the `output_grid` as a copy of the `input_grid`. Replace all azure (8) pixels in the `output_grid` with white (0).
2.  Identify the two vertical red (2) line segments in the `input_grid`. Record their column indices (`col_left`, `col_right`) and their starting and ending row indices (`row_start_left`, `row_end_left`, `row_start_right`, `row_end_right`). Assume `col_left < col_right`.
3.  Find the coordinates (`r`, `c`) of all azure (8) pixels in the *original* `input_grid`.
4.  For each found azure pixel at input coordinates (`r`, `c`):
    a.  Determine which red segment is 'source' based on `r`'s row range, and which is 'target'. Note the corresponding `source_col`, `target_col`, `source_row_start`, `target_row_start`, and `target_row_end`. Skip the marker if `r` doesn't align with either segment's row range.
    b.  Generate the "same-side" line:
        *   Set the pixel at (`r`, `c`) in the `output_grid` to yellow (4).
        *   Draw an azure (8) horizontal line segment in row `r` starting adjacent to the source red line and ending just before column `c`.
    c.  Generate the "opposite-side" line:
        *   Calculate the corresponding target row `r_target` based on `r`'s relative position within the source segment.
        *   Check if `r_target` is valid (within the target segment's row range and grid bounds).
        *   If `r_target` is valid, draw an azure (8) horizontal line segment in row `r_target`. This line starts *at* the column corresponding to the source line (`source_col`) and ends *just before* the column corresponding to the target line (`target_col`), effectively overwriting the original red pixel at (`r_target`, `source_col`) but preserving the one at (`r_target`, `target_col`).
5.  Return the final `output_grid`.
"""

def find_vertical_lines(grid: np.ndarray, color: int) -> List[Tuple[int, int, int]]:
    """
    Finds contiguous vertical line segments of a specific color.

    Args:
        grid: The input grid (numpy array).
        color: The color value to search for.

    Returns:
        A list of tuples, where each tuple represents a line:
        (column_index, start_row_index, end_row_index). Returns empty list if no lines found.
    """
    lines = []
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)

    for c in range(cols):
        for r in range(rows):
            if grid[r, c] == color and not visited[r, c]:
                start_r = r
                end_r = r
                # Mark current pixel visited
                visited[r, c] = True
                # Extend downwards contiguously
                curr_r = r + 1
                while curr_r < rows and grid[curr_r, c] == color:
                    visited[curr_r, c] = True
                    end_r = curr_r
                    curr_r += 1
                # Store the found segment
                lines.append((c, start_r, end_r))
                # No need to mark visited again, done inside loop
                
    return lines

def find_pixels(grid: np.ndarray, color: int) -> List[Tuple[int, int]]:
    """Finds all pixels of a specific color."""
    pixels = np.argwhere(grid == color)
    # Convert numpy array rows to tuples: [(r1, c1), (r2, c2), ...]
    return [tuple(p) for p in pixels]


def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule to the input grid.
    """
    input_arr = np.array(input_grid, dtype=int)
    output_arr = np.array(input_grid, dtype=int)
    rows, cols = input_arr.shape

    # 1. Initialize output grid by removing azure markers
    output_arr[output_arr == 8] = 0

    # 2. Identify the two vertical red (2) line segments
    red_lines = find_vertical_lines(input_arr, 2)
    if len(red_lines) != 2:
        # If structure isn't as expected, return the initialized grid.
        return output_arr.tolist()

    # Sort lines by column index to identify left and right
    red_lines.sort(key=lambda x: x[0])
    col_left, row_start_left, row_end_left = red_lines[0]
    col_right, row_start_right, row_end_right = red_lines[1]

    # 3. Identify all azure (8) marker pixels in the *original* input
    azure_markers = find_pixels(input_arr, 8)

    # 4. Process each azure marker
    for r, c in azure_markers:
        # a. Determine Source/Target
        source_col, target_col = -1, -1
        source_row_start, target_row_start, target_row_end = -1, -1, -1
        is_left_source = False

        # Check if marker row aligns with left red segment
        if row_start_left <= r <= row_end_left:
            source_col, target_col = col_left, col_right
            source_row_start = row_start_left
            target_row_start, target_row_end = row_start_right, row_end_right
            is_left_source = True
        # Check if marker row aligns with right red segment
        elif row_start_right <= r <= row_end_right:
            source_col, target_col = col_right, col_left
            source_row_start = row_start_right
            target_row_start, target_row_end = row_start_left, row_end_left
            is_left_source = False
        else:
            # Marker not aligned with any red line's row range - skip this marker
            continue

        # b. Generate Same-Side Line
        # Place yellow marker
        if 0 <= r < rows and 0 <= c < cols:
             output_arr[r, c] = 4
        
        # Draw azure segment leading to marker
        if is_left_source:
            # Source is left red line, fill from col_left+1 up to c
            fill_start_col = source_col + 1
            fill_end_col = c # Exclusive end for slicing/range
            if fill_start_col < fill_end_col: # Ensure valid range
                 output_arr[r, fill_start_col:fill_end_col] = 8
        else:
            # Source is right red line, fill from c+1 up to col_right
            fill_start_col = c + 1
            fill_end_col = source_col # Exclusive end for slicing/range
            if fill_start_col < fill_end_col: # Ensure valid range
                 output_arr[r, fill_start_col:fill_end_col] = 8

        # c. Generate Opposite-Side Line
        # Calculate potential target row
        relative_row = r - source_row_start
        r_target = target_row_start + relative_row

        # Validate target row: within grid and within target segment's row span
        if not (0 <= r_target < rows and target_row_start <= r_target <= target_row_end):
             # If the calculated target row is invalid, skip drawing opposite line
             continue

        # Draw azure segment on the opposite side
        # The line should start *at* the source column and end *before* the target column
        fill_start_col_opp = -1
        fill_end_col_opp = -1
        
        if is_left_source: # Source=Left, Target=Right
            fill_start_col_opp = source_col # col_left (inclusive)
            fill_end_col_opp = target_col   # col_right (exclusive)
        else: # Source=Right, Target=Left
            # Need to fill from left+1 up to right+1 (exclusive) to achieve the visual effect
            # i.e., columns from target_col+1 up to source_col+1
            fill_start_col_opp = target_col + 1 # col_left + 1 (inclusive)
            fill_end_col_opp = source_col + 1   # col_right + 1 (exclusive)

        # Apply the fill if the range is valid
        if fill_start_col_opp < fill_end_col_opp:
            output_arr[r_target, fill_start_col_opp:fill_end_col_opp] = 8

    # 5. Return the final grid
    return output_arr.tolist()