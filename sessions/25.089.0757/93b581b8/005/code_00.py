import numpy as np

"""
Transforms the input grid by:
1. Identifying the unique 2x2 block of non-white pixels (the source_block) in the input grid.
2. Creating a new output grid of the same dimensions as the input, initialized to all white pixels (0).
3. Painting four new 2x2 monochromatic blocks at the absolute corners of the output grid.
4. The color of each new corner block is determined by the pixel diagonally opposite to its relative corner within the source_block.
   - Top-Left corner block uses the color of the source_block's Bottom-Right pixel (D).
   - Top-Right corner block uses the color of the source_block's Bottom-Left pixel (C).
   - Bottom-Left corner block uses the color of the source_block's Top-Right pixel (B).
   - Bottom-Right corner block uses the color of the source_block's Top-Left pixel (A).
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
    # Ensure indices are within bounds
    end_r = min(top_left_r + height, grid.shape[0])
    end_c = min(top_left_c + width, grid.shape[1])
    start_r = max(0, top_left_r)
    start_c = max(0, top_left_c)

    if start_r < end_r and start_c < end_c:
        grid[start_r : end_r, start_c : end_c] = color


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
    H, W = input_np.shape # Get grid dimensions

    # 1. Initialize output_grid as a white canvas of the same size
    output_grid = np.zeros_like(input_np, dtype=int)

    # 2. Locate the source 2x2 block in the input grid
    block_coord = find_source_block_top_left(input_np)
    
    # If no source block is found (unlikely based on examples), return the white grid
    if block_coord is None:
        print("Warning: No source 2x2 non-white block found.")
        return output_grid.tolist() 
        
    r, c = block_coord

    # 3. Identify the colors A, B, C, D from the source block in the input grid
    # Ensure coordinates + offset are within bounds (though find_source_block_top_left should guarantee this)
    if r+1 < H and c+1 < W:
      color_A = input_np[r, c]       # Top-left
      color_B = input_np[r, c+1]     # Top-right
      color_C = input_np[r+1, c]     # Bottom-left
      color_D = input_np[r+1, c+1]   # Bottom-right
    else:
      # This case should not be reached if find_source_block_top_left works correctly
      print("Warning: Source block location is out of expected bounds.")
      return output_grid.tolist() 


    # 4. Define the locations and colors for the new 2x2 corner blocks
    #    Structure: (top_left_r, top_left_c, color)
    #    Ensure grid is large enough for 2x2 blocks before painting.
    if H >= 2 and W >= 2:
      new_blocks_info = [
          (0, 0, color_D),       # Top-Left New Block (uses source bottom-right color D)
          (0, W - 2, color_C),   # Top-Right New Block (uses source bottom-left color C)
          (H - 2, 0, color_B),   # Bottom-Left New Block (uses source top-right color B)
          (H - 2, W - 2, color_A) # Bottom-Right New Block (uses source top-left color A)
      ]

      # 5. Paint the new blocks onto the white output grid
      for block_r, block_c, block_color in new_blocks_info:
          paint_block(output_grid, block_r, block_c, 2, 2, block_color)
    else:
        # If the grid is too small, no blocks can be painted, return the white grid.
        print(f"Warning: Grid size ({H}x{W}) is too small to place 2x2 blocks.")


    # 6. Convert back to list of lists for the expected output format
    return output_grid.tolist()