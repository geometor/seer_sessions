import numpy as np

"""
Transforms the input grid by:
1. Identifying the unique 2x2 block of non-white pixels (the source_block).
2. Copying the input grid to the output grid.
3. Painting four new 2x2 monochromatic blocks at the absolute corners of the output grid.
4. The color of each new corner block is determined by the pixel diagonally opposite to its relative corner within the source_block.
   - Top-Left corner block uses the color of the source_block's Bottom-Right pixel.
   - Top-Right corner block uses the color of the source_block's Bottom-Left pixel.
   - Bottom-Left corner block uses the color of the source_block's Top-Right pixel.
   - Bottom-Right corner block uses the color of the source_block's Top-Left pixel.
5. The original source_block remains unchanged in the output grid.
"""

def find_source_block_top_left(grid: np.ndarray) -> tuple[int, int] | None:
    """
    Finds the top-left coordinate (r, c) of the first 2x2 block 
    where all four pixels are non-white (color != 0).
    Assumes there is exactly one such block based on the task description.
    
    Args:
        grid: The input grid as a NumPy array.
        
    Returns:
        A tuple (row, col) of the top-left corner, or None if not found.
    """
    rows, cols = grid.shape
    for r in range(rows - 1):
        for c in range(cols - 1):
            # Check if all four cells in the 2x2 block starting at (r, c) are non-white
            if (grid[r, c] != 0 and 
                grid[r, c+1] != 0 and
                grid[r+1, c] != 0 and
                grid[r+1, c+1] != 0):
                return r, c
    return None # Should not happen based on task constraints

def paint_block(grid: np.ndarray, top_left_r: int, top_left_c: int, height: int, width: int, color: int):
    """
    Fills a rectangular block in the grid with a specified color.
    Uses NumPy slicing for efficiency. Assumes coordinates and dimensions are valid.
    
    Args:
        grid: The NumPy array representing the grid (modified in-place).
        top_left_r: The starting row index.
        top_left_c: The starting column index.
        height: The height of the block.
        width: The width of the block.
        color: The color value to fill the block with.
    """
    grid[top_left_r : top_left_r + height, top_left_c : top_left_c + width] = color

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    
    Args:
        input_grid: A list of lists representing the input grid.
        
    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input list of lists to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_np)
    H, W = output_grid.shape # Get grid dimensions

    # 1. Locate the source 2x2 block
    block_coord = find_source_block_top_left(input_np)
    if block_coord is None:
        # Handle case where no block is found (shouldn't occur per task)
        print("Warning: No source 2x2 non-white block found.")
        return output_grid.tolist() 
        
    r, c = block_coord

    # 2. Identify the colors A, B, C, D from the source block
    color_A = input_np[r, c]       # Top-left
    color_B = input_np[r, c+1]     # Top-right
    color_C = input_np[r+1, c]     # Bottom-left
    color_D = input_np[r+1, c+1]   # Bottom-right

    # 3. Define the locations and colors for the new 2x2 corner blocks
    #    Structure: (top_left_r, top_left_c, color)
    #    Ensure grid is large enough for 2x2 blocks.
    if H >= 2 and W >= 2:
      new_blocks_info = [
          (0, 0, color_D),       # Top-Left New Block (uses color D)
          (0, W - 2, color_C),   # Top-Right New Block (uses color C)
          (H - 2, 0, color_B),   # Bottom-Left New Block (uses color B)
          (H - 2, W - 2, color_A) # Bottom-Right New Block (uses color A)
      ]

      # 4. Paint the new blocks onto the output grid
      for block_r, block_c, block_color in new_blocks_info:
          paint_block(output_grid, block_r, block_c, 2, 2, block_color)
    else:
        print("Warning: Grid is too small to place 2x2 blocks.")


    # Convert back to list of lists for the expected output format
    return output_grid.tolist()