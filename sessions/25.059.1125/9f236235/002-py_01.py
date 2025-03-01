"""
1. **Identify Background Grid:** Find the lines of pixels that divide the input
   grid into equal size rectangular subgrids. White (0) pixels may form a
   background. Other background lines will all be of the same color and one
   pixel wide.

2. **Identify Subgrids:** the background grid creates equally sized rectangular
   subgrids.

3. **Locate Key Colors:** Within each sub-grid, locate the color of the pixel
   in the upper-left corner.

4. **Construct Output Grid:** Create a new grid where each cell corresponds to a
   subgrid in the original input. The dimensions of output are based on number
   of subgrids in each dimension.

5.  **Populate Output Grid** Populate each cell of the output grid with the
    "key color" of the corresponding subgrid in the input grid (found in step
    3).
"""

import numpy as np

def find_grid_lines(grid):
    rows, cols = grid.shape
    horizontal_lines = []
    vertical_lines = []

    # Find horizontal lines
    for r in range(rows):
        first_pixel = grid[r, 0]
        all_same = True
        for c in range(1, cols):
            if grid[r, c] != first_pixel:
                all_same = False
                break
        if all_same:
            horizontal_lines.append((r, first_pixel))

    # Find vertical lines
    for c in range(cols):
        first_pixel = grid[0, c]
        all_same = True
        for r in range(1, rows):
            if grid[r, c] != first_pixel:
                all_same = False
                break
        if all_same:
            vertical_lines.append((c, first_pixel))

    return horizontal_lines, vertical_lines

def find_subgrids(grid, horizontal_lines, vertical_lines):
    rows, cols = grid.shape
    subgrids = []

    # Filter out lines that aren't part of the main dividing structure.  Look for repeating pattern.
    horizontal_colors = [color for _, color in horizontal_lines]
    vertical_colors = [color for _, color in vertical_lines]

    # Find most common color, and assume this is the background grid color
    horizontal_counts = np.bincount(horizontal_colors)
    vertical_counts = np.bincount(vertical_colors)

    h_grid_color = np.argmax(horizontal_counts)
    v_grid_color = np.argmax(vertical_counts)

    h_lines = [row for row, color in horizontal_lines if color == h_grid_color]
    v_lines = [col for col, color in vertical_lines if color == v_grid_color]

    # remove duplicates, which are not part of a grid structure.
    h_lines = sorted(list(set(h_lines)))
    v_lines = sorted(list(set(v_lines)))
    
    # calculate distances, look for repeating pattern of grid
    h_diffs = np.diff(h_lines)
    v_diffs = np.diff(v_lines)
    
    # Use most frequent distance.
    if (len(h_diffs) > 0):
       h_grid_size = np.bincount(h_diffs).argmax()
    else:
       h_grid_size = rows # default if no horizontal lines
       h_lines = [0,rows] # add top and bottom

    if (len(v_diffs) > 0):
       v_grid_size = np.bincount(v_diffs).argmax()
    else:
        v_grid_size = cols
        v_lines = [0, cols]

    # ensure includes first and last row/col
    if 0 not in h_lines:
        h_lines.insert(0,0)
    if rows not in h_lines:
        h_lines.append(rows)
    if 0 not in v_lines:
        v_lines.insert(0,0)
    if cols not in v_lines:
        v_lines.append(cols)

    # define subgrids based on final h_lines, v_lines
    for i in range(len(h_lines) - 1):
        for j in range(len(v_lines) - 1):
            subgrids.append(((h_lines[i], v_lines[j]), (h_lines[i+1], v_lines[j+1]))) # (top-left), (bottom-right)

    return subgrids, h_grid_size, v_grid_size


def transform(input_grid):
    grid = np.array(input_grid)
    rows, cols = grid.shape

    # Find horizontal and vertical lines
    horizontal_lines, vertical_lines = find_grid_lines(grid)

    # Determine subgrids
    subgrids, h_grid_size, v_grid_size = find_subgrids(grid, horizontal_lines, vertical_lines)
   
    # calculate output grid dimensions
    output_rows = (rows-1) // h_grid_size
    output_cols = (cols-1) // v_grid_size

    # handle case where no subgrids detected
    if output_rows == 0: output_rows = 1
    if output_cols == 0: output_cols = 1
    if h_grid_size == 0: h_grid_size = rows
    if v_grid_size == 0: v_grid_size = cols

    # Initialize output grid
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Populate output grid
    for i in range(len(subgrids)):
       
        (r_start, c_start), (r_end, c_end) = subgrids[i]
        
        # identify key color
        key_color = grid[r_start, c_start]

        # determine output grid location based on subgrid
        out_row = i // output_cols
        out_col = i % output_cols
        
        output_grid[out_row, out_col] = key_color

    return output_grid.tolist()