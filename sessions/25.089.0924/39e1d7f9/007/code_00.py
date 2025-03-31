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
            *   Iterate through all possible block positions (top-left corner r, c) within that specific cell's boundaries.
            *   If the block at input_grid[r:r+block_h, c:c+block_w] consists entirely of the background color (0):
                *   Fill the corresponding area in the output_grid (output_grid[r:r+block_h, c:c+block_w]) with the globally determined max_color.
        *   **If the cell does not contain content:** Leave the corresponding area in the output grid unchanged from the input.

4.  **Return Output:** Return the modified output grid.
"""

# Helper function to find grid parameters
def find_grid_params(grid):
    """
    Finds the grid line color, row/col indices including implicit borders, and block dimensions.

    Args:
        grid: The input numpy array.

    Returns:
        A tuple (grid_color, extended_rows, extended_cols, block_h, block_w)
        or None if no valid grid structure is found.
        extended_rows/cols include implicit borders -1 and h/w.
    """
    h, w = grid.shape
    grid_color = -1
    
    potential_grid_colors = {}
    # Count uniform non-background rows
    for r in range(h):
        unique_colors, counts = np.unique(grid[r, :], return_counts=True)
        # Check if the row is uniform and not background
        if len(unique_colors) == 1 and unique_colors[0] != 0 and counts[0] == w:
            color = unique_colors[0]
            potential_grid_colors[color] = potential_grid_colors.get(color, {'rows': 0, 'cols': 0})
            potential_grid_colors[color]['rows'] += 1
            
    # Count uniform non-background columns
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
        # No valid grid structure with lines found
        return None 

    # Select grid color (most frequent line color if multiple valid)
    grid_color = max(valid_grid_colors, key=lambda c: potential_grid_colors[c]['rows'] + potential_grid_colors[c]['cols'])

    # Get indices of actual grid lines using the determined grid_color
    row_indices = [r for r in range(h) if np.all(grid[r, :] == grid_color)]
    col_indices = [c for c in range(w) if np.all(grid[:, c] == grid_color)]

    # If somehow we picked a color but it doesn't form full lines (shouldn't happen with above logic), error out
    if not row_indices or not col_indices:
        return None

    # Add implicit borders (-1 and h/w) for easier cell iteration
    extended_rows = sorted(list(set([-1] + row_indices + [h])))
    extended_cols = sorted(list(set([-1] + col_indices + [w])))

    # Calculate block dimensions based on the *difference* between consecutive grid lines
    # Assume uniform spacing based on the first gap found
    block_h = 0
    if len(extended_rows) > 1:
         # Calculate differences between all consecutive lines
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
        return None # Invalid block dimensions derived

    return grid_color, extended_rows, extended_cols, block_h, block_w


# Helper function to find the maximum color of content blocks
def find_max_content_color(grid, grid_color, block_h, block_w):
    """
    Finds the maximum color value among solid content blocks anywhere in the grid.

    Args:
        grid: The input numpy array.
        grid_color: The color of the grid lines.
        block_h: Height of the blocks within cells.
        block_w: Width of the blocks within cells.

    Returns:
        The maximum content color found (int), or -1 if none exist.
    """
    max_color = -1
    h, w = grid.shape

    # Iterate through all possible top-left corners for a block
    for r in range(h - block_h + 1):
        for c in range(w - block_w + 1):
            # Extract potential block slice
            block = grid[r:r + block_h, c:c + block_w]
            
            # Check if it's a solid block (all pixels the same color)
            unique_colors = np.unique(block)
            if len(unique_colors) == 1:
                color = unique_colors[0]
                # Check if it's a content block (not background 0, not grid line color)
                if color != 0 and color != grid_color:
                    # Update max_color if this block's color is higher
                    max_color = max(max_color, color)
                    
    return max_color

# Helper function to check if a cell contains any content block
def cell_contains_content(grid, grid_color, cell_r_start, cell_r_end, cell_c_start, cell_c_end, block_h, block_w):
    """
    Checks if the specified cell region in the grid contains at least one solid content block.

    Args:
        grid: The input numpy array.
        grid_color: The color of the grid lines.
        cell_r_start, cell_r_end: Row boundaries of the cell (exclusive of grid lines).
        cell_c_start, cell_c_end: Column boundaries of the cell (exclusive of grid lines).
        block_h, block_w: Dimensions of the blocks to check for.

    Returns:
        True if at least one content block is found within the cell, False otherwise.
    """
    # Iterate through potential block top-left corners *within the cell's boundaries*
    for r in range(cell_r_start, cell_r_end - block_h + 1):
        # Boundary check (upper row boundary)
        if r + block_h > cell_r_end: continue 
        for c in range(cell_c_start, cell_c_end - block_w + 1):
            # Boundary check (right column boundary)
            if c + block_w > cell_c_end: continue 
                
            # Extract block from the grid using global coordinates r, c
            block = grid[r:r + block_h, c:c + block_w]
            
            # Ensure block shape is correct (mostly redundant due to loop limits, but safe)
            if block.shape != (block_h, block_w): continue 

            # Check if it's a solid block
            unique_colors = np.unique(block)
            if len(unique_colors) == 1:
                color = unique_colors[0]
                # Is it a content block (not background 0, not grid color)?
                if color != 0 and color != grid_color:
                    return True # Found content, no need to search further in this cell
                    
    return False # No content blocks were found in this cell after checking all positions

# Main transformation function
def transform(input_grid):
    """
    Applies the transformation rule: Finds the global max content color, then for each
    grid cell that contains *any* content block, replaces all background blocks (color 0)
    within that cell with the global max content color.
    """
    h, w = input_grid.shape
    
    # 1. Identify Grid Parameters
    # Find grid color, line locations, and block dimensions
    grid_params = find_grid_params(input_grid)
    if grid_params is None:
        # If grid structure (lines, block size) isn't found or is invalid, return input copy
        return np.copy(input_grid) 
        
    grid_color, row_indices, col_indices, block_h, block_w = grid_params

    # Final check on derived block dimensions against grid size
    if block_h <= 0 or block_w <= 0 or block_h > h or block_w > w :
         return np.copy(input_grid)

    # 2. Find Global Maximum Content Color
    # Scan the entire grid for the highest color value present in any content block
    max_color = find_max_content_color(input_grid, grid_color, block_h, block_w)

    # If no content blocks were found anywhere in the grid, return the original grid copy
    if max_color == -1:
        return np.copy(input_grid)

    # 3. Process Cells and Apply Transformation
    # Create the output grid as a copy of the input to modify
    output_grid = np.copy(input_grid) 

    # Iterate through each cell defined by the grid line indices
    for r_idx in range(len(row_indices) - 1):
        for c_idx in range(len(col_indices) - 1):
            # Define the boundaries of the current cell (exclusive of the grid lines)
            # Coordinates are global within the input_grid
            cell_r_start = row_indices[r_idx] + 1
            cell_r_end = row_indices[r_idx + 1]
            cell_c_start = col_indices[c_idx] + 1
            cell_c_end = col_indices[c_idx + 1]

            # Skip processing if the calculated cell dimensions are invalid (e.g., adjacent grid lines)
            if cell_r_start >= cell_r_end or cell_c_start >= cell_c_end:
                continue
                
            # Check if the current cell contains at least one content block
            has_content = cell_contains_content(input_grid, grid_color, 
                                                 cell_r_start, cell_r_end, 
                                                 cell_c_start, cell_c_end, 
                                                 block_h, block_w)

            # If the cell contains content, proceed to replace its background blocks
            if has_content:
                # Iterate through all possible block top-left corners (r, c) *within this cell*
                for r in range(cell_r_start, cell_r_end - block_h + 1):
                    # Boundary check (should not exceed cell_r_end)
                    if r + block_h > cell_r_end: continue
                    for c in range(cell_c_start, cell_c_end - block_w + 1):
                        # Boundary check (should not exceed cell_c_end)
                        if c + block_w > cell_c_end: continue
                        
                        # Check if the block at this position (r, c) in the *original* input grid is a background block
                        original_block = input_grid[r:r + block_h, c:c + block_w]

                        # Verify shape and check if all pixels in the block are the background color (0)
                        if original_block.shape == (block_h, block_w) and np.all(original_block == 0):
                            # If it's a background block, replace it in the *output* grid with the global max_color
                            output_grid[r:r + block_h, c:c + block_w] = max_color
                            
    # 4. Return the modified grid
    return output_grid