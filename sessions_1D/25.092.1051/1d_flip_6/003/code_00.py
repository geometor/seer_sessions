import numpy as np
from typing import List, Tuple, Optional, Dict, Any

"""
Transforms a 1D grid by identifying a unique pattern consisting of a single 'mover' pixel adjacent to a contiguous block (length >= 2) of pixels of a different, uniform color. The transformation swaps the relative position of the mover pixel and the block within the grid segment defined by the pattern. Pixels outside this segment remain unchanged.
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

    # Iterate through potential start positions of the pattern
    for i in range(n - 1):
        # Case 1: Potential Mover at grid_1d[i], Potential Block starts at grid_1d[i+1]
        mover_cand_color = grid_1d[i]
        block_cand_start_color = grid_1d[i+1]

        # Check if colors are different and if a block of length >= 2 starts at i+1
        if mover_cand_color != block_cand_start_color and i + 2 < n and grid_1d[i+1] == grid_1d[i+2]:
            # Verify mover candidate is truly single (check left boundary or neighbor)
            if i == 0 or grid_1d[i-1] != mover_cand_color:
                block_color = block_cand_start_color
                # Find the end of the block
                k = i + 1
                while k + 1 < n and grid_1d[k+1] == block_color:
                    k += 1
                # Check if the element after the block is different (ensures block ends here)
                # or if we are at the end of the grid
                if k + 1 == n or grid_1d[k+1] != block_color:
                    block_sequence = list(grid_1d[i+1 : k+1])
                    start_index = i
                    end_index = k
                    return {
                        "mover_color": mover_cand_color,
                        "block_sequence": block_sequence,
                        "start_index": start_index,
                        "end_index": end_index,
                        "mover_is_left": True
                    }

        # Case 2: Potential Block ends at grid_1d[i], Potential Mover at grid_1d[i+1]
        mover_cand_color = grid_1d[i+1]
        block_cand_end_color = grid_1d[i]

        # Check if colors are different and if a block of length >= 2 ends at i
        if mover_cand_color != block_cand_end_color and i > 0 and grid_1d[i] == grid_1d[i-1]:
            # Verify mover candidate is truly single (check right boundary or neighbor)
            if i + 1 == n - 1 or grid_1d[i+2] != mover_cand_color:
                block_color = block_cand_end_color
                # Find the start of the block
                j = i
                while j - 1 >= 0 and grid_1d[j-1] == block_color:
                    j -= 1
                # Check if the element before the block is different (ensures block starts here)
                # or if we are at the start of the grid
                if j == 0 or grid_1d[j-1] != block_color:
                    block_sequence = list(grid_1d[j : i+1])
                    start_index = j
                    end_index = i + 1
                    return {
                        "mover_color": mover_cand_color,
                        "block_sequence": block_sequence,
                        "start_index": start_index,
                        "end_index": end_index,
                        "mover_is_left": False
                    }

    return None # No valid pattern found


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

    # Initialize output grid as a copy of the input
    output_grid_1d = grid_1d.copy()

    # Find the specific mover-block pattern
    pattern_info = find_pattern(grid_1d)

    # If the pattern is found, apply the transformation
    if pattern_info:
        # Extract pattern details
        mover_color = pattern_info["mover_color"]
        block_sequence = pattern_info["block_sequence"]
        start = pattern_info["start_index"]
        end = pattern_info["end_index"]
        mover_is_left = pattern_info["mover_is_left"]

        # Construct the new sequence by swapping the mover and block
        if mover_is_left:
            # New sequence: block + mover
            new_sequence = block_sequence + [mover_color]
        else:
            # New sequence: mover + block
            new_sequence = [mover_color] + block_sequence

        # Verify lengths before replacement (as a safeguard)
        expected_len = end - start + 1
        if len(new_sequence) == expected_len:
            # Replace the original pattern segment in the output grid
            output_grid_1d[start : end + 1] = new_sequence
        else:
            # This case should ideally not happen if find_pattern is correct
            print(f"Warning: Length mismatch during replacement. Original: {expected_len}, New: {len(new_sequence)}. Pattern: {pattern_info}")
            # Return unmodified copy in case of unexpected error
            if original_ndim == 2:
                return output_grid_1d.reshape(1, -1)
            else:
                return output_grid_1d

    # If no pattern was found, output_grid_1d remains an unchanged copy

    # Reshape back to the original input format (1D or 2D)
    if original_ndim == 2:
        return output_grid_1d.reshape(1, -1)
    else:
        return output_grid_1d