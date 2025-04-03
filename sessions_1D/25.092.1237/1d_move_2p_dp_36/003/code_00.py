"""
Transforms a 1xN input grid by swapping the first contiguous block of non-white pixels 
with the immediately following contiguous block of white pixels.

1. Extracts the single row from the input grid.
2. Scans the row from left to right to identify the first contiguous block of 
   non-white pixels (value != 0). Call this block_A.
3. Identifies the contiguous block of white pixels (value == 0) immediately 
   following block_A. Call this block_B.
4. If both block_A and block_B are found and are adjacent, swaps their positions 
   in the row.
5. The segments of the row before block_A and after block_B remain in their 
   original relative positions.
6. If block_A is not found, or if block_B does not immediately follow block_A, 
   the grid remains unchanged.
7. Returns the transformed row within a 1xN grid structure.
"""

import numpy as np
from typing import List, Tuple, Optional

def find_first_non_white_block(row: List[int]) -> Optional[Tuple[int, int]]:
    """Finds the start and end indices of the first contiguous non-white block."""
    n = len(row)
    start_A = -1
    end_A = -1

    # Find the start index of block_A
    for i in range(n):
        if row[i] != 0:
            start_A = i
            break

    # If no non-white pixels are found
    if start_A == -1:
        return None

    # Find the end index of block_A (last contiguous non-white pixel)
    for i in range(start_A, n):
        if row[i] == 0:
            end_A = i - 1
            break
        # If the block extends to the end of the grid
        if i == n - 1:
            end_A = i
            
    return start_A, end_A

def find_subsequent_white_block(row: List[int], start_search_index: int) -> Optional[Tuple[int, int]]:
    """Finds the start and end indices of the white block starting at start_search_index."""
    n = len(row)
    start_B = start_search_index
    end_B = -1

    # Check if there's space for block_B and if it starts with a white pixel
    if start_B >= n or row[start_B] != 0:
        # No valid block_B found starting at this index
        return None

    # Find the end index of block_B (last contiguous white pixel starting at start_B)
    for i in range(start_B, n):
        if row[i] != 0:
            end_B = i - 1
            break
        # If the block extends to the end of the grid
        if i == n - 1:
            end_B = i
            
    # end_B must be >= start_B if we found a white pixel at start_B
    return start_B, end_B


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the block swapping transformation to the input grid.

    Args:
        input_grid: A NumPy array representing the 1xN input grid.

    Returns:
        A NumPy array representing the transformed 1xN grid.
    """
    # Validate input shape (optional but good practice)
    if input_grid.shape[0] != 1:
        # Or raise an error, depending on expected behavior for invalid input
        return input_grid 

    # Extract the single row and convert to a list
    row = input_grid[0, :].tolist()
    n = len(row)

    # Handle empty row case
    if n == 0:
        return input_grid # Return original empty grid structure

    # --- Step 1: Find the first non-white block (block_A) ---
    block_A_indices = find_first_non_white_block(row)

    # If no block_A is found, return the original grid
    if block_A_indices is None:
        return input_grid
        
    start_A, end_A = block_A_indices

    # --- Step 2: Find the white block immediately following block_A (block_B) ---
    # The search for block_B must start exactly at the position after block_A ends
    block_B_indices = find_subsequent_white_block(row, start_search_index=end_A + 1)
    
    # If no block_B is found immediately following block_A, return the original grid
    if block_B_indices is None:
        return input_grid
        
    start_B, end_B = block_B_indices

    # --- Step 3 & 4: Extract segments and reconstruct the output ---
    # Extract the segment before block_A (might be empty)
    initial_segment = row[0:start_A]
    
    # Extract the content of block_A
    block_A_content = row[start_A : end_A + 1]
    
    # Extract the content of block_B
    block_B_content = row[start_B : end_B + 1]
    
    # Extract the segment after block_B (might be empty)
    final_segment = row[end_B + 1 :]

    # Construct the new row by swapping block_A and block_B
    output_row_list = initial_segment + block_B_content + block_A_content + final_segment
    
    # Convert the result back to a numpy array with the original shape
    output_grid = np.array([output_row_list], dtype=input_grid.dtype)
    
    return output_grid