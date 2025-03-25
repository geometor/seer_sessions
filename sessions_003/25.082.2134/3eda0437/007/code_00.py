"""
1. Iterate through each row of the input grid.
2. For each row, scan for contiguous regions of 0-colored pixels (left-to-right).
3. For each 0-colored pixel encountered:
    - Check if it's part of an already identified region.
    - If not, start a new "region" and mark its starting index.
    - Continue scanning to the right, extending the region as long as 0s are encountered.
    - Search for non-zero boundary pixels to the left and right of the region.
        - If a non-zero pixel is found on the left, set region.left_bound to its index.
        - If a non-zero pixel is found on the right, set region.right_bound to its index.
        - If we reach the left edge without a boundary, keep region.left_bound = -1.
        - If we reach the right edge without a boundary, keep region.right_bound = -1.
4. After scanning a region, check if it's bounded (left_bound != -1 and right_bound != -1).
5. If the region is bounded, fill it with magenta (color 6) from region.left_bound + 1 to region.right_bound (exclusive).
6. If a region touches the edge, and there is no bounding pixel on that edge, it is not filled.
7. Proceed until the end of the row.
8. Repeat for all rows.
"""

import numpy as np

def find_region_bounds(grid, row, start_col):
    """
    Finds the left and right bounds of a contiguous region of 0s.
    """
    rows, cols = grid.shape
    left_bound = -1
    right_bound = -1

    # Find left bound
    for c in range(start_col - 1, -1, -1):
        if grid[row, c] != 0:
            left_bound = c
            break

    # Extend region to the right and find right bound
    end_col = start_col
    for c in range(start_col, cols):
        if grid[row, c] == 0:
            end_col = c
        else:
            right_bound = c
            break

    return left_bound, right_bound, end_col


def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    grid = np.array(input_grid)
    output_grid = np.copy(grid)
    rows, cols = grid.shape

    # iterate through rows
    for r in range(rows):
        c = 0
        while c < cols:
            # find 0 regions
            if grid[r, c] == 0:
                # find bounds
                left_bound, right_bound, end_col = find_region_bounds(grid, r, c)

                # fill if bounded
                if left_bound != -1 and right_bound != -1:
                    for k in range(left_bound + 1, right_bound):
                        output_grid[r, k] = 6
                c = end_col + 1  # Skip the processed region.

            else:
                c += 1

    return output_grid.tolist()