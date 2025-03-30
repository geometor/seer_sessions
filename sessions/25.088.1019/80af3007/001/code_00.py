import numpy as np

def find_solid_blocks(grid, block_size, color):
    """
    Finds the top-left coordinates of all solid blocks of a given size and color.

    Args:
        grid (np.array): The input grid.
        block_size (tuple): The (height, width) of the block to search for.
        color (int): The color of the block to search for.

    Returns:
        list: A list of (row, col) tuples representing the top-left coordinates
              of found blocks.
    """
    block_h, block_w = block_size
    grid_h, grid_w = grid.shape
    found_blocks = []
    
    # Create the target block pattern
    target_block = np.full(block_size, color, dtype=grid.dtype)

    # Iterate through possible top-left corners
    for r in range(grid_h - block_h + 1):
        for c in range(grid_w - block_w + 1):
            # Extract the subgrid
            subgrid = grid[r:r + block_h, c:c + block_w]
            # Check if the subgrid matches the target block
            if np.array_equal(subgrid, target_block):
                found_blocks.append((r, c))
    return found_blocks

def transform(input_grid):
    """
    Transforms the input grid by identifying 3x3 solid gray blocks and mapping
    their locations to pixels in a 9x9 output grid.

    Rule:
    1. Scan the input grid to find all instances of 3x3 blocks composed entirely
       of gray (5) pixels.
    2. For each 3x3 gray block found starting at input coordinates (r, c),
       determine the corresponding output coordinates (r_out, c_out) by integer
       division: r_out = r // 3, c_out = c // 3.
    3. Create a 9x9 output grid, initially all white (0).
    4. Set the pixel at (r_out, c_out) in the output grid to gray (5) for each
       found block.
    """
    
    input_grid_np = np.array(input_grid, dtype=int)
    block_size = (3, 3)
    block_color = 5
    output_size = (9, 9)
    background_color = 0
    
    # Initialize the output grid with the background color
    output_grid = np.full(output_size, background_color, dtype=int)
    
    # Find all 3x3 gray blocks in the input grid
    found_blocks = find_solid_blocks(input_grid_np, block_size, block_color)
    
    # Map the found blocks to the output grid
    for r, c in found_blocks:
        # Calculate output coordinates using integer division
        r_out = r // 3
        c_out = c // 3
        
        # Check if the calculated coordinates are within the output grid bounds
        if 0 <= r_out < output_size[0] and 0 <= c_out < output_size[1]:
             # Set the corresponding pixel in the output grid to the block color
            output_grid[r_out, c_out] = block_color
            
    return output_grid.tolist()