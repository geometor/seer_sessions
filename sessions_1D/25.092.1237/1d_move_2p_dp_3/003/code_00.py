"""
Identifies a specific row in a 2D input grid containing a characteristic pattern: a contiguous sequence of a single non-white(0), non-green(3) color (the 'object sequence'), followed by one or more white(0) pixels (the 'gap'), followed by a single green(3) pixel (the 'barrier').
Transforms this target row by swapping the positions of the 'object sequence' and the 'gap'. The object sequence moves immediately to the left of the barrier, and the gap moves to the position originally occupied by the start of the object sequence relative to the prefix.
All other rows in the grid remain unchanged. If no row matches the pattern, the original grid is returned.
"""

import numpy as np
from typing import Tuple, Optional

def find_object_sequence_1d(row: np.ndarray) -> Optional[Tuple[int, int, int]]:
    """
    Finds the start index, end index, and color of the first contiguous sequence
    of identical pixels in a 1D array (row) that are not white (0) or green (3).

    Args:
        row: A 1D numpy array representing a row of the grid.

    Returns:
        A tuple (start_index, end_index, color) if found, otherwise None.
    """
    start_index = -1
    current_color = -1
    for i, pixel in enumerate(row):
        if pixel != 0 and pixel != 3: # Potential object pixel
            if start_index == -1: # Start of a new potential sequence
                start_index = i
                current_color = pixel
            elif pixel != current_color: # End of sequence due to different non-0/3 color
                # Found a complete sequence before this different color started
                return start_index, i - 1, current_color
        elif start_index != -1: # Sequence ends because we hit 0 or 3
            # Found the end of the sequence
            return start_index, i - 1, current_color
            
    # Check if the sequence runs to the end of the row
    if start_index != -1:
        return start_index, len(row) - 1, current_color
        
    return None # No suitable object sequence found

def find_barrier_1d(row: np.ndarray, search_start_index: int = 0) -> Optional[int]:
    """
    Finds the index of the first green (3) pixel in a 1D array (row),
    starting the search from a given index.

    Args:
        row: A 1D numpy array representing a row of the grid.
        search_start_index: The index from which to start searching for the barrier.

    Returns:
        The index of the green pixel if found, otherwise None.
    """
    try:
        # Find all occurrences of '3' in the specified slice
        relative_indices = np.where(row[search_start_index:] == 3)[0]
        if len(relative_indices) > 0:
            # Return the absolute index in the original row
            return search_start_index + relative_indices[0]
        else:
            return None
    except IndexError: # Should not happen with numpy where but good practice
         return None


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the object/gap swap transformation to the target row within the input grid.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed grid.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    target_row_found = False

    # Iterate through each row to find the target row
    for r in range(rows):
        current_row = input_grid[r, :]

        # 1. Find the object sequence in the current row
        object_info = find_object_sequence_1d(current_row)
        if not object_info:
            continue # No object sequence in this row

        obj_start, obj_end, obj_color = object_info

        # 2. Find the barrier (green pixel) after the object sequence
        barrier_index = find_barrier_1d(current_row, search_start_index=obj_end + 1)
        if barrier_index is None:
            continue # No barrier found after the object in this row

        # 3. Define and validate the gap
        gap_start_index = obj_end + 1
        gap_end_index = barrier_index # gap is up to, but not including, the barrier

        # Ensure gap exists (barrier is not immediately adjacent to object)
        if gap_start_index >= gap_end_index:
             continue # No gap found between object and barrier

        gap_seq = current_row[gap_start_index:gap_end_index]

        # Check if the gap contains only white (0) pixels
        if not np.all(gap_seq == 0):
            continue # Gap contains non-white pixels, this is not the target row

        # If we reach here, we've found the target row and confirmed the pattern
        target_row_found = True

        # 4. Extract segments from the target row
        prefix = current_row[:obj_start]
        object_seq = current_row[obj_start : obj_end + 1]
        # gap_seq is already extracted
        barrier_pixel = np.array([current_row[barrier_index]]) # Keep as array for concatenation
        suffix = current_row[barrier_index + 1 :]

        # 5. Construct the modified row by rearranging segments
        # Order: prefix, gap, object, barrier, suffix
        modified_row = np.concatenate((prefix, gap_seq, object_seq, barrier_pixel, suffix))

        # 6. Update the output grid with the modified row
        output_grid[r, :] = modified_row

        # Assume only one target row per grid based on examples
        break 

    # Return the modified grid (or the original copy if no target row was found)
    return output_grid