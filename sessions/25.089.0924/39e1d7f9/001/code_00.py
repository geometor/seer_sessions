import numpy as np
import copy

"""
Transformation Rule:

1.  **Identify Grid Structure:** Determine the background color (0), the grid line color (the color forming full horizontal and vertical lines), and the dimensions of the cells defined by these lines. Calculate the dimensions (height `bh`, width `bw`) of the blocks contained within these cells (cell dimensions minus 1).
2.  **Find Maximum Content Color:** Scan the entire input grid for all solid rectangular blocks of size `bh` x `bw` that are neither the background color (0) nor the grid line color. Find the maximum numerical color value among these "content blocks". Store this as `max_color`. If no content blocks are found, the grid remains unchanged.
3.  **Process Cells:** Iterate through each cell defined by the grid lines.
4.  **Conditional Replacement:** For each cell:
    a. Check if the cell contains *any* content blocks.
    b. If it does, find all background blocks (solid blocks of color 0 with dimensions `bh` x `bw`) within that same cell.
    c. Replace each found background block with a solid block of `max_color` of the same dimensions (`bh` x `bw`).
    d. If the cell does not contain any content blocks, leave it unchanged.
5.  **Output:** The final grid includes the original grid lines, original content blocks, and the newly colored blocks where background blocks were replaced.
"""

def find_grid_params(grid):
    """
    Finds the grid line color, row/col spacing, and block dimensions.

    Args:
        grid: The input numpy array.

    Returns:
        A tuple (grid_color, row_indices, col_indices, block_h, block_w)
        or None if no grid structure is found.
    """
    h, w = grid.shape
    grid_color = -1
    row_indices = []
    col_indices = []

    # Find horizontal grid lines and their color
    for r in range(h):
        unique_colors = np.unique(grid[r, :])
        if len(unique_colors) == 1 and unique_colors[0] != 0:
            if grid_color == -1:
                grid_color = unique_colors[0]
            if unique_colors[0] == grid_color:
                 row_indices.append(r)

    # Find vertical grid lines (must match horizontal grid color)
    if grid_color != -1:
        for c in range(w):
             unique_colors = np.unique(grid[:, c])
             if len(unique_colors) == 1 and unique_colors[0] == grid_color:
                 col_indices.append(c)

    if not row_indices or not col_indices or grid_color == -1:
        # Handle cases where grid might be just a single cell or malformed
         # Try finding grid color by checking if any non-zero color appears in > 50% of rows/cols
        potential_colors = {}
        for c in range(1,10):
             potential_colors[c] = {'row':0, 'col':0}

        for r in range(h):
             unique_colors, counts = np.unique(grid[r, :], return_counts=True)
             for color, count in zip(unique_colors, counts):
                 if color != 0 and count == w:
                     potential_colors[color]['row'] += 1
        for c in range(w):
            unique_colors, counts = np.unique(grid[:, c], return_counts=True)
            for color, count in zip(unique_colors, counts):
                if color != 0 and count == h:
                    potential_colors[color]['col'] += 1

        best_color = -1
        for color, counts in potential_colors.items():
            if counts['row'] > h // 2 or counts['col'] > w // 2:
                 grid_color = color
                 break

        if grid_color != -1:
            row_indices = [r for r in range(h) if np.all(grid[r, :] == grid_color)]
            col_indices = [c for c in range(w) if np.all(grid[:, c] == grid_color)]

    if not row_indices or not col_indices or grid_color == -1:
         print("Warning: Could not determine grid structure definitively.")
         # Default assumption if no grid lines: entire grid is one cell
         return grid_color, [-1, h], [-1, w], h, w # Treat borders as implicit grid lines

    # Calculate spacing and block dimensions
    # Assume uniform spacing
    row_spacing = np.diff(row_indices)
    col_spacing = np.diff(col_indices)

    if len(row_spacing) > 0 and np.all(row_spacing == row_spacing[0]):
        block_h = row_spacing[0] - 1
    elif len(row_indices) > 0: # Only one line or inconsistent spacing, guess from first gap
        block_h = row_indices[0] if row_indices[0] > 0 else h - row_indices[-1] -1 if row_indices[-1] < h - 1 else 1
        if len(row_indices) > 1 : # try avg
             block_h = int(round(np.mean(row_spacing) -1 )) if len(row_spacing)>0 else block_h
    else: # No horizontal lines detected other than maybe borders
        block_h = h

    if len(col_spacing) > 0 and np.all(col_spacing == col_spacing[0]):
        block_w = col_spacing[0] - 1
    elif len(col_indices) > 0: # Only one line or inconsistent spacing, guess from first gap
        block_w = col_indices[0] if col_indices[0] > 0 else w - col_indices[-1] -1 if col_indices[-1] < w - 1 else 1
        if len(col_indices) > 1:
             block_w = int(round(np.mean(col_spacing)-1)) if len(col_spacing) > 0 else block_w
    else: # No vertical lines detected other than maybe borders
        block_w = w

    # Add implicit borders for cell iteration
    extended_rows = sorted(list(set([-1] + row_indices + [h])))
    extended_cols = sorted(list(set([-1] + col_indices + [w])))


    # Ensure block dimensions are at least 1
    block_h = max(1, block_h)
    block_w = max(1, block_w)


    return grid_color, extended_rows, extended_cols, block_h, block_w

def find_max_content_color(grid, grid_color, block_h, block_w, row_indices, col_indices):
    """
    Finds the maximum color value among content blocks.

    Args:
        grid: The input numpy array.
        grid_color: The color of the grid lines.
        block_h: Height of the blocks within cells.
        block_w: Width of the blocks within cells.
        row_indices: List of row indices of horizontal grid lines (including borders -1, h).
        col_indices: List of col indices of vertical grid lines (including borders -1, w).

    Returns:
        The maximum content color found, or -1 if none exist.
    """
    max_color = -1
    h, w = grid.shape

    for r_idx in range(len(row_indices) - 1):
        for c_idx in range(len(col_indices) - 1):
            cell_r_start = row_indices[r_idx] + 1
            cell_r_end = row_indices[r_idx + 1]
            cell_c_start = col_indices[c_idx] + 1
            cell_c_end = col_indices[c_idx + 1]

            # Iterate through potential block top-left corners within the cell
            for r in range(cell_r_start, cell_r_end - block_h + 1):
                 for c in range(cell_c_start, cell_c_end - block_w + 1):
                    block = grid[r:r + block_h, c:c + block_w]
                    if block.shape != (block_h, block_w): continue # Skip incomplete blocks at edges

                    unique_colors = np.unique(block)
                    # Check if it's a solid block, not background, and not grid color
                    if len(unique_colors) == 1:
                         color = unique_colors[0]
                         if color != 0 and color != grid_color:
                             max_color = max(max_color, color)
                    # # Alternative check: Does it contain *any* non-background, non-grid color?
                    # elif np.any((block != 0) & (block != grid_color)):
                    #      content_colors = block[(block != 0) & (block != grid_color)]
                    #      if len(content_colors)>0:
                    #           max_color = max(max_color, np.max(content_colors))


    return max_color


def transform(input_grid):
    """
    Transforms the input grid by finding cells containing content blocks
    and replacing background blocks within those cells with the maximum
    content color found anywhere in the grid.
    """
    output_grid = np.copy(input_grid)
    h, w = input_grid.shape

    # 1. Identify Grid Parameters
    grid_params = find_grid_params(input_grid)
    if grid_params is None:
        print("Could not find grid parameters.")
        return output_grid # Return copy if grid structure unclear

    grid_color, row_indices, col_indices, block_h, block_w = grid_params
    
    if block_h <= 0 or block_w <= 0:
         print(f"Warning: Invalid block dimensions calculated ({block_h}x{block_w}). Aborting.")
         return output_grid

    # 2. Find Maximum Content Color
    max_color = find_max_content_color(input_grid, grid_color, block_h, block_w, row_indices, col_indices)

    # If no content blocks are found, no transformation is needed
    if max_color == -1:
        return output_grid

    # 3. & 4. Process Each Cell and Apply Transformation
    for r_idx in range(len(row_indices) - 1):
        for c_idx in range(len(col_indices) - 1):
            # Define cell boundaries (excluding grid lines)
            cell_r_start = row_indices[r_idx] + 1
            cell_r_end = row_indices[r_idx + 1]
            cell_c_start = col_indices[c_idx] + 1
            cell_c_end = col_indices[c_idx + 1]

            # Check if cell is valid
            if cell_r_start >= cell_r_end or cell_c_start >= cell_c_end:
                continue

            cell_content = input_grid[cell_r_start:cell_r_end, cell_c_start:cell_c_end]

            # Check if this cell contains any content block
            cell_has_content = False
            # Iterate through potential blocks within the cell to check for content
            for r_cell in range(0, cell_content.shape[0] - block_h + 1):
                 for c_cell in range(0, cell_content.shape[1] - block_w + 1):
                      block = cell_content[r_cell:r_cell + block_h, c_cell:c_cell + block_w]
                      if block.shape != (block_h, block_w): continue
                      unique_colors = np.unique(block)
                      if len(unique_colors) == 1:
                           color = unique_colors[0]
                           if color != 0 and color != grid_color:
                                cell_has_content = True
                                break # Found content, no need to check further blocks in this cell
                      # # Alternative: Check for *any* content pixel
                      # elif np.any((block != 0) & (block != grid_color)):
                      #       cell_has_content = True
                      #       break
                 if cell_has_content:
                      break


            # If cell contains content, replace background blocks within it
            if cell_has_content:
                # Iterate through potential block top-left corners in the original grid coordinates
                for r in range(cell_r_start, cell_r_end - block_h + 1, 1): # Step by 1 initially, should refine later if blocks are spaced
                    for c in range(cell_c_start, cell_c_end - block_w + 1, 1):
                        # Check if the block at this position in the *original* grid is a background block
                        original_block = input_grid[r:r + block_h, c:c + block_w]

                        if original_block.shape == (block_h, block_w) and np.all(original_block == 0):
                             # Replace this block in the output grid
                             output_grid[r:r + block_h, c:c + block_w] = max_color

    # 5. Return the modified grid
    return output_grid