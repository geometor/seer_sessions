import numpy as np
from typing import List, Tuple, Optional, Dict, Any

"""
Identifies a pattern where a single 'mover' pixel is adjacent to a
contiguous block (>= 2 pixels) of a different color in a 1D grid.
The transformation swaps the relative position of the mover pixel and
the block. If the mover is initially to the left of the block, it moves
to the right, and vice-versa. The rest of the grid remains unchanged.
"""

def find_pattern(grid_1d: np.ndarray) -> Optional[Dict[str, Any]]:
    """
    Finds the first occurrence of a mover pixel adjacent to a block (>=2 pixels)
    of a different, uniform color.

    Args:
        grid_1d: A 1D numpy array representing the grid row.

    Returns:
        A dictionary containing pattern details (mover_color, block_sequence,
        start_index, end_index, mover_is_left) if found, otherwise None.
    """
    n = len(grid_1d)
    if n < 3: # Need at least 3 elements for mover + block(len>=2)
        return None

    # Iterate through potential boundaries between elements
    for i in range(n - 1):
        left_val = grid_1d[i]
        right_val = grid_1d[i+1]

        # Potential boundary found if colors are different
        if left_val != right_val:

            # Check Case 1: Mover (left_val at i) + Block (starting at i+1)
            # The block must have length >= 2
            if i + 2 < n and grid_1d[i+1] == grid_1d[i+2]:
                block_color = grid_1d[i+1]
                # Find the end of the block
                k = i + 1
                while k + 1 < n and grid_1d[k+1] == block_color:
                    k += 1
                # Block length is k - (i+1) + 1 = k - i
                block_len = k - i
                # No need to check block_len >= 2 again due to initial check

                mover_color = left_val
                start_index = i
                end_index = k
                block_sequence = list(grid_1d[i+1 : k+1])
                return {
                    "mover_color": mover_color,
                    "block_sequence": block_sequence,
                    "start_index": start_index,
                    "end_index": end_index,
                    "mover_is_left": True
                }

            # Check Case 2: Block (ending at i) + Mover (right_val at i+1)
            # The block must have length >= 2
            if i > 0 and grid_1d[i] == grid_1d[i-1]:
                 block_color = grid_1d[i]
                 # Find the start of the block
                 j = i
                 while j - 1 >= 0 and grid_1d[j-1] == block_color:
                     j -= 1
                 # Block length is i - j + 1
                 block_len = i - j + 1
                 # Need to confirm block length >= 2
                 if block_len >= 2:
                     mover_color = right_val # The element at i+1 is the mover
                     start_index = j
                     end_index = i + 1 # Pattern includes the mover at i+1
                     block_sequence = list(grid_1d[j : i+1])
                     return {
                         "mover_color": mover_color,
                         "block_sequence": block_sequence,
                         "start_index": start_index,
                         "end_index": end_index,
                         "mover_is_left": False
                    }
    return None # No pattern found


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A numpy array representing the input grid.
                    Expected to be 1D or 2D with a single row.

    Returns:
        A numpy array representing the transformed grid.
    """
    # Ensure input is a numpy array and handle potential 2D shape (1, N)
    if not isinstance(input_grid, np.ndarray):
        input_grid = np.array(input_grid)

    original_ndim = input_grid.ndim
    if original_ndim == 2 and input_grid.shape[0] == 1:
        grid_1d = input_grid[0]
    elif original_ndim == 1:
        grid_1d = input_grid
    else:
         raise ValueError(f"Input grid must be 1D or a 2D array with a single row. Got shape: {input_grid.shape}")

    # Initialize output grid as a copy
    output_grid_1d = grid_1d.copy()

    # Find the mover and block pattern
    pattern_info = find_pattern(grid_1d)

    # If a pattern is found, apply the transformation
    if pattern_info:
        mover_color = pattern_info["mover_color"]
        block_sequence = pattern_info["block_sequence"]
        start = pattern_info["start_index"]
        end = pattern_info["end_index"]
        mover_is_left = pattern_info["mover_is_left"]

        # Construct the new sequence by swapping mover and block
        if mover_is_left:
            # New sequence: block + mover
            new_sequence = block_sequence + [mover_color]
        else:
            # New sequence: mover + block
            new_sequence = [mover_color] + block_sequence

        # Verify lengths before replacement (should always match if find_pattern is correct)
        expected_len = end - start + 1
        if len(new_sequence) == expected_len:
            # Replace the original pattern segment with the new sequence in the output grid
            output_grid_1d[start : end + 1] = new_sequence
        else:
            # Log an error if lengths mismatch - indicates a logic flaw
            print(f"Error: Length mismatch during replacement. Original length: {expected_len}, New length: {len(new_sequence)}")
            # Return the unmodified grid copy in case of error
            if original_ndim == 2:
                return output_grid_1d.reshape(1, -1)
            else:
                return output_grid_1d


    # Reshape back to original format if necessary (e.g., 2D with 1 row)
    if original_ndim == 2:
        return output_grid_1d.reshape(1, -1)
    else:
        return output_grid_1d
