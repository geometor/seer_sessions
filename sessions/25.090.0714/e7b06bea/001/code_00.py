import numpy as np
import math

"""
Transforms the input grid based on the following rules:
1. Identify the rightmost contiguous block of non-background (0), non-gray (5) vertical lines. Each column in this block must consist entirely of a single color.
2. Extract the colors (C1, C2, ..., Ck) from left to right within this block, and note the column index (min_col) of the block's leftmost column.
3. Determine a repetition factor 'rep' by finding the height of the contiguous segment of gray (5) pixels starting from the top-left cell (0,0). If cell (0,0) is not gray or column 0 doesn't exist, default 'rep' to 1. Ensure 'rep' is at least 1.
4. Calculate the target column index for the output line: target_col = min_col - 1.
5. Create an output grid of the same dimensions as the input, filled entirely with the background color (0).
6. Populate the 'target_col' in the output grid row by row. For each row 'r', the color used is determined by cycling through the extracted colors C1...Ck, where each color is repeated 'rep' times consecutively. The formula for the color is colors[(r // rep) % k].
7. Check if the input grid contains any gray (5) pixels in column 0.
8. If gray pixels exist in column 0 of the input grid AND the calculated 'target_col' is not equal to 3, then copy the entire contents of column 0 from the input grid to column 0 of the output grid. Otherwise, column 0 of the output grid remains background color (unless it is the target_col itself).
9. Return the final output grid.
"""

# Constants for colors
BG_COLOR = 0
GRAY_COLOR = 5

def _find_rightmost_colored_block(grid_np):
    """
    Finds the rightmost contiguous block of columns where each column
    consists of a single, non-background, non-gray color.
    
    Args:
        grid_np: numpy array representation of the input grid.

    Returns:
        A tuple (block_colors, min_col):
        - block_colors: A list of the colors in the block, ordered left-to-right.
        - min_col: The column index of the leftmost column in the block.
        Returns (None, -1) if no such block is found.
    """
    height, width = grid_np.shape
    block_colors = []
    min_col = -1
    max_col = -1

    # Iterate columns from right to left
    for c in range(width - 1, -1, -1):
        column = grid_np[:, c]
        unique_colors = np.unique(column)

        # Check if column is a single, valid (non-BG, non-Gray) color
        is_valid_column = (len(unique_colors) == 1 and 
                           unique_colors[0] != BG_COLOR and 
                           unique_colors[0] != GRAY_COLOR)

        if is_valid_column:
            # If this is the first valid column found (searching from right)
            if max_col == -1:
                max_col = c
                min_col = c
                block_colors.insert(0, unique_colors[0]) # Add color to start of list
            # If this column is directly left of the current block start
            elif c == min_col - 1:
                min_col = c # Extend block to the left
                block_colors.insert(0, unique_colors[0]) # Add color to start of list
            # If it's valid but not adjacent (gap found), means we finished the rightmost block
            else:
                break 
        # If column is invalid and we were previously tracking a block, stop.
        elif max_col != -1:
            break # We have found the complete rightmost block

    if not block_colors:
        return None, -1
    else:
        return block_colors, min_col

def _get_gray_line_height(grid_np):
    """
    Calculates the height of the contiguous gray segment starting at (0,0).
    
    Args:
        grid_np: numpy array representation of the input grid.

    Returns:
        Integer height of the gray segment. Defaults to 1 if cell (0,0) 
        is not gray or column 0 doesn't exist. Ensures return value is >= 1.
    """
    height, width = grid_np.shape
    # Check if grid has columns and if the top-left cell is gray
    if width == 0 or grid_np[0, 0] != GRAY_COLOR:
        return 1 # Default repetition factor

    rep_height = 0
    # Count contiguous gray cells down column 0
    for r in range(height):
        if grid_np[r, 0] == GRAY_COLOR:
            rep_height += 1
        else:
            break # Stop counting once a non-gray cell is encountered
            
    # Ensure repetition factor is at least 1 to avoid division by zero later
    return max(1, rep_height)


def transform(input_grid):
    """
    Applies the transformation rules to the input grid.
    
    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input to numpy array for efficient processing
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    
    # 5: Initialize output grid with background color
    output_np = np.full_like(input_np, BG_COLOR)

    # 1 & 2: Find the colored block and its properties
    block_colors, min_col = _find_rightmost_colored_block(input_np)

    # Handle case where no valid block is found
    if block_colors is None:
        # Return an empty grid (all background) as per initialization
        return output_np.tolist() 

    num_colors = len(block_colors)
    # Should not happen if block_colors is not None, but added safety check
    if num_colors == 0: 
         return output_np.tolist()

    # 3: Determine repetition factor from gray line height
    rep_factor = _get_gray_line_height(input_np)

    # 4: Calculate target column for the output line
    target_col = min_col - 1

    # Check if the calculated target column is valid (within grid bounds)
    if target_col < 0:
        # This scenario is not expected based on examples but handle defensively.
        # Return the empty grid if target calculation leads to invalid index.
        # print(f"Warning: Calculated target column {target_col} is out of bounds.") 
        return output_np.tolist()

    # 6: Populate the target column in the output grid
    for r in range(height):
        # Calculate the index into the block_colors list
        # Integer division gives the block index, modulo wraps around colors
        color_index = (r // rep_factor) % num_colors
        output_np[r, target_col] = block_colors[color_index]

    # 7 & 8: Handle the conditional copying of the gray line from input column 0
    # Check if column 0 exists and contains any gray pixels
    has_gray_col0 = width > 0 and np.any(input_np[:, 0] == GRAY_COLOR)

    # Copy column 0 only if it had gray AND the target column is NOT 3
    if has_gray_col0 and target_col != 3:
         # Ensure column 0 actually exists before trying to copy
         if width > 0: 
              output_np[:, 0] = input_np[:, 0]

    # 9: Return the final grid as a list of lists
    return output_np.tolist()