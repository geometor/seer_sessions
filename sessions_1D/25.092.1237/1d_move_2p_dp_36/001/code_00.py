import numpy as np
from typing import List, Tuple

"""
Transforms a 1D grid (list of integers) based on the following rule:
1. Scan the input grid from left to right to identify the first contiguous block of non-white pixels (value != 0). Call this block_A.
2. Identify the contiguous block of white pixels (value == 0) immediately following block_A. Call this block_B.
3. If both block_A and block_B are found and are adjacent, swap their positions in the grid.
4. The segments of the grid before block_A and after block_B remain in their original relative positions.
5. If block_A is not found, or if block_B does not immediately follow block_A, the grid remains unchanged.
"""

def transform(input_grid: List[int]) -> List[int]:
    """
    Applies the block swapping transformation to the input grid.

    Args:
        input_grid: A list of integers representing the pixels in a single row.

    Returns:
        A new list of integers representing the transformed grid.
    """
    
    # Ensure input is a list for easier manipulation
    grid = list(input_grid)
    n = len(grid)

    # Handle empty grid case
    if n == 0:
        return []

    # --- Step 1: Find the first non-white block (block_A) ---
    start_A = -1
    end_A = -1
    
    # Find the start index of block_A
    for i in range(n):
        if grid[i] != 0:
            start_A = i
            break

    # If no non-white pixels are found, return the grid unchanged
    if start_A == -1:
        return grid

    # Find the end index of block_A (last contiguous non-white pixel)
    for i in range(start_A, n):
        if grid[i] == 0:
            end_A = i - 1
            break
        # If the block extends to the end of the grid
        if i == n - 1:
            end_A = i
            
    # --- Step 2: Find the white block immediately following block_A (block_B) ---
    start_B = end_A + 1
    end_B = -1

    # Check if there's space for block_B and if it starts with a white pixel
    if start_B >= n or grid[start_B] != 0:
        # No valid block_B found immediately after block_A
        return grid

    # Find the end index of block_B (last contiguous white pixel starting at start_B)
    for i in range(start_B, n):
        if grid[i] != 0:
            end_B = i - 1
            break
        # If the block extends to the end of the grid
        if i == n - 1:
            end_B = i

    # At this point, end_B must be >= start_B because we know grid[start_B] == 0
            
    # --- Step 3 & 4: Extract segments and reconstruct the output ---
    # Extract the segment before block_A (might be empty)
    initial_segment = grid[0:start_A]
    
    # Extract the content of block_A
    block_A_content = grid[start_A : end_A + 1]
    
    # Extract the content of block_B
    block_B_content = grid[start_B : end_B + 1]
    
    # Extract the segment after block_B (might be empty)
    final_segment = grid[end_B + 1 :]

    # Construct the output grid by swapping block_A and block_B
    output_grid = initial_segment + block_B_content + block_A_content + final_segment
    
    return output_grid
