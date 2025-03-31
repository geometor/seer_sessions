import numpy as np
import copy

"""
Transformation Rule:

1.  **Identify Grid Structure:**
    *   Find the background color (assumed to be 0).
    *   Find the single color forming full horizontal and vertical grid lines (grid_color).
    *   Determine the row and column indices of these grid lines.
    *   Calculate the height (block_h) and width (block_w) of the rectangular blocks contained within the cells defined by the grid lines (typically cell dimension - 1).

2.  **Find Global Maximum Content Color:**
    *   Scan the entire input grid.
    *   Identify all solid rectangular blocks of size block_h x block_w that are neither the background color (0) nor the grid_color. These are "content blocks".
    *   Find the maximum numerical color value among all these content blocks across the entire grid. Store this as max_color.
    *   If no content blocks are found anywhere, return the input grid unchanged.

3.  **Process Cells and Apply Transformation:**
    *   Create a copy of the input grid to serve as the output grid.
    *   Iterate through each cell defined by the grid lines.
    *   **For each cell:**
        *   Check if the cell contains at least one solid content block (size block_h x block_w, color not 0 or grid_color).
        *   **If the cell contains content:**
            *   Iterate through all possible block positions (top-left corner r, c) within that specific cell.
            *   If the block at input_grid[r:r+block_h, c:c+block_w] consists entirely of the background color (0):
                *   Fill the corresponding area in the output_grid (output_grid[r:r+block_h, c:c+block_w]) with the globally determined max_color.
        *   **If the cell does not contain content:** Leave the corresponding area in the output grid unchanged from the input.

4.  **Return Output:** Return the modified output grid.
"""

def find_grid_params(grid):
    """
    Finds the grid line color, row/col indices, and block dimensions.

    Args:
        grid: The input numpy array.

    Returns:
        A tuple (grid_color, extended_rows, extended_cols, block_h, block_w)
        or None if no valid grid structure is found.
        extended_rows/cols include implicit borders -1 and h/w.
    """
    h, w = grid.shape
    grid_color = -1
    
    # Find potential grid colors by looking for uniform rows/cols (excluding background 0)
    potential_grid_colors = {}
    for r in range(h):
        unique_colors, counts = np.unique(grid[r, :], return_counts=True)
        # Check if the row is uniform and not background
        if len(unique_colors) == 1 and unique_colors[0] != 0 and counts[0] == w:
            color = unique_colors[0]
            potential_grid_colors[color] = potential_grid_colors.get(color, {'rows': 0, 'cols': 0})
            potential_grid_colors[color]['rows'] += 1
            
    for c in range(w):
        unique_colors, counts = np.unique(grid[:, c], return_counts=True)
         # Check if the col is uniform and not background
        if len(unique_colors) == 1 and unique_colors[0] != 0 and counts[0] == h:
            color = unique_colors[0]
            potential_grid_colors[color] = potential_grid_colors.get(color, {'rows': 0, 'cols': 0})
            potential_grid_colors[color]['cols'] += 1

    # The grid color must form both rows and columns
    valid_grid_colors = [color for color, counts in potential_grid_colors.items() if counts['rows'] > 0 and counts['cols'] > 0]

    if not valid_grid_colors:
        # Handle edge case: grid might have no lines (single cell)
        # Or lines only in one direction (less common in ARC, treat as single cell for now)
        # Need a fallback - perhaps check if only one non-zero color exists?
        non_zero_colors = np.unique(grid[grid != 0])
        if len(non_zero_colors) == 1:
             # Assume this single color *might* be the grid color if it forms any lines
             # But more likely, it's content in a gridless setup.
             # Let's assume gridless means the whole thing is one block/cell
             # We still need a grid_color for checks later, maybe pick -1 or a dummy?
             # Let's return None to indicate no standard grid structure found.
             return None
        else:
            # Cannot determine grid structure reliably
             return None

    # Usually there's only one valid grid color. If multiple, pick the most frequent line color.
    grid_color = max(valid_grid_colors, key=lambda c: potential_grid_colors[c]['rows'] + potential_grid_colors[c]['cols'])

    # Find actual grid lines using the determined grid_color
    row_indices = [r for r in range(h) if np.all(grid[r, :] == grid_color)]
    col_indices = [c for c in range(w) if np.all(grid[:, c] == grid_color)]

    # If somehow we picked a color but it doesn't form full lines (shouldn't happen with above logic), error out
    if not row_indices or not col_indices:
        return None

    # Add implicit borders for cell iteration
    extended_rows = sorted(list(set([-1] + row_indices + [h])))
    extended_cols = sorted(list(set([-1] + col_indices + [w])))

    # Calculate block dimensions based on the *difference* between consecutive grid lines
    # Ensure there are at least two lines (including implicit borders) to measure a gap
    block_h = 0
    if len(extended_rows) > 1:
         # Calculate differences between all consecutive lines and check consistency
         row_diffs = np.diff(extended_rows)
         if len(row_diffs)>0:
            block_h = row_diffs[0] - 1 # Use first gap, assume uniformity

    block_w = 0
    if len(extended_cols) > 1:
        col_diffs = np.diff(extended_cols)
        if len(col_diffs)>0:
            block_w = col_diffs[0] - 1 # Use first gap, assume uniformity

    # Handle grids that might just be lines (block dim 0) or malformed
    if block_h <= 0 or block_w <= 0:
        # Try deriving from grid size if only borders were found
        if block_h <= 0 and len(row_indices) == 0: block_h = h
        if block_w <= 0 and len(col_indices) == 0: block_w = w
        # If still zero or negative, grid structure is invalid
        if block_h <= 0 or block_w <= 0:
            return None # Invalid block dimensions derived

    return grid_color, extended_rows, extended_cols, block_h, block_w


def find_max_content_color(grid, grid_color, block_h, block_w):
    """
    Finds the maximum color value among solid content blocks anywhere in the grid.

    Args:
        grid: The input numpy array.
        grid_color: The color of the grid lines.
        block_h: Height of the blocks within cells.
        block_w: Width of the blocks within cells.

    Returns:
        The maximum content color found, or -1 if none exist.
    """
    max_color = -1
    h, w = grid.shape

    # Iterate through all possible top-left corners for a block
    for r in range(h - block_h + 1):
        for c in range(w - block_w + 1):
            block = grid[r:r + block_h, c:c + block_w]

            # Check if it's a solid block
            unique_colors = np.unique(block)
            if len(unique_colors) == 1:
                color = unique_colors[0]
                # Check if it's a content block (not background, not grid line)
                if color != 0 and color != grid_color:
                    max_color = max(max_color, color)
    return max_color

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    h, w = input_grid.shape

    # 1. Identify Grid Parameters
    grid_params = find_grid_params(input_grid)
    if grid_params is None:
        # print("Failed to determine grid parameters. Returning input.")
        # This might happen for grids without the expected structure.
        # Depending on task requirements, might need more robust fallback.
        # For this specific task structure, returning the input seems safe if params fail.
        return output_grid
    grid_color, row_indices, col_indices, block_h, block_w = grid_params

    # Basic sanity check for block dimensions derived
    if block_h <= 0 or block_w <= 0 or block_h > h or block_w > w :
         # print(f"Warning: Invalid block dimensions calculated ({block_h}x{block_w}). Returning input.")
         return output_grid

    # 2. Find Maximum Content Color globally
    max_color = find_max_content_color(input_grid, grid_color, block_h, block_w)

    # If no content blocks are found anywhere, no transformation is needed
    if max_color == -1:
        # print("No content blocks found. Returning input.")
        return output_grid

    # 3. & 4. Process Each Cell and Apply Transformation
    # Iterate through cells defined by grid lines (using extended indices)
    for r_idx in range(len(row_indices) - 1):
        for c_idx in range(len(col_indices) - 1):
            # Define cell boundaries (exclusive of grid lines)
            cell_r_start = row_indices[r_idx] + 1
            cell_r_end = row_indices[r_idx + 1]
            cell_c_start = col_indices[c_idx] + 1
            cell_c_end = col_indices[c_idx + 1]

            # Ensure cell dimensions are valid
            if cell_r_start >= cell_r_end or cell_c_start >= cell_c_end:
                continue
                
            # Check if this cell contains *any* solid content block
            cell_has_content = False
            # Iterate through potential block top-left corners *within this cell*
            for r_cell in range(cell_r_start, cell_r_end - block_h + 1):
                # Check bounds before slicing
                if r_cell + block_h > cell_r_end: continue
                for c_cell in range(cell_c_start, cell_c_end - block_w + 1):
                     # Check bounds before slicing
                    if c_cell + block_w > cell_c_end: continue

                    block = input_grid[r_cell:r_cell + block_h, c_cell:c_cell + block_w]

                    # Should already be correct size, but double check might be good
                    if block.shape != (block_h, block_w): continue

                    unique_colors = np.unique(block)
                    if len(unique_colors) == 1:
                        color = unique_colors[0]
                        # Is it a content block?
                        if color != 0 and color != grid_color:
                            cell_has_content = True
                            break # Found content in this cell, stop searching the cell
                if cell_has_content:
                    break

            # If this cell had content, iterate again to find and replace background blocks
            if cell_has_content:
                # Iterate through potential block top-left corners *within this cell* again
                for r_cell in range(cell_r_start, cell_r_end - block_h + 1):
                     # Check bounds before slicing
                    if r_cell + block_h > cell_r_end: continue
                    for c_cell in range(cell_c_start, cell_c_end - block_w + 1):
                        # Check bounds before slicing
                        if c_cell + block_w > cell_c_end: continue

                        # Check if the block at this position in the *original* grid is a background block
                        # Need to use r_cell, c_cell which are already global coordinates
                        original_block = input_grid[r_cell:r_cell + block_h, c_cell:c_cell + block_w]

                        if original_block.shape == (block_h, block_w) and np.all(original_block == 0):
                            # Replace this block in the output grid with the global max_color
                            output_grid[r_cell:r_cell + block_h, c_cell:c_cell + block_w] = max_color

    # 5. Return the modified grid
    return output_grid