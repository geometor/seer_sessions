import numpy as np
from typing import List, Tuple, Optional, Dict, Any

"""
Transforms a 1D grid by finding a specific pattern and rearranging its components.
The pattern consists of a single 'mover' pixel (color 1-9) immediately adjacent
to a contiguous 'block' of two or more pixels (all having the same color 1-9,
different from the mover's color). The transformation swaps the relative position
of the mover pixel and the block within the grid segment defined by the pattern.
All other pixels in the grid, including background pixels (color 0), remain unchanged.
"""

def find_non_background_pattern(grid_1d: np.ndarray) -> Optional[Dict[str, Any]]:
    """
    Finds the first occurrence of a non-background mover pixel adjacent
    to a non-background block (>=2 pixels) of a different, uniform color.

    Args:
        grid_1d: A 1D numpy array representing the grid row.

    Returns:
        A dictionary containing pattern details (mover_color, block_sequence,
        start_index, end_index, mover_is_left) if found, otherwise None.
    """
    n = len(grid_1d)
    if n < 3: # Need at least 3 elements for mover + block(len>=2)
        return None

    # Iterate through potential boundaries between pattern elements
    for i in range(n - 1):
        c1 = grid_1d[i]
        c2 = grid_1d[i+1]

        # Potential boundary must involve two different non-zero colors
        if c1 != 0 and c2 != 0 and c1 != c2:

            # CASE 1: c1 is potential Mover (at i), c2 starts potential Block (at i+1)
            # Check if c1 is single (not preceded by same color)
            is_c1_single = (i == 0 or grid_1d[i-1] != c1)
            # Check if c2 starts a block of length >= 2
            is_c2_block_start = (i + 2 < n and grid_1d[i+2] == c2)

            if is_c1_single and is_c2_block_start:
                # Find the end of the block starting at i+1
                block_color = c2
                k = i + 1 # Start of block
                while k + 1 < n and grid_1d[k+1] == block_color:
                    k += 1
                # End of block is k
                # Verify block is properly terminated (or hits grid end)
                is_block_terminated = (k + 1 == n or grid_1d[k+1] != block_color)

                if is_block_terminated:
                    mover_color = c1
                    block_sequence = list(grid_1d[i+1 : k+1])
                    start_index = i
                    end_index = k
                    return {
                        "mover_color": mover_color,
                        "block_sequence": block_sequence,
                        "start_index": start_index,
                        "end_index": end_index,
                        "mover_is_left": True
                    }

            # CASE 2: c1 ends potential Block (at i), c2 is potential Mover (at i+1)
            # Check if c2 is single (not followed by same color)
            is_c2_single = (i + 1 == n - 1 or grid_1d[i+2] != c2)
            # Check if c1 ends a block of length >= 2
            is_c1_block_end = (i > 0 and grid_1d[i-1] == c1)

            if is_c2_single and is_c1_block_end:
                 # Find the start of the block ending at i
                 block_color = c1
                 j = i # End of block
                 while j - 1 >= 0 and grid_1d[j-1] == block_color:
                     j -= 1
                 # Start of block is j
                 # Verify block is properly terminated (or hits grid start)
                 is_block_terminated = (j == 0 or grid_1d[j-1] != block_color)

                 if is_block_terminated:
                     mover_color = c2
                     block_sequence = list(grid_1d[j : i+1])
                     start_index = j
                     end_index = i + 1 # Pattern includes the mover c2
                     return {
                         "mover_color": mover_color,
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
    # --- Input Handling ---
    # Ensure input is a numpy array
    if not isinstance(input_grid, np.ndarray):
        input_grid = np.array(input_grid, dtype=int)

    # Handle potential 2D shape (1, N) -> convert to 1D for processing
    original_ndim = input_grid.ndim
    if original_ndim == 2:
        if input_grid.shape[0] == 1:
            grid_1d = input_grid[0]
        elif input_grid.shape[1] == 1: # Handle (N, 1) case if needed, though examples are rows
             grid_1d = input_grid.flatten()
             original_ndim = 1 # Treat as 1D for output reshaping consistency
        else:
             raise ValueError(f"Input grid must be 1D or 2D with one dimension = 1. Got shape: {input_grid.shape}")
    elif original_ndim == 1:
        grid_1d = input_grid
    else:
        raise ValueError(f"Input grid must be 1D or 2D. Got shape: {input_grid.shape}")

    # --- Initialization ---
    # Initialize output grid as a copy of the 1D working grid
    output_grid_1d = grid_1d.copy()

    # --- Pattern Finding ---
    # Find the specific mover-block pattern, ignoring background pixels in the core components
    pattern_info = find_non_background_pattern(grid_1d)

    # --- Transformation Application ---
    # If the pattern is found, apply the swap transformation
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

        # Replace the original pattern segment in the output grid with the new sequence
        # Ensure length matches (should always be true if find_pattern is correct)
        if len(new_sequence) == (end - start + 1):
             output_grid_1d[start : end + 1] = new_sequence
        else:
             # This case indicates a potential flaw in find_non_background_pattern logic
             print(f"Warning: Length mismatch during replacement. Indices [{start}:{end+1}], Expected len {end-start+1}, New len {len(new_sequence)}. Pattern: {pattern_info}")
             # Return unmodified copy in case of unexpected error to avoid crashing
             pass # Output grid remains the initial copy

    # --- Output Formatting ---
    # Reshape back to the original input format (1D or 2D) if necessary
    if original_ndim == 2 and input_grid.shape[0] == 1:
        return output_grid_1d.reshape(1, -1)
    else: # Handles original 1D or (N, 1) cases converted earlier
        return output_grid_1d