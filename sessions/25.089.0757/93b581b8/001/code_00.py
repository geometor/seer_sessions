import numpy as np

"""
Transforms the input grid by locating a central 2x2 non-white block and adding four new 2x2 monochromatic blocks around it. 
The color of each new block is determined by the pixel diagonally opposite to its relative corner within the original 2x2 block. 
Specifically:
- Find the 2x2 block of non-white pixels. Let its top-left corner be (r, c).
- The pixels are A (r, c), B (r, c+1), C (r+1, c), D (r+1, c+1).
- A new 2x2 block of color D is placed at (r-1, c-1).
- A new 2x2 block of color C is placed at (r-1, c+2).
- A new 2x2 block of color B is placed at (r+2, c-1).
- A new 2x2 block of color A is placed at (r+2, c+2).
The original 2x2 block remains unchanged.
"""

def find_2x2_block_top_left(grid):
    """
    Finds the top-left coordinate (r, c) of the first 2x2 block 
    where at least the top-left cell is non-white.
    Assumes there is exactly one such block based on the task description.
    """
    rows, cols = grid.shape
    for r in range(rows - 1):
        for c in range(cols - 1):
            # Check if the top-left pixel is non-white
            # A more robust check might ensure all four are non-white,
            # or that it's surrounded by white, but based on examples,
            # finding the first non-white pixel seems sufficient to locate the block.
            if grid[r, c] != 0:
                # Simple check for 2x2 non-white block structure, could be enhanced
                if grid[r+1, c] != 0 or grid[r, c+1] != 0 or grid[r+1, c+1] != 0:
                   return r, c
    return None # Should not happen based on task constraints

def paint_block(grid, top_left_r, top_left_c, height, width, color):
    """
    Fills a rectangular block in the grid with a specified color.
    Handles boundary checks implicitly if NumPy slicing is used carefully.
    """
    # Ensure coordinates are within grid bounds (although problem statement implies they will be)
    rows, cols = grid.shape
    end_r = min(top_left_r + height, rows)
    end_c = min(top_left_c + width, cols)
    start_r = max(top_left_r, 0)
    start_c = max(top_left_c, 0)
    
    grid[start_r:end_r, start_c:end_c] = color

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input list of lists to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_np)

    # 1. Locate the 2x2 block
    block_coord = find_2x2_block_top_left(input_np)
    if block_coord is None:
        # Handle case where no block is found, though task implies one exists
        return output_grid.tolist() 
        
    r, c = block_coord

    # 2. Identify the colors A, B, C, D
    color_A = input_np[r, c]       # Top-left
    color_B = input_np[r, c+1]     # Top-right
    color_C = input_np[r+1, c]     # Bottom-left
    color_D = input_np[r+1, c+1]   # Bottom-right

    # 3. Define the locations and colors for the new 2x2 blocks
    #    Structure: (top_left_r, top_left_c, color)
    new_blocks_info = [
        (r - 1, c - 1, color_D),  # Top-Left New Block (uses color D)
        (r - 1, c + 2, color_C),  # Top-Right New Block (uses color C)
        (r + 2, c - 1, color_B),  # Bottom-Left New Block (uses color B)
        (r + 2, c + 2, color_A)   # Bottom-Right New Block (uses color A)
    ]

    # 4. Paint the new blocks onto the output grid
    for block_r, block_c, block_color in new_blocks_info:
        paint_block(output_grid, block_r, block_c, 2, 2, block_color)

    # Convert back to list of lists for the expected output format
    return output_grid.tolist()