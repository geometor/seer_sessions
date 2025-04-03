import numpy as np
import collections

"""
Identify the single largest contiguous block of a non-white color in a 1D input array. 
Create an output array of the same size, initially filled with white (0). 
Copy only the pixels belonging to the largest identified block from the input to the output array at the same positions. 
All other pixels in the output remain white. If multiple blocks share the maximum length, the first one encountered is chosen.
"""

def find_contiguous_blocks(grid, target_color):
    """Finds all contiguous blocks of a specific color in a 1D grid."""
    blocks = []
    in_block = False
    start_index = -1
    for i, pixel in enumerate(grid):
        if pixel == target_color and not in_block:
            # Start of a new block
            in_block = True
            start_index = i
        elif pixel != target_color and in_block:
            # End of the current block
            in_block = False
            end_index = i # end index is exclusive
            blocks.append({'start': start_index, 'end': end_index, 'length': end_index - start_index, 'color': target_color})
            start_index = -1 # reset
    
    # Handle block ending at the very end of the grid
    if in_block:
        end_index = len(grid)
        blocks.append({'start': start_index, 'end': end_index, 'length': end_index - start_index, 'color': target_color})
        
    return blocks

def transform(input_grid):
    """
    Transforms the input grid by keeping only the largest contiguous block 
    of the non-white color and turning everything else white.
    
    Args:
        input_grid (list): A 1D list of integers representing pixel colors.

    Returns:
        list: The transformed 1D list of integers.
    """
    
    # Convert input to numpy array for easier handling if needed, though list operations are fine here
    # input_arr = np.array(input_grid)
    grid_len = len(input_grid)
    
    # Initialize output_grid with all white pixels (0)
    output_grid = [0] * grid_len

    # 1. Identify the non-white color C
    non_white_color = None
    for pixel in input_grid:
        if pixel != 0:
            non_white_color = pixel
            break
            
    # If no non-white color is found, return the all-white grid
    if non_white_color is None:
        return output_grid

    # 2. Find all contiguous blocks of the non-white color
    blocks = find_contiguous_blocks(input_grid, non_white_color)

    # 3. Find the largest block
    largest_block = None
    max_length = 0
    
    if not blocks: # No blocks of the non-white color found
      return output_grid

    for block in blocks:
        if block['length'] > max_length:
            max_length = block['length']
            largest_block = block
            
    # Check if a largest block was actually found (handles cases with only white pixels correctly via the initial check)
    if largest_block:
        # 4. Copy the largest block to the output grid
        start = largest_block['start']
        end = largest_block['end']
        output_grid[start:end] = input_grid[start:end]

    return output_grid