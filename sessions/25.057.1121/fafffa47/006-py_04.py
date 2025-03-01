"""
1.  **Identify Objects:** Find two primary objects within the input grid: one starting from the top-left corner, and one starting from the bottom-right corner. Objects are defined as contiguous regions of non-zero pixels.
2.  **Determine Output Grid Size:**  If either object is not found, the output is all zeros. Otherwise, calculate the diagonal distance between the closest corners of the objects identified in Step 1. The height and width of output will be calculated from that distance.
3. **Draw Diagonal:** Create the output grid, then fill the diagonal with red (color 2). The direction of the line depends on where the object is, i.e. top-left object is bottom-right corner of output.
4.  **Fill Remaining Cells:** Keep all cells not part of the diagonal filled with background color, which is white (0).
"""

import numpy as np

def find_top_left_object(grid):
    """Finds the top-left non-zero pixel and its color."""
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0:
                return (r, c), grid[r, c]
    return None, None

def get_object_bounds(grid, start_row, start_col, color):
    """Gets the bounding box of a contiguous object."""
    rows, cols = grid.shape
    min_row, max_row = rows, -1
    min_col, max_col = cols, -1

    visited = set()
    stack = [(start_row, start_col)]

    while stack:
        r, c = stack.pop()
        if (r, c) in visited:
            continue
        visited.add((r, c))

        if 0 <= r < rows and 0 <= c < cols and grid[r, c] == color:
            min_row = min(min_row, r)
            max_row = max(max_row, r)
            min_col = min(min_col, c)
            max_col = max(max_col, c)

            # Add adjacent cells to the stack
            stack.append((r + 1, c))
            stack.append((r - 1, c))
            stack.append((r, c + 1))
            stack.append((r, c - 1))
    return min_row, max_row, min_col, max_col

def invert_and_flip_grid(grid):
    """Inverts (bottom-to-top) and flips (right-to-left) a grid."""
    return np.flipud(np.fliplr(grid))

def transform(input_grid):
    """Transforms the input grid according to the diagonal rule."""
    # Find the top-left object
    tl_coord, tl_color = find_top_left_object(input_grid)
    if tl_coord is None:
        return np.zeros_like(input_grid)  # Return all zeros if no top-left object
    tl_min_row, tl_max_row, tl_min_col, tl_max_col = get_object_bounds(input_grid, tl_coord[0], tl_coord[1], tl_color)

    # Find the bottom-right object
    inverted_grid = invert_and_flip_grid(input_grid)
    br_coord, br_color = find_top_left_object(inverted_grid)
    if br_coord is None:
        return np.zeros_like(input_grid) # Return all zeros if no bottom right object

    rows, cols = input_grid.shape
    br_min_row, br_max_row, br_min_col, br_max_col = get_object_bounds(inverted_grid, br_coord[0], br_coord[1], br_color)

     #translate back to original coordinates
    br_start_row = rows - 1 - br_max_row
    br_start_col = cols - 1 - br_max_col

    # Determine output grid size based on the diagonal
    output_height = max(tl_max_row, br_start_row) - min(tl_min_row, br_start_row) + 1
    output_width = max(tl_max_col, br_start_col) - min(tl_min_col, br_start_col) + 1

    #adjust output to connect corners
    output_height = br_start_row + 1
    output_width = br_start_col + 1
    if br_start_col < tl_max_col:
        output_width = tl_max_col + 1
    if br_start_row < tl_max_row:
        output_height = tl_max_row + 1
    
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Draw the diagonal line
    # find closest corners
    if abs(tl_min_row - br_start_row) > abs(tl_max_row - br_start_row):
      start_row = tl_max_row
    else:
      start_row = tl_min_row

    if abs(tl_min_col - br_start_col) > abs(tl_max_col - br_start_col):
      start_col = tl_max_col
    else:
      start_col = tl_min_col

    end_row = br_start_row
    end_col = br_start_col

    #normalize to origin
    start_row_norm = start_row
    start_col_norm = start_col
    if br_start_row > start_row:
        end_row = br_start_row - start_row_norm
        start_row_norm = 0
    else:
        start_row_norm = start_row - br_start_row
        end_row = 0

    if br_start_col > start_col:
        end_col = br_start_col - start_col_norm
        start_col_norm = 0
    else:
        start_col_norm = start_col - br_start_col
        end_col = 0

    row = start_row_norm
    col = start_col_norm
    while row <= end_row and col <= end_col:
        output_grid[row, col] = 2
        if(row < end_row):
            row += 1
        if(col < end_col):
            col += 1

    return output_grid