import copy

"""
Transforms an input grid by moving a single, specifically selected, non-zero cell horizontally.
1. Find all non-zero cells and determine the overall minimum and maximum column indices they occupy.
2. Identify all non-zero cells that are "horizontally isolated" (left and right neighbors are 0 or grid boundary).
3. From the isolated cells, select the one with the maximum row index. If there's a tie in row index, select the one with the maximum column index among the tied cells. This is the 'moving cell'.
4. Calculate the destination column for the moving cell by reflecting its original column across the center of the global non-zero column range (destination_col = min_col + max_col - original_col).
5. Create the output grid by copying the input, setting the original position of the moving cell to 0, and setting the calculated destination position (same row, new column) to the moving cell's original value.
"""


def find_non_zero_cells(grid):
    """Finds all cells with non-zero values."""
    non_zero_cells = []
    height = len(grid)
    if height == 0:
        return non_zero_cells
    width = len(grid[0])
    for r in range(height):
        for c in range(width):
            if grid[r][c] != 0:
                non_zero_cells.append({'r': r, 'c': c, 'v': grid[r][c]})
    return non_zero_cells

def get_global_column_range(non_zero_cells):
    """Calculates the min and max column index containing non-zero cells."""
    if not non_zero_cells:
        # Return default or signal no range if appropriate
        return None, None
    min_c = min(cell['c'] for cell in non_zero_cells)
    max_c = max(cell['c'] for cell in non_zero_cells)
    return min_c, max_c

def find_all_horizontally_isolated_cells(grid):
    """Finds all non-zero cells horizontally isolated by zeros or boundaries."""
    isolated_cells = []
    height = len(grid)
    if height == 0: return isolated_cells
    width = len(grid[0])
    if width == 0: return isolated_cells

    for r in range(height):
        for c in range(width):
            value = grid[r][c]
            if value != 0:
                # Check left neighbor
                is_left_bg = (c == 0) or (grid[r][c - 1] == 0)
                # Check right neighbor
                is_right_bg = (c == width - 1) or (grid[r][c + 1] == 0)

                if is_left_bg and is_right_bg:
                    isolated_cells.append({'r': r, 'c': c, 'v': value})
    return isolated_cells

def select_moving_cell(isolated_cells):
    """Selects the cell to move: max row index, then max col index."""
    if not isolated_cells:
        return None
    # Sort primarily by row (descending), then by column (descending)
    # The max element according to this key is the first element after sorting reversed
    # Alternatively, use max with a tuple key
    # Key: (row_index, column_index) -> max finds the largest tuple lexicographically
    moving_cell = max(isolated_cells, key=lambda cell: (cell['r'], cell['c']))
    return moving_cell


def transform(input_grid):
    # initialize output_grid as a deep copy to avoid modifying the input
    output_grid = copy.deepcopy(input_grid)
    height = len(output_grid)
    if height == 0:
        return output_grid
    width = len(output_grid[0])
    if width == 0:
        return output_grid

    # 1. Analyze Input Grid & 2. Determine Global Column Boundaries
    non_zero_cells = find_non_zero_cells(output_grid)
    if not non_zero_cells:
        return output_grid # No non-zero cells, nothing to move

    min_nz_col, max_nz_col = get_global_column_range(non_zero_cells)
    if min_nz_col is None: # Should not happen if non_zero_cells is not empty
         return output_grid

    # 3. Identify Candidate Cells
    isolated_cells = find_all_horizontally_isolated_cells(output_grid)
    if not isolated_cells:
         # No isolated cell found, return the original grid
        return output_grid

    # 4. Select the Moving Cell
    moving_cell = select_moving_cell(isolated_cells)
    if not moving_cell: # Should not happen if isolated_cells is not empty
         return output_grid

    r_move = moving_cell['r']
    c_move = moving_cell['c']
    v_move = moving_cell['v']

    # 5. Calculate the Destination Column
    # Reflect c_move across the center point (min_nz_col + max_nz_col) / 2
    # Formula: new_pos = min + max - old_pos
    c_new = min_nz_col + max_nz_col - c_move

    # Ensure destination column is within grid bounds
    if 0 <= c_new < width:
        # 6. Construct the Output Grid (modify the copy)
        # a. Clear the original position
        output_grid[r_move][c_move] = 0
        # b. Place the value at the new position
        output_grid[r_move][c_new] = v_move
    # else: If destination is out of bounds, the logic might be flawed or the
    #       problem guarantees this won't happen. Based on examples, it seems
    #       c_new will always be valid relative to min/max_nz_col, but checking
    #       against grid width adds robustness. For now, assume it's valid.

    # 7. Output
    return output_grid