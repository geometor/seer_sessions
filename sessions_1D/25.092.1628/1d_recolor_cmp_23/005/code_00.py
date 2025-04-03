import numpy as np
from typing import List, Tuple, Dict

"""
Transforms a 1D sequence (potentially represented as a 1xN 2D array) of pixels.
The transformation identifies all contiguous horizontal blocks of azure (8) pixels.
It then filters these blocks to find those immediately surrounded by white (0) pixels on both sides.
Among these surrounded blocks, it determines the maximum length.
Finally, it changes the color of the pixels within *all* such blocks 
that have this maximum length to orange (7). All other pixels retain their original color.
The output grid retains the original dimensions.
"""

def find_contiguous_blocks(sequence: np.ndarray, target_color: int) -> List[Dict[str, int]]:
    """
    Identifies contiguous blocks of a specific color in a 1D numpy array.

    Args:
        sequence: A 1D numpy array of integers.
        target_color: The integer color value to find blocks of.

    Returns:
        A list of dictionaries, where each dictionary represents a block
        and contains 'start', 'end', and 'length' keys.
    """
    blocks = []
    n = len(sequence)
    i = 0
    while i < n:
        if sequence[i] == target_color:
            start = i
            # Find the end of the block
            while i < n and sequence[i] == target_color:
                i += 1
            end = i - 1
            length = end - start + 1
            blocks.append({'start': start, 'end': end, 'length': length})
        else:
            # Move to the next pixel if not the target color
            i += 1
    return blocks

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A numpy array (potentially 2D with shape (1, N)) representing the input grid.

    Returns:
        A numpy array representing the transformed grid, with the same dimensions as the input.
    """
    # 1. Ensure we are working with a 1D sequence for logic
    # Handle potential 2D input (e.g., shape (1, N))
    if input_grid.ndim == 2:
        if input_grid.shape[0] != 1:
             # This specific problem seems to deal with 1xN grids
             raise ValueError("Input grid has more than one row, logic unclear for this case.")
        sequence = input_grid[0]
    elif input_grid.ndim == 1:
        sequence = input_grid
    else:
        raise ValueError("Input grid must be 1D or 2D.")

    # Initialize output_sequence as a copy of the input sequence
    output_sequence = sequence.copy()
    n = len(sequence)

    # 2. Identify all contiguous blocks of azure (8)
    azure_blocks = find_contiguous_blocks(sequence, 8)

    # 3. Filter azure blocks to find candidate blocks (surrounded by white 0)
    candidate_blocks = []
    for block in azure_blocks:
        start = block['start']
        end = block['end']

        # Check left boundary: must exist and be white (0)
        is_left_surrounded = (start > 0 and sequence[start - 1] == 0)

        # Check right boundary: must exist and be white (0)
        is_right_surrounded = (end < n - 1 and sequence[end + 1] == 0)

        if is_left_surrounded and is_right_surrounded:
            candidate_blocks.append(block) # Already ordered by start index

    # 4. If no candidate blocks are found, return the original grid (in original shape)
    if not candidate_blocks:
        # Reshape back if needed before returning
        if input_grid.ndim == 2:
             return output_sequence.reshape(input_grid.shape)
        else:
             return output_sequence

    # 5. Determine the maximum length among the candidate blocks
    max_length = 0
    for block in candidate_blocks:
        if block['length'] > max_length:
            max_length = block['length']
            
    # If max_length remained 0 (e.g., only blocks of length 0 possible, which shouldn't happen here),
    # it means no valid positive length candidates, so return original
    if max_length == 0:
        if input_grid.ndim == 2:
             return output_sequence.reshape(input_grid.shape)
        else:
             return output_sequence

    # 6. Iterate through *all* candidate blocks again
    # 7. Change color to orange (7) for *all* candidate blocks with the maximum length
    for block in candidate_blocks:
        if block['length'] == max_length:
            start = block['start']
            end = block['end']
            # Change the color of pixels within this block's range
            for i in range(start, end + 1):
                output_sequence[i] = 7
            # Do *not* break here, continue checking other candidates

    # 8. Reshape the output sequence back to the original input grid shape and return
    if input_grid.ndim == 2:
        return output_sequence.reshape(input_grid.shape)
    else:
        return output_sequence