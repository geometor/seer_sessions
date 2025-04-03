import numpy as np
from typing import List, Tuple

"""
Transforms a 1D grid by identifying segments: leading white space, the first contiguous block of non-white pixels (mobile block), the white space separating the mobile block from the next non-white pixel (separating whitespace), the first non-white pixel after the mobile block (anchor pixel), and the trailing white space. The transformation reconstructs the grid by rearranging these segments: the separating whitespace is moved to the beginning, followed by the original leading whitespace, the mobile block, the anchor pixel, and finally the trailing whitespace.

1.  Scan the input grid to find the start and end indices of the first contiguous block of non-white pixels (the "mobile block").
2.  Identify the "leading whitespace" as pixels before the mobile block start.
3.  Scan from the end of the mobile block to find the index and value of the next non-white pixel (the "anchor pixel").
4.  Identify the "separating whitespace" as the white pixels between the mobile block's end and the anchor pixel's index.
5.  Identify the "trailing whitespace" as pixels after the anchor pixel.
6.  Construct the output grid by concatenating: separating whitespace, leading whitespace, mobile block pixels, the anchor pixel, and trailing whitespace.
"""


def find_first_non_white_block_indices(grid_1d: List[int]) -> Tuple[int, int]:
    """
    Finds the start index (inclusive) and end index (exclusive) of the 
    first contiguous block of non-white pixels.

    Returns:
        Tuple[int, int]: (start_index, end_index). Returns (-1, -1) if no 
                         non-white block is found.
    """
    start_index = -1
    end_index = -1
    n = len(grid_1d)

    # Find the start of the block
    for i, pixel in enumerate(grid_1d):
        if pixel != 0:
            start_index = i
            break
            
    # If no non-white pixel found, return (-1, -1)
    if start_index == -1:
        return -1, -1

    # Find the end of the block (first white pixel after start_index)
    end_index = start_index # Initialize end_index assume block has length at least 1
    for i in range(start_index, n):
        if grid_1d[i] == 0:
            end_index = i
            break
        # If loop finishes without finding a 0, the block goes to the end
        if i == n - 1 and grid_1d[i] != 0: 
             end_index = n # End index is exclusive

    return start_index, end_index

def find_first_non_white_after_index(grid_1d: List[int], start_search_index: int) -> Tuple[int, int]:
    """
    Finds the index and value of the first non-white pixel at or after 
    start_search_index.

    Returns:
        Tuple[int, int]: (index, value). Returns (-1, -1) if none found.
    """
    for i in range(start_search_index, len(grid_1d)):
        if grid_1d[i] != 0:
            return i, grid_1d[i]
    return -1, -1 # Not found

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule to the input grid.
    """
    # Ensure input is treated as 1D
    if not input_grid or len(input_grid) != 1:
        # Handle invalid input if necessary, though ARC tasks usually provide valid examples
        # Return unchanged grid for robustness
        return input_grid 
        
    grid_1d = input_grid[0]
    grid_len = len(grid_1d)

    # --- 1. Identify Mobile Block ---
    mobile_start, mobile_end = find_first_non_white_block_indices(grid_1d)
    
    # Handle case where no mobile block is found (e.g., all white grid)
    if mobile_start == -1:
         return input_grid # Return original grid if no pattern detected

    # Extract mobile block pixels
    mobile_block = grid_1d[mobile_start:mobile_end]

    # --- 2. Identify Leading Whitespace ---
    leading_whitespace = grid_1d[:mobile_start]

    # --- 3. Identify Anchor Pixel ---
    # Search for the first non-white pixel *after* the mobile block ends
    anchor_index, anchor_pixel = find_first_non_white_after_index(grid_1d, mobile_end)

    # Handle case where no anchor pixel is found after the mobile block
    if anchor_index == -1:
        # This case might imply the mobile block is at the very end, or only trailing whitespace follows.
        # Based on examples, an anchor always exists. If not, maybe return original?
        # For now, assume anchor exists as per examples. If error occurs, this needs review.
         return input_grid # Or potentially handle differently if this case is valid

    # --- 4. Identify Separating Whitespace ---
    # Pixels between the end of the mobile block and the anchor pixel
    separating_whitespace = grid_1d[mobile_end:anchor_index]

    # --- 5. Identify Trailing Whitespace ---
    # Pixels after the anchor pixel
    trailing_whitespace = grid_1d[anchor_index+1:]

    # --- 6. Construct Output Grid ---
    # Concatenate the parts in the new order:
    # separating_whitespace + leading_whitespace + mobile_block + [anchor_pixel] + trailing_whitespace
    output_grid_1d = separating_whitespace + leading_whitespace + mobile_block + [anchor_pixel] + trailing_whitespace

    # Ensure the output grid maintains the original length (sanity check)
    if len(output_grid_1d) != grid_len:
         # Handle potential length mismatch error, though logic should preserve length
         print(f"Warning: Output length {len(output_grid_1d)} differs from input length {grid_len}")
         # Fallback or error handling needed here if this occurs
         return input_grid # Safer to return original if length changes unexpectedly

    # Format the output as a list containing one list (1xN grid)
    output_grid = [output_grid_1d]

    return output_grid