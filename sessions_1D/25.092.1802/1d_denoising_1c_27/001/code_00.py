import numpy as np
from collections import defaultdict

"""
Identifies contiguous blocks of non-background pixels in a 1D input grid. 
Calculates the size of each block.
Keeps only the block(s) with the largest size, changing all other non-background pixels to the background color (0).
The background color is assumed to be 0.
"""

def find_contiguous_blocks(arr_1d, target_color, background_color=0):
    """
    Finds contiguous blocks of a specific color in a 1D array.

    Args:
        arr_1d (np.array): The 1D input array.
        target_color (int): The color of the blocks to find.
        background_color (int): The color to ignore (usually 0).

    Returns:
        list: A list of tuples, where each tuple represents a block:
              (start_index, end_index, size). Returns empty list if no blocks found.
    """
    blocks = []
    start_index = -1
    for i, pixel in enumerate(arr_1d):
        if pixel == target_color and start_index == -1:
            # Start of a new block
            start_index = i
        elif pixel != target_color and start_index != -1:
            # End of the current block
            end_index = i - 1
            size = end_index - start_index + 1
            blocks.append((start_index, end_index, size))
            start_index = -1  # Reset for the next block

    # Check if a block extends to the end of the array
    if start_index != -1:
        end_index = len(arr_1d) - 1
        size = end_index - start_index + 1
        blocks.append((start_index, end_index, size))

    return blocks

def transform(input_grid):
    """
    Filters objects in a 1D grid based on size, keeping only the largest contiguous block(s).

    Args:
        input_grid (list): A list representing the 1D input grid.

    Returns:
        list: A list representing the 1D output grid with only the largest block(s) retained.
    """
    # Convert input list to numpy array for easier processing
    # Assuming input is always 1xN, so we take the first row if it's nested
    if isinstance(input_grid[0], list):
        input_arr = np.array(input_grid[0])
    else: # Assume it's already a flat list
        input_arr = np.array(input_grid)
        
    # Define background color
    background_color = 0
    
    # Find unique non-background colors present in the input
    unique_colors = np.unique(input_arr[input_arr != background_color])

    # If there are no non-background colors, return the input as is
    if len(unique_colors) == 0:
         # Ensure output format matches input format (list of list or flat list)
        if isinstance(input_grid[0], list):
             return input_grid
        else:
             return input_grid # Return the flat list

    # Assume the task focuses on the single non-background color present, as per examples
    # If multiple non-background colors could exist, the logic might need refinement.
    # For now, pick the first (and likely only) non-background color.
    primary_color = unique_colors[0]

    # Find all contiguous blocks of the primary color
    blocks = find_contiguous_blocks(input_arr, primary_color, background_color)

    # If no blocks are found (e.g., only background color), return the input
    if not blocks:
         # Ensure output format matches input format (list of list or flat list)
        if isinstance(input_grid[0], list):
             return input_grid
        else:
             return input_grid # Return the flat list

    # Find the maximum size among all blocks found
    max_size = 0
    for _, _, size in blocks:
        if size > max_size:
            max_size = size

    # Create the output grid, initialized with the background color
    output_arr = np.full_like(input_arr, background_color)

    # Iterate through the blocks again
    # Fill the output grid with pixels belonging to the largest block(s)
    for start_index, end_index, size in blocks:
        if size == max_size:
            output_arr[start_index : end_index + 1] = primary_color

    # Convert the numpy array back to the required list format
    # Match the original input format (list of list or flat list)
    if isinstance(input_grid[0], list):
        output_grid = [output_arr.tolist()]
    else:
        output_grid = output_arr.tolist()
        
    return output_grid