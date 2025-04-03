import numpy as np
from collections import deque

"""
1. Identify all distinct groups (blocks) of connected cells in the input grid 
   that share the same non-zero digit value. Connectivity includes cells 
   touching horizontally, vertically, or diagonally (8-way connectivity).
2. For each identified block, determine its size (number of cells) and its 
   anchor (the coordinates of the top-most, left-most cell within the block).
3. Discard any blocks with a size of 1.
4. If no blocks remain after discarding single-cell blocks, the output grid 
   is identical to the input grid.
5. If blocks remain, select the target block using the following hierarchical criteria:
    a. Find the minimum anchor row index among all remaining blocks. Consider 
       only blocks having this minimum row index for the next steps.
    b. Among these selected blocks, find the minimum block size. Consider only 
       blocks having this minimum size for the next step.
    c. If only one block remains, it is the target block.
    d. If multiple blocks still remain (i.e., they are tied on minimum anchor 
       row and minimum size), select the one whose anchor has the maximum 
       column index. This is the target block.
6. Create the output grid by copying the input grid.
7. Modify the output grid by changing the value of every cell belonging to the 
   selected target block to 5.
8. Return the modified grid.
"""

def find_blocks(grid):
    """
    Identifies all connected blocks of non-zero cells in the grid.

    Args:
        grid: A numpy array representing the input grid.

    Returns:
        A list of dictionaries, where each dictionary represents a block
        and contains:
        - 'value': The common digit value of the block's cells.
        - 'cells': A list of (row, col) tuples for cells in the block.
        - 'size': The number of cells in the block.
        - 'anchor': A tuple (min_row, min_col) representing the top-left anchor.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    blocks = []
    
    # Define 8 directions for connectivity (horizontal, vertical, diagonal)
    directions = [(-1, -1), (-1, 0), (-1, 1), 
                  (0, -1),           (0, 1), 
                  (1, -1), (1, 0), (1, 1)]

    for r in range(rows):
        for c in range(cols):
            # If cell is non-zero and not visited, start BFS to find a block
            if grid[r, c] != 0 and not visited[r, c]:
                block_value = grid[r, c]
                current_block_cells = []
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c # Initialize anchor candidates

                while q:
                    row, col = q.popleft()
                    current_block_cells.append((row, col))
                    
                    # Update potential anchor (top-most, then left-most)
                    if row < min_r:
                        min_r, min_c = row, col
                    elif row == min_r and col < min_c:
                        min_c = col

                    # Explore neighbors
                    for dr, dc in directions:
                        nr, nc = row + dr, col + dc
                        # Check bounds, matching value, and not visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == block_value and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                # Store the found block
                blocks.append({
                    'value': block_value,
                    'cells': current_block_cells,
                    'size': len(current_block_cells),
                    'anchor': (min_r, min_c)
                })
                
    return blocks

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    
    Args:
        input_grid: A list of lists representing the input grid.
        
    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input to numpy array for easier processing
    grid_np = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input
    output_grid = grid_np.copy()

    # 1. Identify all connected blocks of non-zero cells and calculate properties
    all_blocks = find_blocks(grid_np)

    # 2. Filter out blocks with size 1 or less
    valid_blocks = [block for block in all_blocks if block['size'] > 1]

    # 3. If no valid blocks, return the original grid (as list of lists)
    if not valid_blocks:
        return output_grid.tolist()

    # 4. & 5. Select the target block based on the hierarchical criteria
    
    # 5a. Find minimum anchor row
    min_anchor_row = min(block['anchor'][0] for block in valid_blocks)
    blocks_min_row = [block for block in valid_blocks if block['anchor'][0] == min_anchor_row]

    # Check if only one block qualifies after step 5a
    if len(blocks_min_row) == 1:
        target_block = blocks_min_row[0]
    else:
        # 5b. Find minimum size among those with minimum anchor row
        min_size = min(block['size'] for block in blocks_min_row)
        blocks_min_row_min_size = [block for block in blocks_min_row if block['size'] == min_size]

        # Check if only one block qualifies after step 5b
        if len(blocks_min_row_min_size) == 1:
            target_block = blocks_min_row_min_size[0]
        else:
            # 5d. Find maximum anchor column among those tied on min row and min size
            max_anchor_col = max(block['anchor'][1] for block in blocks_min_row_min_size)
            # There must be exactly one block with the max anchor column at this stage
            target_block = [block for block in blocks_min_row_min_size if block['anchor'][1] == max_anchor_col][0]

    # 6. & 7. Modify the output grid by changing the target block's cells to 5
    for r, c in target_block['cells']:
        output_grid[r, c] = 5

    # 8. Return the modified grid as list of lists
    return output_grid.tolist()