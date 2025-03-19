"""
1.  **Preserve Gray Lines:** Keep all gray (5) pixels in their original positions.
2.  **Identify Target Section:** Find the smallest rectangular section that *encloses all* initial green (3) pixels. This section's edges are defined by the gray lines, but it must be adjacent to at least one green pixel in the input on each of its sides. The target section must not have any gray pixels inside the rectangle.
3.  **Remove Green Pixels Outside Target:** Change all green pixels outside the target section to white (0).
4.  **Consolidate Green Pixels Inside Target:**
    *   Count the *original* number of green pixels within the identified target section.
    *   Remove all green pixels from the target section
    *   If the original count was greater than or equal to 9, place a 3x3 square of green pixels in the bottom-right corner of the target section.
    *   If the original count was greater than 0 and less than 9, place a horizontal line of green pixels along the bottom edge of the target section, starting from the rightmost position. The length of the line equals the original green pixel count.
    * If the count is 0, remove all green pixels
"""

import numpy as np

def _find_target_section(grid):
    """Finds the smallest rectangle enclosing all green pixels, bordered by gray lines."""
    rows, cols = grid.shape
    green_rows, green_cols = np.where(grid == 3)

    if len(green_rows) == 0:
        return 0, rows, 0, cols  # No green pixels, return entire grid

    min_row, max_row = np.min(green_rows), np.max(green_rows)
    min_col, max_col = np.min(green_cols), np.max(green_cols)

    # Expand the section to include adjacent gray lines
    # and make sure, it does not contains any gray line inside

    # Expand up
    while min_row > 0 and 5 not in grid[min_row-1,min_col:max_col+1]  :
      min_row -= 1

    # Expand down
    while max_row < rows - 1 and 5 not in grid[max_row+1,min_col:max_col+1]:
      max_row += 1
    
    # Expand left
    while min_col > 0 and 5 not in grid[min_row:max_row+1,min_col-1]:
      min_col -= 1
    
    # Expand right
    while max_col < cols-1 and 5 not in grid[min_row:max_row+1, max_col+1]:
      max_col += 1
    
    return min_row, max_row + 1, min_col, max_col + 1


def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Identify Target Section:
    target_row_start, target_row_end, target_col_start, target_col_end = _find_target_section(input_grid)

    # Count original green pixels within target section
    original_num_green = np.sum(input_grid[target_row_start:target_row_end, target_col_start:target_col_end] == 3)
    
    # Remove Green Pixels Outside Target:
    for r in range(rows):
        for c in range(cols):
            if not (target_row_start <= r < target_row_end and target_col_start <= c < target_col_end):
                if output_grid[r, c] == 3:
                    output_grid[r, c] = 0

    # remove all green pixels from the target section
    for r in range(target_row_start, target_row_end):
        for c in range(target_col_start, target_col_end):
            output_grid[r,c] = 0 if output_grid[r,c] == 3 else output_grid[r,c] #reset all greens in section to zero

    # Consolidate Green Pixels Inside Target (based on original count):
    if original_num_green >= 9:
        for r in range(target_row_end - 3, target_row_end):
            for c in range(target_col_end - 3, target_col_end):
                output_grid[r, c] = 3
    elif 0 < original_num_green < 9:
        for c in range(target_col_end - original_num_green, target_col_end):
            output_grid[target_row_end - 1, c] = 3
    #else if original_num_green == 0 , the section is already reset.

    return output_grid