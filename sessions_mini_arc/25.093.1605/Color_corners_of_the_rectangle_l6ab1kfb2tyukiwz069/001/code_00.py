import numpy as np
from scipy.ndimage import label

"""
Transforms an input grid by identifying contiguous blocks of cells with the value 3. 
For each block, it finds the cells located at the minimum and maximum row and column indices 
(corners) within that block. If a cell at a corner position within the block's bounding box 
actually contains the value 3 (i.e., is part of the block), its value is changed to 7 in the output grid. 
Cells with value 0 remain unchanged. Cells with value 3 that are not at the corners of their block 
also remain unchanged.
"""

def find_blocks_and_corners(grid, value_to_find=3):
    """
    Finds contiguous blocks of a specific value and identifies their corner coordinates.

    Args:
        grid (np.array): The input grid.
        value_to_find (int): The value forming the blocks.

    Returns:
        list: A list of lists, where each inner list contains the corner coordinates 
              [(r, c), ...] for a single block.
    """
    # Create a binary mask where the target value is 1, others are 0
    mask = (grid == value_to_find)
    
    # Label connected components (blocks) in the mask
    # structure defines connectivity (8-connectivity in this case, including diagonals, 
    # but standard 4-connectivity is often used for grids. Let's stick to 4 for now based on examples)
    structure = np.array([[0,1,0], [1,1,1], [0,1,0]]) # 4-connectivity
    labeled_array, num_features = label(mask, structure=structure)
    
    all_block_corners = []

    # If no blocks are found, return empty list
    if num_features == 0:
        return all_block_corners

    # Iterate through each found block (label from 1 to num_features)
    for i in range(1, num_features + 1):
        # Find the coordinates (indices) of all cells belonging to the current block
        block_coords = np.argwhere(labeled_array == i)
        
        # If block is empty for some reason, skip
        if block_coords.size == 0:
            continue
            
        # Determine the bounding box of the block
        min_r = np.min(block_coords[:, 0])
        max_r = np.max(block_coords[:, 0])
        min_c = np.min(block_coords[:, 1])
        max_c = np.max(block_coords[:, 1])
        
        # Identify potential corner coordinates
        potential_corners = [
            (min_r, min_c),
            (min_r, max_c),
            (max_r, min_c),
            (max_r, max_c)
        ]
        
        # Filter corners: Keep only those potential corners that are actually part of the current block
        # We check against the labeled_array to ensure the corner belongs to *this* specific block.
        # Remove duplicates if min/max row/col are the same (e.g., single cell or line)
        actual_corners = []
        seen_coords = set()
        for r, c in potential_corners:
            if (r,c) not in seen_coords and labeled_array[r, c] == i:
                 actual_corners.append((r, c))
                 seen_coords.add((r,c))
                 
        if actual_corners:
            all_block_corners.append(actual_corners)
            
    return all_block_corners


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    Identifies blocks of '3's and changes the corner cells of each block to '7'.
    """
    # Convert input list of lists to numpy array for easier processing
    input_array = np.array(input_grid)
    
    # Initialize output_grid as a copy of the input_grid
    output_array = np.copy(input_array)
    
    # Find all blocks of '3's and their corner coordinates
    # Each element in block_corner_sets is a list of corners for *one* block
    block_corner_sets = find_blocks_and_corners(input_array, value_to_find=3)
    
    # Iterate through the sets of corners found
    for corner_set in block_corner_sets:
        # Iterate through each corner coordinate (r, c) in the current set
        for r, c in corner_set:
            # Change the value at the corner position in the output grid to 7
            output_array[r, c] = 7
            
    # Convert the result back to a list of lists
    output_grid = output_array.tolist()

    return output_grid