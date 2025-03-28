```python
"""
Transforms the input grid by identifying specific white rows and columns that act as separators between gray blocks. 
A separator is a maximal contiguous block of all-white rows (or columns) bounded by rows (or columns) containing gray pixels.
These white separator cells are filled primarily with red (2), but cells adjacent (cardinally) to non-separator white areas are filled with blue (1).

1. Identify all row indices that consist entirely of white pixels (0).
2. Group these white row indices into maximal contiguous blocks.
3. Filter these blocks to find "separator row blocks": A block is a separator if the row immediately above its start and the row immediately below its end both contain at least one gray pixel (5). Store all indices within these separator blocks.
4. Repeat steps 1-3 for columns to find "separator column blocks" and store their indices.
5. Create a copy of the input grid for the output.
6. Iterate through each cell (r, c) of the grid.
7. If the cell's original color is white AND (its row index r is in the set of separator rows OR its column index c is in the set of separator columns):
    a. Check its four cardinal neighbors (nr, nc) in the original input grid.
    b. Determine if the cell is an "edge" cell: An edge cell is a separator cell adjacent to a white cell that is *not* part of any separator row or column.
    c. If any valid neighbor (nr, nc) is white AND (nr is NOT a separator row AND nc is NOT a separator column), mark the current cell (r, c) as an edge cell (target color blue).
    d. If the cell is an edge cell, set its color in the output grid to blue (1).
    e. Otherwise (it's an internal separator cell), set its color in the output grid to red (2).
8. Cells not meeting the separator criteria or cells that were originally not white remain unchanged.
9. Return the modified grid.
"""

import numpy as np

def find_contiguous_blocks(indices):
    """
    Groups a sorted list of indices into contiguous blocks.
    Args:
        indices (list): A sorted list of integer indices.
    Returns:
        list: A list of tuples, where each tuple is (start_index, end_index)
              representing a contiguous block.
    """
    if not indices:
        return []

    blocks = []
    start_block = indices[0]
    end_block = indices[0]

    for i in range(1, len(indices)):
        if indices[i] == end_block + 1:
            end_block = indices[i]
        else:
            blocks.append((start_block, end_block))
            start_block = indices[i]
            end_block = indices[i]
    
    # Add the last block
    blocks.append((start_block, end_block))
    return blocks

def transform(input_grid):
    """
    Fills separating white rows/columns between gray blocks with red, marking edges with blue.

    Args:
        input_grid (list of lists): A 2D list representing the input grid.

    Returns:
        list of lists: A 2D list representing the transformed output grid.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    output_grid = np.copy(input_np)

    white = 0
    blue = 1
    red = 2
    gray = 5

    separator_rows = set()
    separator_cols = set()

    # --- Identify Separator Row Blocks ---
    # 1. Find all white rows
    white_row_indices = [r for r in range(height) if np.all(input_np[r, :] == white)]
    
    # 2. Group into contiguous blocks
    row_blocks = find_contiguous_blocks(white_row_indices)

    # 3. Filter for separator blocks
    for start_row, end_row in row_blocks:
        has_gray_above = False
        if start_row > 0:
            if np.any(input_np[start_row - 1, :] == gray):
                has_gray_above = True
        
        has_gray_below = False
        if end_row < height - 1:
             if np.any(input_np[end_row + 1, :] == gray):
                 has_gray_below = True

        if has_gray_above and has_gray_below:
            for r in range(start_row, end_row + 1):
                separator_rows.add(r)

    # --- Identify Separator Column Blocks ---
    # 1. Find all white columns
    white_col_indices = [c for c in range(width) if np.all(input_np[:, c] == white)]

    # 2. Group into contiguous blocks
    col_blocks = find_contiguous_blocks(white_col_indices)
    
    # 3. Filter for separator blocks
    for start_col, end_col in col_blocks:
        has_gray_left = False
        if start_col > 0:
             if np.any(input_np[:, start_col - 1] == gray):
                 has_gray_left = True
        
        has_gray_right = False
        if end_col < width - 1:
            if np.any(input_np[:, end_col + 1] == gray):
                has_gray_right = True

        if has_gray_left and has_gray_right:
            for c in range(start_col, end_col + 1):
                separator_cols.add(c)

    # --- Iterate and Fill Separators ---
    # 4. Create output grid (already done via copy)
    # 5. Iterate through each cell
    for r in range(height):
        for c in range(width):
            # 7. Check if the cell is a white separator cell
            is_separator_cell = (r in separator_rows) or (c in separator_cols)
            
            if input_np[r, c] == white and is_separator_cell:
                target_color = red  # Assume red initially
                is_edge = False

                # 7a & 7b & 7c. Check neighbors for edge condition
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = r + dr, c + dc

                    # Check if neighbor is within bounds
                    if 0 <= nr < height and 0 <= nc < width:
                        # Check if neighbor is white AND NOT part of any separator
                        is_neighbor_white = (input_np[nr, nc] == white)
                        is_neighbor_separator = (nr in separator_rows) or (nc in separator_cols)
                        
                        if is_neighbor_white and not is_neighbor_separator:
                            is_edge = True
                            break # Found an edge condition, no need to check other neighbors

                # 7d. If it's an edge, set target to blue
                if is_edge:
                    target_color = blue
                # 7e. Otherwise, target remains red (already set)

                # Update the output grid
                output_grid[r, c] = target_color
            
            # 8. Cells not meeting criteria or not originally white remain unchanged (already copied)

    # 9. Return the result
    return output_grid.tolist()
```