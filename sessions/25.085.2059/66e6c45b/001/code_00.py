import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by taking the four pixels from the central 2x2 non-background block 
    and moving them to the four corners of the output grid. The rest of the output grid is 
    filled with the background color (0).
    - The top-left pixel of the input block moves to the top-left corner (0, 0).
    - The top-right pixel of the input block moves to the top-right corner (0, width-1).
    - The bottom-left pixel of the input block moves to the bottom-left corner (height-1, 0).
    - The bottom-right pixel of the input block moves to the bottom-right corner (height-1, width-1).
    """

    # Convert input list of lists to a NumPy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Initialize the output grid with the background color (0)
    # It has the same dimensions as the input grid.
    output_grid = np.zeros_like(input_np)

    # Identify the coordinates of the central 2x2 block's top-left corner.
    # Based on the examples (4x4 grids), the block starts at (1, 1).
    # Note: This assumes the grid is 4x4 and the block is always at (1,1).
    # A more general solution might search for the block.
    if height == 4 and width == 4:
        block_r, block_c = 1, 1 # Top-left corner of the 2x2 block in a 4x4 grid
    else:
        # If the grid size is different, this specific logic might fail.
        # For now, proceed assuming the 4x4 structure from examples.
        # A more robust approach would dynamically find the non-zero block.
        # Let's find the first non-zero pixel and assume it's the top-left of the block.
        non_zero_coords = np.argwhere(input_np != 0)
        if non_zero_coords.size > 0:
            block_r, block_c = non_zero_coords[0] 
        else:
             # No non-zero pixels found, return the all-zero grid.
             return output_grid.tolist()


    # Check if the identified coordinates and the expected block structure are valid
    # Ensure the block fits within the grid dimensions from the identified top-left.
    if (block_r + 1 < height and block_c + 1 < width):
        
        # Extract the pixel values from the 2x2 block in the input grid
        pixel_tl = input_np[block_r, block_c]
        pixel_tr = input_np[block_r, block_c + 1]
        pixel_bl = input_np[block_r + 1, block_c]
        pixel_br = input_np[block_r + 1, block_c + 1]

        # Place the extracted pixels into the corresponding corners of the output grid
        output_grid[0, 0] = pixel_tl                # Map input top-left to output top-left corner
        output_grid[0, width - 1] = pixel_tr        # Map input top-right to output top-right corner
        output_grid[height - 1, 0] = pixel_bl      # Map input bottom-left to output bottom-left corner
        output_grid[height - 1, width - 1] = pixel_br # Map input bottom-right to output bottom-right corner
    
    # Convert the NumPy array back to a list of lists before returning
    return output_grid.tolist()