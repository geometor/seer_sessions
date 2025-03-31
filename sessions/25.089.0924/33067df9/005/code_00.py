import numpy as np

"""
Transforms an input grid containing sparse colored pixels into a 26x26 output grid.
The output grid has a 2-pixel white border. The inner 22x22 area displays 
solid-colored blocks corresponding to the non-white pixels in the input. 
The relative positions of the input pixels determine the layout of the blocks 
in the output grid. The size of each block is uniform and calculated based on the 
number of input rows and columns that contain non-white pixels, ensuring they fit 
within the 22x22 active area with 2-pixel gaps between them.
"""

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)

    # Define constants for the output grid layout
    output_size = 26
    border_size = 2
    gap_size = 2
    background_color = 0
    active_area_dimension = output_size - 2 * border_size # Should be 22

    # Initialize the output grid with the background color
    output_grid = np.full((output_size, output_size), background_color, dtype=int)

    # 1. Find coordinates of non-white pixels
    non_white_coordinates = np.argwhere(input_np != background_color)

    # 2. Handle empty input: If no non-background pixels are found, return the initialized output grid.
    if non_white_coordinates.size == 0:
        return output_grid.tolist() 

    # 3. Identify unique active rows and columns and count them
    active_rows = sorted(list(np.unique(non_white_coordinates[:, 0])))
    active_cols = sorted(list(np.unique(non_white_coordinates[:, 1])))
    N_rows = len(active_rows)
    N_cols = len(active_cols)
    
    # Defensive check (should not be needed if non_white_coordinates is not empty)
    if N_rows == 0 or N_cols == 0:
         return output_grid.tolist()

    # 4. Calculate the dimensions of the output blocks using integer division
    # Handle the edge case of a single row or column where there are no gaps
    if N_rows == 1:
         block_height = active_area_dimension
    else:
         # Total space for rows = N_rows * block_height + (N_rows - 1) * gap_size = active_area_dimension
         block_height = (active_area_dimension - (N_rows - 1) * gap_size) // N_rows
    
    if N_cols == 1:
         block_width = active_area_dimension
    else:
         # Total space for cols = N_cols * block_width + (N_cols - 1) * gap_size = active_area_dimension
         block_width = (active_area_dimension - (N_cols - 1) * gap_size) // N_cols

    # Ensure block dimensions are at least 1 if calculation results in 0 or less
    block_height = max(1, block_height)
    block_width = max(1, block_width)
    
    # 5. Create mappings from input row/col index to output block index (0-based)
    row_map = {r: i for i, r in enumerate(active_rows)}
    # Corrected dictionary comprehension for col_map
    col_map = {c: j for j, c in enumerate(active_cols)} 

    # 6. Iterate through each non-white input pixel and draw its corresponding block
    for r, c in non_white_coordinates:
        # a. Get the pixel's color
        color = input_np[r, c]

        # b. Find the corresponding output block's row index i
        i = row_map[r] 
        # c. Find the corresponding output block's column index j
        j = col_map[c]

        # d. Calculate the top-left corner (out_r_start, out_c_start) for the block
        # Formula: offset + block_index * (block_dimension + gap)
        out_r_start = border_size + i * (block_height + gap_size)
        out_c_start = border_size + j * (block_width + gap_size)
        
        # e. Calculate the bottom-right corner coordinates (exclusive)
        out_r_end = out_r_start + block_height
        out_c_end = out_c_start + block_width

        # f. Fill the block in the output grid using slicing
        # Slicing automatically handles the dimensions
        # Ensure indices do not exceed output bounds (numpy slicing handles this gracefully up to the edge)
        output_grid[out_r_start:out_r_end, out_c_start:out_c_end] = color

    # 7. Return the completed output grid as a list of lists
    return output_grid.tolist()