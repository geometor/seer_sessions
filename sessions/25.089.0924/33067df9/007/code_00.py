import numpy as np

"""
Transforms an input grid containing sparse colored pixels into a 26x26 output grid.
The output grid has a 2-pixel white border. The inner 22x22 active area displays 
solid-colored blocks corresponding to the non-white pixels in the input grid.

The transformation follows these rules:
1. Identify the rows and columns in the input grid that contain at least one non-white pixel ('active' rows/columns).
2. The output grid is always 26x26 with a 2-pixel white border. The central 22x22 area is used for drawing blocks.
3. The number of block rows in the output corresponds to the number of active input rows (N_rows).
4. The number of potential block columns in the output corresponds to the number of active input columns (N_cols).
5. All blocks in the output have a uniform height, calculated to fit N_rows blocks and (N_rows - 1) gaps of 2 pixels within the 22x22 active height.
6. Blocks originating from pixels in the same input row are placed in the same output block row.
7. Blocks originating from pixels in the same input row will merge horizontally if:
    a) Their corresponding input column indices map to consecutive output block column indices.
    b) They have the same color.
8. The width of a potentially merged block is calculated based on the base width of a single block and the number of merged segments. The base width is calculated to fit N_cols blocks and (N_cols - 1) gaps of 2 pixels within the 22x22 active width.
9. The color of each output block (or merged block) is determined by the color of the corresponding input pixel(s).
10. The top-left position of each block (or merged block) is determined by its mapped row/column index in the output block grid layout, considering the border and gap sizes.
"""

def transform(input_grid):
    """
    Applies the grid transformation rule with potential horizontal merging.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed 26x26 output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)

    # Define constants for the output grid layout
    output_size = 26
    border_size = 2
    gap_size = 2
    background_color = 0
    active_area_dimension = output_size - 2 * border_size # 22

    # Initialize the output grid with the background color
    output_grid = np.full((output_size, output_size), background_color, dtype=int)

    # 1. Find coordinates of non-white pixels
    non_white_coordinates = np.argwhere(input_np != background_color)

    # 2. Handle empty input
    if non_white_coordinates.size == 0:
        return output_grid.tolist() 

    # 3. Identify unique active rows and columns and count them
    active_rows = sorted(list(np.unique(non_white_coordinates[:, 0])))
    active_cols = sorted(list(np.unique(non_white_coordinates[:, 1])))
    N_rows = len(active_rows)
    N_cols = len(active_cols)
    
    # Defensive check (should not happen if non_white_coordinates is not empty)
    if N_rows == 0 or N_cols == 0:
         return output_grid.tolist()

    # 4. Calculate the uniform block height and the base block width (for a single unmerged block)
    # Use integer division //
    if N_rows == 1:
         block_height = active_area_dimension
    else:
         # Total height available for blocks = active_area_dimension - total gap height
         block_height = (active_area_dimension - (N_rows - 1) * gap_size) // N_rows
    
    if N_cols == 1:
         base_block_width = active_area_dimension
    else:
         # Total width available for blocks = active_area_dimension - total gap width
         base_block_width = (active_area_dimension - (N_cols - 1) * gap_size) // N_cols

    # Ensure block dimensions are at least 1 if calculation yields 0 or less
    block_height = max(1, block_height)
    base_block_width = max(1, base_block_width)
    
    # 5. Create mappings from input row/col index to output block layout index (0-based)
    # row_map maps active input row index 'r' to output block row index 'i'
    row_map = {r: i for i, r in enumerate(active_rows)}
    # col_map maps active input col index 'c' to output block col index 'j'
    col_map = {c: j for j, c in enumerate(active_cols)} 

    # 6. Iterate through each ACTIVE input row to handle potential merging
    for i, r in enumerate(active_rows): # i is the output block row index, r is the input row index
        # a. Find non-white pixels specifically in this input row 'r'
        # Get indices within non_white_coordinates that match the current row 'r'
        row_pixel_coord_indices = np.where(non_white_coordinates[:, 0] == r)[0]
        
        # Should not be empty because 'r' is from active_rows, but check defensively
        if row_pixel_coord_indices.size == 0: 
            continue 

        # b. Extract relevant info: (output_col_index_j, input_col_c, color)
        pixel_info_in_row = []
        for idx in row_pixel_coord_indices:
            # Get the full coordinate [r, c] from the main list
            coord = non_white_coordinates[idx] 
            c = coord[1] # Input column index
            color = input_np[r, c] # Color of the pixel
            j = col_map[c] # Corresponding output block column index
            pixel_info_in_row.append({'j': j, 'c': c, 'color': color})
            
        # c. Sort these pixels based on their output column index (j) to process left-to-right
        pixel_info_in_row.sort(key=lambda x: x['j'])

        # d. Iterate through sorted pixels, grouping consecutive pixels by color for merging
        k = 0 # Index for iterating through pixel_info_in_row
        while k < len(pixel_info_in_row):
            # Start of a potential merge group
            start_j = pixel_info_in_row[k]['j']
            current_color = pixel_info_in_row[k]['color']
            
            # Find how many consecutive pixels (in terms of 'j') share the same color
            merge_count = 1
            last_j = start_j
            # Look ahead to check for merge conditions
            while (k + merge_count < len(pixel_info_in_row) and 
                   pixel_info_in_row[k + merge_count]['j'] == last_j + 1 and # Is the next pixel's 'j' consecutive?
                   pixel_info_in_row[k + merge_count]['color'] == current_color): # Does it have the same color?
                last_j = pixel_info_in_row[k + merge_count]['j'] # Update last_j for the next check
                merge_count += 1 # Increment count of merged blocks

            # e. Calculate properties of the (potentially merged) block
            # Width = sum of base widths + sum of gaps between merged blocks
            merged_block_width = merge_count * base_block_width + (merge_count - 1) * gap_size
            
            # Calculate the top-left corner (out_r_start, out_c_start) for the block in the output grid
            # Output row position depends on 'i' (output block row index)
            out_r_start = border_size + i * (block_height + gap_size)
            # Output column position depends on 'start_j' (output block col index of the first block in the group)
            out_c_start = border_size + start_j * (base_block_width + gap_size)
            
            # Calculate the bottom-right corner coordinates (exclusive end points for slicing)
            out_r_end = out_r_start + block_height
            out_c_end = out_c_start + merged_block_width

            # f. Fill the calculated block area in the output grid with the determined color
            # Numpy slicing handles the dimensions based on start/end indices
            output_grid[out_r_start:out_r_end, out_c_start:out_c_end] = current_color
            
            # Move index 'k' past the group we just processed
            k += merge_count

    # 7. Return the completed output grid as a standard list of lists
    return output_grid.tolist()