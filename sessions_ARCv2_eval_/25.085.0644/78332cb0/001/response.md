```python
import numpy as np
import itertools

def find_separators(grid_np):
    """
    Find indices of full rows and columns consisting entirely of magenta (6).

    Args:
        grid_np: A numpy array representing the input grid.

    Returns:
        A tuple containing two lists:
        - sep_rows: Indices of rows that are full separators.
        - sep_cols: Indices of columns that are full separators.
    """
    sep_color = 6
    h, w = grid_np.shape
    sep_rows = [r for r in range(h) if np.all(grid_np[r, :] == sep_color)]
    sep_cols = [c for c in range(w) if np.all(grid_np[:, c] == sep_color)]
    return sep_rows, sep_cols

def extract_blocks(grid_np, sep_rows, sep_cols):
    """
    Extracts the rectangular subgrids (blocks) located between the separators.
    Blocks are returned along with their original row/column index within the 
    conceptual grid formed by the separators.

    Args:
        grid_np: A numpy array representing the input grid.
        sep_rows: A list of indices for horizontal separator rows.
        sep_cols: A list of indices for vertical separator columns.

    Returns:
        A list of dictionaries, where each dictionary contains:
        - 'data': The numpy array of the extracted block.
        - 'row': The original row index of the block in the grid-of-blocks.
        - 'col': The original column index of the block in the grid-of-blocks.
    """
    h, w = grid_np.shape
    blocks_info = []
    
    # Define the boundaries for slicing, including edges of the grid
    row_coords = [-1] + sorted(sep_rows) + [h]
    col_coords = [-1] + sorted(sep_cols) + [w]

    # Iterate through the segments defined by row separators
    for r_idx, (r_start, r_end) in enumerate(zip(row_coords[:-1], row_coords[1:])):
        # Iterate through the segments defined by column separators
        for c_idx, (c_start, c_end) in enumerate(zip(col_coords[:-1], col_coords[1:])):
            # Calculate the actual block coordinates (start+1 to exclude separator)
            block_r_start = r_start + 1
            block_r_end = r_end
            block_c_start = c_start + 1
            block_c_end = c_end

            # Check if the calculated coordinates define a valid block area
            if block_r_start < block_r_end and block_c_start < block_c_end:
                block = grid_np[block_r_start:block_r_end, block_c_start:block_c_end]
                # Store the block data and its original position (grid-of-blocks index)
                blocks_info.append({'data': block, 'row': r_idx, 'col': c_idx})
                
    return blocks_info

def transform(input_grid):
    """
    Identifies separator lines (rows or columns of magenta 6) in the input grid.
    Extracts the blocks defined by these separators.
    Reassembles the blocks into a new grid based on the separator configuration:
    - Input Horizontal separators only -> Output Horizontal assembly, blocks ordered bottom-to-top.
    - Input Vertical separators only -> Output Vertical assembly, blocks ordered left-to-right.
    - Input Both separator types -> Output Vertical assembly, blocks ordered TL, BR, TR, BL.
    Separators (single row/column of magenta 6) are inserted between blocks in the output, 
    with orientation opposite to the input separators defining the output assembly direction
    (e.g., horizontal assembly uses vertical separators).
    """
    input_np = np.array(input_grid, dtype=int)
    h, w = input_np.shape
    sep_color = 6

    # 1. & 2. Identify separator rows and columns.
    sep_rows, sep_cols = find_separators(input_np)

    # 3. Determine the type of segmentation based on found separators.
    has_horizontal = bool(sep_rows)
    has_vertical = bool(sep_cols)

    segmentation_type = "none"
    if has_horizontal and has_vertical:
        segmentation_type = "both"
    elif has_horizontal:
        segmentation_type = "horizontal"
    elif has_vertical:
        segmentation_type = "vertical"
    else:
        # If no separators are found, return the input grid unchanged.
        return input_grid 

    # 4. Extract the blocks based on the separators.
    blocks_info = extract_blocks(input_np, sep_rows, sep_cols)
    
    # If no blocks could be extracted (e.g., grid only contains separators), return input.
    if not blocks_info: 
        return input_grid 

    # Assume all blocks have the same dimensions, get from the first block.
    sample_block = blocks_info[0]['data']
    block_h, block_w = sample_block.shape

    # 5. & 6. Determine the output orientation and the order of blocks.
    ordered_blocks = []
    output_orientation = "vertical" # Default, changed if only horizontal seps found

    if segmentation_type == "horizontal":
        output_orientation = "horizontal"
        # Order blocks by their original row index, descending (bottom-up).
        ordered_blocks = [b['data'] for b in sorted(blocks_info, key=lambda x: x['row'], reverse=True)]
    elif segmentation_type == "vertical":
        output_orientation = "vertical"
        # Order blocks by their original column index, ascending (left-to-right).
        ordered_blocks = [b['data'] for b in sorted(blocks_info, key=lambda x: x['col'])]
    elif segmentation_type == "both":
        output_orientation = "vertical"
        # Special order for 'both' case: Top-Left, Bottom-Right, Top-Right, Bottom-Left.
        # Create a dictionary mapping (row, col) index to block data for easy lookup.
        block_dict = {(b['row'], b['col']): b['data'] for b in blocks_info}
        # Define the specific order of indices. Assumes a 2x2 grid structure.
        order_indices = [(0, 0), (1, 1), (0, 1), (1, 0)] # TL, BR, TR, BL
        for r, c in order_indices:
             # Only add the block if it exists for the given index.
             if (r, c) in block_dict: 
                 ordered_blocks.append(block_dict[(r,c)])
             # Note: This implicitly handles grids that might not be perfectly 2x2 
             # by only including the blocks that exist in the specified order.

    # If ordering resulted in no blocks (e.g., missing blocks in 'both' case), return input.
    if not ordered_blocks: 
        return input_grid

    # 7. Construct the output grid by assembling blocks and separators.
    num_blocks = len(ordered_blocks)
    
    if output_orientation == "vertical":
        # Stack blocks vertically, insert horizontal separators between them.
        # Separator is a single row with the width of a block.
        separator = np.full((1, block_w), sep_color, dtype=int)
        output_components = []
        for i, block in enumerate(ordered_blocks):
            output_components.append(block)
            # Add a separator after each block except the last one.
            if i < num_blocks - 1:
                output_components.append(separator)
        # Combine all components vertically.
        output_grid = np.vstack(output_components)
        
    elif output_orientation == "horizontal":
        # Arrange blocks horizontally, insert vertical separators between them.
        # Separator is a single column with the height of a block.
        separator = np.full((block_h, 1), sep_color, dtype=int)
        output_components = []
        for i, block in enumerate(ordered_blocks):
            output_components.append(block)
            # Add a separator after each block except the last one.
            if i < num_blocks - 1:
                output_components.append(separator)
        # Combine all components horizontally.
        output_grid = np.hstack(output_components)
    else:
         # Fallback: Should not be reached due to earlier logic.
         return input_grid

    # Convert the final numpy array back to a list of lists.
    return output_grid.tolist()
```