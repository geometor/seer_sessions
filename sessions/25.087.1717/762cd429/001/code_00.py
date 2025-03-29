import numpy as np

def find_pattern_block(grid):
    """
    Finds the top-left corner (r, c) and colors [[c1, c2], [c3, c4]] 
    of the first 2x2 block of non-background (non-zero) pixels.
    
    Args:
        grid (np.array): The input grid.

    Returns:
        tuple: (r, c, c1, c2, c3, c4) if found, otherwise None.
    """
    height, width = grid.shape
    for r in range(height - 1):
        for c in range(width - 1):
            # Check if all four pixels in the 2x2 block are non-zero
            if grid[r, c] != 0 and \
               grid[r, c+1] != 0 and \
               grid[r+1, c] != 0 and \
               grid[r+1, c+1] != 0:
                c1 = grid[r, c]
                c2 = grid[r, c+1]
                c3 = grid[r+1, c]
                c4 = grid[r+1, c+1]
                return r, c, c1, c2, c3, c4
    return None # Should not happen based on task description

def draw_if_fits(grid, r_start, c_start, block_array):
    """
    Draws the block_array onto the grid at (r_start, c_start) 
    only if the entire block fits within the grid boundaries.

    Args:
        grid (np.array): The target grid to draw on.
        r_start (int): The starting row index.
        c_start (int): The starting column index.
        block_array (np.array): The block of pixels to draw.
    """
    block_height, block_width = block_array.shape
    grid_height, grid_width = grid.shape
    
    r_end = r_start + block_height
    c_end = c_start + block_width
    
    # Check boundaries
    if r_start >= 0 and c_start >= 0 and r_end <= grid_height and c_end <= grid_width:
        # Draw the block
        grid[r_start:r_end, c_start:c_end] = block_array

def transform(input_grid):
    """
    Generates multiple colored rectangular blocks based on a 2x2 pattern 
    block found in the input grid. The generation rules involve scaling 
    the pattern and creating larger blocks based on the columns of the 
    pattern at specific relative offsets. Blocks are only drawn if they 
    fit entirely within the grid boundaries.

    1. Find the unique 2x2 non-white pattern block [[c1, c2], [c3, c4]] 
       at location (r, c).
    2. Initialize an output grid of the same size as the input, filled with white (0).
    3. Copy the original 2x2 block to the output grid at (r, c).
    4. Define potential generated blocks based on rules (scaling, columnar expansion) 
       with specific relative offsets from (r, c).
    5. For each potential block, check if it fits within the grid boundaries.
    6. If a block fits, draw it onto the output grid.
    """
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape
    
    # Find the 2x2 pattern block
    pattern_info = find_pattern_block(input_array)
    if pattern_info is None:
        # If no pattern found (unexpected), return a copy of the input or an empty grid
        return input_grid 
        
    r, c, c1, c2, c3, c4 = pattern_info

    # Initialize output grid
    output_array = np.zeros_like(input_array)

    # 1. Copy the original pattern block
    original_block = input_array[r:r+2, c:c+2]
    draw_if_fits(output_array, r, c, original_block)

    # 2. Generate and attempt to draw the scaled 4x4 block
    scaled_block = np.array([[c1, c1, c2, c2],
                             [c1, c1, c2, c2],
                             [c3, c3, c4, c4],
                             [c3, c3, c4, c4]], dtype=int)
    draw_if_fits(output_array, r - 1, c + 2, scaled_block)

    # 3. Generate and attempt to draw the first column 4x4 blocks
    block_c1_4x4 = np.full((4, 4), c1, dtype=int)
    block_c3_4x4 = np.full((4, 4), c3, dtype=int)
    draw_if_fits(output_array, r - 3, c + 6, block_c1_4x4)
    draw_if_fits(output_array, r + 1, c + 6, block_c3_4x4)

    # 4. Generate and attempt to draw the second column 4x4 blocks
    block_c2_4x4 = np.full((4, 4), c2, dtype=int)
    block_c4_4x4 = np.full((4, 4), c4, dtype=int)
    draw_if_fits(output_array, r - 3, c + 10, block_c2_4x4)
    draw_if_fits(output_array, r + 1, c + 10, block_c4_4x4)

    # 5. Generate and attempt to draw the first column 8x8 blocks
    block_c1_8x8 = np.full((8, 8), c1, dtype=int)
    block_c3_8x8 = np.full((8, 8), c3, dtype=int)
    draw_if_fits(output_array, r - 7, c + 14, block_c1_8x8)
    draw_if_fits(output_array, r + 1, c + 14, block_c3_8x8)
    
    # 6. Generate and attempt to draw the second column 8x8 blocks
    block_c2_8x8 = np.full((8, 8), c2, dtype=int)
    block_c4_8x8 = np.full((8, 8), c4, dtype=int)
    draw_if_fits(output_array, r - 7, c + 22, block_c2_8x8)
    draw_if_fits(output_array, r + 1, c + 22, block_c4_8x8)

    # Convert back to list of lists for the expected output format
    return output_array.tolist()