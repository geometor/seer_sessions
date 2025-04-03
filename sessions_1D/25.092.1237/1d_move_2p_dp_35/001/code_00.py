import numpy as np
from typing import List, Tuple

"""
Identify a contiguous horizontal block of non-background color and a single 'marker' pixel (red=2) 
to its right, separated by some background pixels. Shift the block rightwards so that it becomes 
immediately adjacent to the marker pixel, removing the background pixels that were originally 
between them. The relative order of the block and marker is preserved, and the marker's absolute 
position remains unchanged in the examples shown, but the logic derived places it relative to the 
shifted block. The background color is assumed to be white (0).
"""

def find_contiguous_block(arr: np.ndarray, background_color: int = 0) -> Tuple[int, int, int, int]:
    """
    Finds the first contiguous horizontal block of non-background color.
    Assumes input is 1D or effectively 1D (1xN or Nx1).

    Args:
        arr: The input numpy array (1D).
        background_color: The color considered as background.

    Returns:
        Tuple[int, int, int, int]: (color, start_index, end_index, length)
        Returns (-1, -1, -1, -1) if no block is found.
    """
    start_index = -1
    block_color = -1
    for i, pixel in enumerate(arr):
        if pixel != background_color:
            start_index = i
            block_color = pixel
            break

    if start_index == -1:
        return -1, -1, -1, -1 # No block found

    end_index = start_index
    for i in range(start_index + 1, len(arr)):
        if arr[i] == block_color:
            end_index = i
        else:
            break # End of the block

    length = end_index - start_index + 1
    return block_color, start_index, end_index, length

def find_marker_pixel(arr: np.ndarray, block_end_index: int, block_color: int, background_color: int = 0) -> Tuple[int, int]:
    """
    Finds the first pixel after the block that is not background or the block color.
    In this specific task, it's expected to be color 2 (red).

    Args:
        arr: The input numpy array (1D).
        block_end_index: The index where the contiguous block ends.
        block_color: The color of the contiguous block.
        background_color: The color considered as background.

    Returns:
        Tuple[int, int]: (marker_color, marker_index)
        Returns (-1, -1) if no marker is found after the block.
    """
    for i in range(block_end_index + 1, len(arr)):
        pixel = arr[i]
        if pixel != background_color and pixel != block_color:
            # In this specific task, we implicitly know the marker is color 2
            # but finding the *first* different pixel works for the examples.
            return pixel, i
    return -1, -1 # No marker found

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Shifts a colored block to be adjacent to a marker pixel, removing the background space between them.

    Args:
        input_grid: A 2D list representing the input grid. 
                      Expected to be 1xN for this specific task based on examples.

    Returns:
        A 2D list representing the transformed grid.
    """
    # Convert input to numpy array - assuming 1D layout as per examples
    # If input_grid is [[...]], take the first row.
    if isinstance(input_grid, list) and len(input_grid) == 1 and isinstance(input_grid[0], list):
         input_arr = np.array(input_grid[0], dtype=int)
         is_list_input = True # Flag to return list format if needed
         original_shape = (1, len(input_arr))
    elif isinstance(input_grid, np.ndarray):
         # Handle potential 2D numpy array input (1xN or Nx1)
         if input_grid.shape[0] == 1:
             input_arr = input_grid[0]
             original_shape = input_grid.shape
         elif input_grid.shape[1] == 1:
              input_arr = input_grid.flatten()
              original_shape = input_grid.shape # Store original shape if needed later
         else:
              # This specific task seems 1D, raise error or handle more complex cases if needed
              raise ValueError("Input grid format not recognized as 1D for this task")
         is_list_input = False
    else:
        raise TypeError("Input grid must be a list of lists or a numpy array.")


    background_color = 0

    # Find the contiguous block
    block_color, block_start_index, block_end_index, block_length = find_contiguous_block(input_arr, background_color)
    if block_color == -1:
        # If no block found, return input unchanged or handle error
        return input_grid # Or raise error

    # Find the marker pixel (assumed to be color 2 and after the block)
    # We search specifically for color 2 based on the pattern.
    marker_color = 2 
    marker_index = -1
    for i in range(block_end_index + 1, len(input_arr)):
         if input_arr[i] == marker_color:
              marker_index = i
              break
              
    # If marker isn't found (color 2), return input or handle error.
    if marker_index == -1:
         # Fallback: use the generic function if specific marker (2) wasn't found
         marker_color_found, marker_index_found = find_marker_pixel(input_arr, block_end_index, block_color, background_color)
         if marker_index_found == -1:
             return input_grid # No marker pixel found after block
         # Use the found marker if specific one (2) was absent
         marker_color = marker_color_found
         marker_index = marker_index_found


    # Calculate the gap size (number of background pixels between block end and marker)
    gap_size = 0
    for i in range(block_end_index + 1, marker_index):
        if input_arr[i] == background_color:
            gap_size += 1
        # If non-background found in gap, logic might be different, but examples show only background.

    # Alternative gap calculation based on indices:
    # gap_size = marker_index - block_end_index - 1 
    # This works if the space ONLY contains background color.

    # Initialize the output array with background color
    output_arr = np.full_like(input_arr, background_color)

    # Calculate the new position for the block
    new_block_start_index = block_start_index + gap_size
    new_block_end_index = block_end_index + gap_size # Inclusive index

    # Place the block in the output array
    output_arr[new_block_start_index : new_block_end_index + 1] = block_color

    # Place the marker pixel immediately after the shifted block
    new_marker_index = new_block_end_index + 1
    # Ensure marker index is within bounds
    if new_marker_index < len(output_arr):
        output_arr[new_marker_index] = marker_color

    # Reshape back to original format if necessary and convert back to list if input was list
    if is_list_input:
        # Return as list of lists [[...]]
        return [output_arr.tolist()]
    else:
        # Return as numpy array with original shape
        return output_arr.reshape(original_shape)
