import numpy as np

def find_non_zero_in_block(grid, start_row, end_row, start_col, end_col):
    """
    Finds the single non-zero value within a specified block of the grid.
    Assumes there is exactly one non-zero value in the block.
    """
    for r in range(start_row, end_row):
        for c in range(start_col, end_col):
            if grid[r, c] != 0:
                return grid[r, c]
    # Should not happen based on task description, but added for robustness
    return 0 

def transform(input_grid):
    """
    Extracts non-white pixels from a 3x3 grid of blocks within the input 
    and arranges them into a 3x3 output grid based on their block origin.

    The input grid is divided into nine equal-sized subgrids (blocks) 
    arranged in a 3x3 pattern. The size of each block is 
    (input_height/3) x (input_width/3). For each block, the single 
    non-white pixel within it is found. A new 3x3 grid is created, and 
    the extracted non-white pixel from the input block at position 
    (block_row, block_col) is placed into the output grid at the 
    corresponding position (block_row, block_col).
    """
    
    # Convert input list of lists to a numpy array for easier slicing
    input_grid_np = np.array(input_grid, dtype=int)
    
    # Determine the dimensions of the input grid
    H, W = input_grid_np.shape
    
    # Calculate the dimensions of the blocks
    # Using integer division // ensures we get integer dimensions
    block_height = H // 3
    block_width = W // 3
    
    # Initialize an empty 3x3 grid (numpy array) to store the output
    # Fill with zeros initially, although they will be overwritten
    output_grid = np.zeros((3, 3), dtype=int)
    
    # Iterate through the 3x3 grid of blocks
    for block_row in range(3):
        for block_col in range(3):
            # Calculate the row and column boundaries for the current block
            start_row = block_row * block_height
            end_row = (block_row + 1) * block_height
            start_col = block_col * block_width
            end_col = (block_col + 1) * block_width
            
            # Find the single non-zero pixel within this block
            # OPTION 1: Using nested loops (more explicit)
            pixel_value = 0
            found = False
            for r in range(start_row, end_row):
                for c in range(start_col, end_col):
                    if input_grid_np[r, c] != 0:
                        pixel_value = input_grid_np[r, c]
                        found = True
                        break # Found the pixel, exit inner loop
                if found:
                    break # Found the pixel, exit outer loop
            
            # OPTION 2: Using numpy slicing (more concise)
            # block = input_grid_np[start_row:end_row, start_col:end_col]
            # # Find non-zero elements in the block and take the first one
            # # Assumes exactly one non-zero element exists per block based on task description
            # non_zero_elements = block[block != 0]
            # if non_zero_elements.size > 0:
            #     pixel_value = non_zero_elements[0]
            # else:
            #     # Handle cases where a block might unexpectedly be empty, though unlikely for this task
            #     pixel_value = 0 # Or raise an error
            
            # Place the found pixel value into the output grid at the corresponding position
            output_grid[block_row, block_col] = pixel_value
            
    # Return the completed 3x3 output grid (convert back to list of lists if required by ARC standard)
    return output_grid.tolist()