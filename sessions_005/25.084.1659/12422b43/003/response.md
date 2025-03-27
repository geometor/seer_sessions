```python
"""
Transformation Rule:

1.  Initialize the output grid as a copy of the input grid.
2.  Identify all gray (5) pixels located in the first column (column 0). If none exist, return the unchanged output grid.
3.  Determine the minimum (`min_row_bar`) and maximum (`max_row_bar`) row indices among these gray pixels.
4.  Define the "pattern block" as the rectangular slice of the *input* grid covering rows from `min_row_bar` to `max_row_bar` (inclusive) and all columns *except* the first one (i.e., from column 1 to the end). Record the height of this pattern block (`pattern_height = max_row_bar - min_row_bar + 1`).
5.  If the grid width is 1 (only the gray bar column exists), the pattern block is empty; return the unchanged output grid.
6.  Find the maximum row index (`max_row_orig_content`) occupied by any non-white (0) and non-gray (5) pixel in the *entire* input grid. If no such pixels exist, treat `max_row_orig_content` as -1.
7.  Set the starting destination row for copying the pattern, `current_dest_row`, to `max_row_orig_content + 1`.
8.  Repeatedly perform the following copy operation as long as `current_dest_row` is less than the grid height:
    a.  Calculate the number of rows from the pattern block that can fit starting at `current_dest_row`, limited by the grid height (`rows_to_copy = min(pattern_height, grid_height - current_dest_row)`).
    b.  If `rows_to_copy` is 0 or less, stop the replication process.
    c.  Select the top `rows_to_copy` rows from the `pattern_block`.
    d.  Determine the destination slice in the `output_grid`: rows from `current_dest_row` to `current_dest_row + rows_to_copy - 1`, and columns from 1 to the end.
    e.  Copy the selected slice of the `pattern_block` to the destination slice in the `output_grid`.
    f.  Increment `current_dest_row` by `pattern_height` for the next iteration.
9.  Return the modified output grid.
"""

import numpy as np

def find_gray_bar_span(grid: np.ndarray) -> tuple[int | None, int | None]:
    """Finds the min and max row indices of the gray bar in column 0."""
    height = grid.shape[0]
    gray_rows = [r for r in range(height) if grid[r, 0] == 5]
    if not gray_rows:
        return None, None
    return min(gray_rows), max(gray_rows)

def find_max_content_row(grid: np.ndarray) -> int:
    """Finds the maximum row index of any non-white, non-gray pixel."""
    height, width = grid.shape
    max_row = -1
    for r in range(height):
        for c in range(width):
            if grid[r, c] not in [0, 5]:
                max_row = max(max_row, r)
    return max_row

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Replicates a pattern derived from the rows spanned by a leftmost gray bar,
    copying it downwards into the empty space below existing content.
    """
    # 1. Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # 2. Identify gray pixels in column 0 and determine span.
    min_row_bar, max_row_bar = find_gray_bar_span(output_grid)

    # If no gray bar, return the original grid.
    if min_row_bar is None:
        return output_grid

    # 5. If the grid width is 1, nothing to pattern/copy.
    if width <= 1:
        return output_grid

    # 4. Define the pattern block based on gray bar span and columns 1+.
    pattern_block = input_grid[min_row_bar : max_row_bar + 1, 1:width]
    pattern_height = pattern_block.shape[0]

    # If pattern height is zero (e.g., single pixel gray bar?), check needed?
    # Based on examples, pattern height >= 1 seems guaranteed if bar exists.
    if pattern_height == 0:
        return output_grid # Should not happen if min/max_row_bar are valid

    # 6. Find the maximum row of original non-white/non-gray content.
    max_row_orig_content = find_max_content_row(input_grid)

    # 7. Set the starting destination row for the first copy.
    current_dest_row = max_row_orig_content + 1

    # 8. Replicate the pattern downwards.
    while current_dest_row < height:
        # a. Calculate how many rows of the pattern can fit.
        rows_to_copy = min(pattern_height, height - current_dest_row)

        # b. If no rows can be copied, stop.
        if rows_to_copy <= 0:
            break

        # c. Get the slice of the pattern block to copy.
        source_block_slice = pattern_block[:rows_to_copy, :]

        # d. Determine destination slice in the output grid (cols 1+).
        dest_slice_rows = slice(current_dest_row, current_dest_row + rows_to_copy)
        dest_slice_cols = slice(1, width) # Copy only to columns 1 onwards

        # e. Perform the copy.
        output_grid[dest_slice_rows, dest_slice_cols] = source_block_slice

        # f. Update the destination row for the next potential copy.
        current_dest_row += pattern_height

    # 9. Return the modified grid.
    return output_grid
```