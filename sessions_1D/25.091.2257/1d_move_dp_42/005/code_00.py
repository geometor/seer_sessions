import numpy as np
from typing import List, Tuple, Optional

"""
Shift the first contiguous block of non-background (non-zero) pixels found before a magenta marker (color 6) rightwards, placing it immediately before the marker. The background pixels (color 0) originally located between this block and the marker are moved to fill the space vacated by the block at its original starting position. Pixels before the block's original start and after the marker remain in their relative positions. If no marker or no payload block before the marker is found, the input remains unchanged.
"""

def find_marker(input_array: np.ndarray, marker_color: int = 6) -> Optional[int]:
    """
    Finds the index of the first occurrence of the marker pixel.

    Args:
        input_array: The numpy array to search within.
        marker_color: The integer value of the marker pixel.

    Returns:
        The index of the marker pixel, or None if not found.
    """
    marker_indices = np.where(input_array == marker_color)[0]
    if len(marker_indices) == 0:
        return None
    return marker_indices[0] # Return the index of the first occurrence

def find_first_payload_block(input_array: np.ndarray, end_scan_index: int) -> Tuple[Optional[int], Optional[int], Optional[np.ndarray]]:
    """
    Finds the first contiguous block of non-zero pixels before a given index.

    Args:
        input_array: The numpy array to search within.
        end_scan_index: The index before which to search (exclusive).

    Returns:
        A tuple containing:
        - start_index (int): The starting index of the block, or None if not found.
        - end_index (int): The ending index (inclusive) of the block, or None if not found.
        - payload_pixels (np.ndarray): The pixels of the block, or None if not found.
    """
    start_index = None
    end_index = None
    payload_pixels_list = []
    in_block = False

    # Iterate through the array up to the specified end index
    for i in range(end_scan_index):
        pixel = input_array[i]
        # Start of a new block (non-zero pixel found when not already in a block)
        if not in_block and pixel != 0:
            in_block = True
            start_index = i
            payload_pixels_list.append(pixel)
        # Continue the current block (non-zero pixel found while in a block)
        elif in_block and pixel != 0:
            payload_pixels_list.append(pixel)
        # End of the current block (zero pixel found while in a block)
        elif in_block and pixel == 0:
            end_index = i - 1
            break # Found the *first* block and its end, stop searching

    # If loop finished while still in a block, the block ends right before end_scan_index
    if in_block and end_index is None:
        end_index = end_scan_index - 1

    # If no block was ever started
    if start_index is None:
        return None, None, None
    else:
        # Convert collected pixels to numpy array
        payload_pixels_array = np.array(payload_pixels_list, dtype=input_array.dtype)
        return start_index, end_index, payload_pixels_array


def transform(input_grid: List[int]) -> List[int]:
    """
    Transforms the input list by identifying marker, payload, and gap, then rearranging them.

    Args:
        input_grid: A list of integers representing pixel colors.

    Returns:
        A list of integers representing the transformed pixel colors.
    """
    # Convert input list to numpy array for efficient processing
    input_array = np.array(input_grid)
    
    # 1. Locate the magenta marker (6)
    marker_index = find_marker(input_array, 6)
    
    # If marker not found, return original grid unchanged
    if marker_index is None:
        return input_grid 

    # 2. Find the first payload block (non-zero pixels before the marker)
    payload_start, payload_end, payload_pixels = find_first_payload_block(input_array, marker_index)

    # Handle case where no payload block is found before the marker
    if payload_start is None:
        # No block to move, return original array unchanged
        return input_grid

    # 3. Identify the prefix (pixels before the payload block)
    prefix_pixels = input_array[:payload_start]

    # 4. Identify the gap (pixels between payload end and marker)
    # These should typically be background (0) pixels based on the examples
    gap_pixels = input_array[payload_end + 1 : marker_index]

    # 5. Identify the suffix (pixels after the marker)
    suffix_pixels = input_array[marker_index + 1:]
    
    # 6. Get the marker pixel itself as a numpy array
    marker_pixel = input_array[marker_index:marker_index+1] # Slice to keep it as an array

    # 7. Construct the output array by concatenating the identified parts
    # The order defines the transformation: prefix, gap, payload, marker, suffix
    output_array = np.concatenate((
        prefix_pixels,      # Part before the payload
        gap_pixels,         # Part that was between payload and marker
        payload_pixels,     # The payload block itself
        marker_pixel,       # The marker
        suffix_pixels       # Part after the marker
    ))

    # 8. Convert the result back to a list for the required return type
    return output_array.tolist()