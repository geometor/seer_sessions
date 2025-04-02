import numpy as np

"""
Identifies pairs of rectangular blocks within the input grid that share the
exact same dimensions (height H, width W) and occupy the same range of columns.
Within each such column range and for each specific dimension (H, W), if there
are exactly two blocks found, one composed entirely of white pixels (0) and
the other containing non-white pixels, the white block is replaced by the
content of the non-white block in the output grid. The rest of the grid
remains unchanged.
"""

def transform(input_grid):
    """
    Transforms the input grid based on finding pairs of blocks with identical
    dimensions and column span, where one block is white (all 0s) and the other is not.
    The white block is replaced by the non-white block's content.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list of integers.

    Returns:
        list of lists: The transformed grid.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    output_grid_np = input_grid_np.copy()
    rows, cols = input_grid_np.shape
    
    # Keep track of the locations of white blocks that have already been replaced
    # Use tuple(r_start, r_end, c_start, c_end) as the key
    processed_white_blocks = set() 

    # 1. Iterate through all possible column spans (c1 to c2 inclusive)
    for c1 in range(cols):
        for c2 in range(c1, cols):
            width = c2 - c1 + 1
            
            # 2. For the current column span, iterate through all possible heights
            for h in range(1, rows + 1):
                
                # 3. Find all blocks of exact size (h, width) located within this column span
                matching_blocks = []
                for r_start in range(rows - h + 1):
                    # Define the location tuple for this potential block
                    loc = (r_start, r_start + h - 1, c1, c2)
                    
                    # Extract the subgrid corresponding to this potential block
                    subgrid = input_grid_np[r_start : r_start + h, c1 : c1 + width]
                    
                    # This check is technically redundant if loops are correct, but safe.
                    if subgrid.shape == (h, width):
                         # Store the location and the actual data of the block
                         matching_blocks.append({'loc': loc, 'data': subgrid})

                # 4. Check if exactly two blocks were found for this specific dimension (h, width) and column span (c1, c2)
                if len(matching_blocks) == 2:
                    block_a = matching_blocks[0]
                    block_b = matching_blocks[1]

                    # 5. Determine if one block is all white (0) and the other is not
                    is_a_white = np.all(block_a['data'] == 0)
                    is_b_white = np.all(block_b['data'] == 0)

                    # Check using XOR: exactly one should be white
                    if is_a_white != is_b_white: 
                        
                        # Identify which block is white and which is non-white
                        white_block = block_a if is_a_white else block_b
                        non_white_block = block_b if is_a_white else block_a

                        # Get the location of the white block as a tuple for set lookup
                        wb_loc_tuple = tuple(white_block['loc'])

                        # 6. Check if this white block has already been processed/replaced
                        if wb_loc_tuple not in processed_white_blocks:
                            
                            # Perform the replacement in the output grid
                            # Get coordinates from the white block's location
                            r_wb_start, r_wb_end, c_wb_start, c_wb_end = white_block['loc']
                            # Copy data from the non-white block to the white block's location
                            output_grid_np[r_wb_start:r_wb_end+1, c_wb_start:c_wb_end+1] = non_white_block['data']
                            
                            # Mark this white block location as processed to prevent duplicate replacements
                            processed_white_blocks.add(wb_loc_tuple)

    # Convert the final numpy array back to a list of lists
    return output_grid_np.tolist()