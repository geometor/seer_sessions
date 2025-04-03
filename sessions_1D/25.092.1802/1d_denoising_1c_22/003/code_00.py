import numpy as np
from typing import List, Dict, Optional, Tuple, Union

"""
Identify the single longest contiguous horizontal segment of the non-background 
color within the flattened representation of the input grid. The output grid 
has the same dimensions as the input, but contains only this longest segment, 
placed according to its position in the flattened sequence, with all other cells 
set to the background color (0).
"""

def find_contiguous_blocks(arr: np.ndarray, color: int) -> List[Dict[str, int]]:
    """
    Finds all contiguous blocks of a specified color in a 1D array.

    Args:
        arr: The 1D numpy array to search within.
        color: The color value to search for.

    Returns:
        A list of dictionaries, where each dictionary represents a block 
        and contains 'start', 'end', and 'length' keys.
    """
    blocks = []
    start_index = -1
    n = len(arr)
    for i, pixel in enumerate(arr):
        if pixel == color and start_index == -1:
            # Start of a new block
            start_index = i
        elif pixel != color and start_index != -1:
            # End of the current block
            end_index = i - 1
            length = end_index - start_index + 1
            blocks.append({"start": start_index, "end": end_index, "length": length})
            start_index = -1 # Reset for the next block

    # Check if the array ends with a block
    if start_index != -1:
        end_index = n - 1
        length = end_index - start_index + 1
        blocks.append({"start": start_index, "end": end_index, "length": length})

    return blocks

def find_largest_block(blocks: List[Dict[str, int]]) -> Optional[Dict[str, int]]:
    """
    Finds the block with the maximum length from a list of blocks.
    If there's a tie, returns the first one encountered.

    Args:
        blocks: A list of block dictionaries.

    Returns:
        The dictionary representing the largest block, or None if the list is empty.
    """
    if not blocks:
        return None
    
    largest = blocks[0]
    # Start checking from the second block
    for block in blocks[1:]:
        # Only update if the current block is strictly larger
        # This implicitly handles ties by keeping the first largest found
        if block["length"] > largest["length"]:
            largest = block
            
    return largest

def get_colors(arr: np.ndarray) -> Tuple[int, Optional[int]]:
    """
    Identifies the background (0) and primary (non-zero) colors in a 1D array.
    Assumes only one non-zero color exists.

    Args:
        arr: The 1D numpy array.

    Returns:
        A tuple containing the background color (always 0) and the primary color 
        (or None if only background color is present).
    """
    background_color = 0
    primary_color = None
    unique_colors = np.unique(arr)
    for color in unique_colors:
        if color != background_color:
            primary_color = int(color) # Ensure it's a standard python int
            break # Assume only one non-background color
    return background_color, primary_color


def transform(input_grid: Union[List[List[int]], np.ndarray]) -> Union[List[List[int]], np.ndarray]:
    """
    Transforms the input grid by isolating the longest contiguous segment 
    of the primary color found in the flattened version of the grid.

    Args:
        input_grid: A 2D list or numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed grid.
    """
    # Ensure input is a numpy array
    input_array = np.array(input_grid, dtype=int)
    
    # 1. Record the original dimensions
    original_shape = input_array.shape
    
    # 2. Flatten the 2D input grid into a 1D array
    flat_array = input_array.flatten()
    flat_size = flat_array.size

    # 4. Identify the background and primary colors
    background_color, primary_color = get_colors(flat_array)

    # Handle case where input is all background color
    if primary_color is None:
        # 3. Initialize output with background color and return if no primary color
        return np.full(original_shape, background_color, dtype=int)

    # 5. Find all contiguous segments of the primary color in the flattened array
    blocks = find_contiguous_blocks(flat_array, primary_color)

    # 6. Find the longest segment (block)
    largest_block = find_largest_block(blocks)

    # 3. Initialize a 1D output array with the background color
    output_flat = np.full(flat_size, background_color, dtype=int)

    # 7. If a largest segment was found, place it in the 1D output array
    if largest_block:
        start = largest_block["start"]
        end = largest_block["end"]
        output_flat[start : end + 1] = primary_color

    # 8. Reshape the 1D output array back into the original dimensions
    output_grid = output_flat.reshape(original_shape)

    # 9. Return the resulting 2D output grid
    return output_grid