import numpy as np

def transform(input_grid):
    """
    Identifies a pattern of a single 'mover' pixel followed by a contiguous 'block'
    of pixels (both non-background) within a 1D row. Swaps the position of the
    mover pixel and the entire block, placing the block first and the mover
    immediately after it. Background pixels remain unchanged.
    """

    # -- Input Handling --
    # Determine if input is numpy array or list, and if it represents a 1xN grid or a 1D array/list
    is_numpy = isinstance(input_grid, np.ndarray)
    is_list = isinstance(input_grid, list)
    is_2d_input = False
    row = None

    if is_numpy:
        if input_grid.ndim == 2 and input_grid.shape[0] == 1:
            row = input_grid[0].tolist()
            is_2d_input = True
        elif input_grid.ndim == 1:
            row = input_grid.tolist()
            is_2d_input = False
        else:
            # Handle invalid numpy dimensions - return unchanged for robustness
            return input_grid
    elif is_list:
        if len(input_grid) == 1 and isinstance(input_grid[0], list):
            # Check if the inner list contains only integers
            if all(isinstance(x, int) for x in input_grid[0]):
                 row = input_grid[0]
                 is_2d_input = True
            else:
                 # Handle invalid inner list content - return unchanged
                 return input_grid
        elif all(isinstance(x, int) for x in input_grid):
            row = input_grid
            is_2d_input = False
        else:
            # Handle invalid list structure - return unchanged
            return input_grid
    else:
        # Handle non-list/numpy input - return unchanged
        return input_grid

    # If row could not be determined (e.g., empty list input)
    if row is None:
        return input_grid # Return original input

    # -- Core Logic --
    # Initialize output as a copy of the input row
    output_row = list(row)

    # Find the mover and block
    mover_index = -1
    mover_color = -1
    block_start_index = -1
    block_end_index = -1 # exclusive index (one position after the last block pixel)
    block_color = -1

    for i in range(len(row)):
        # Find the first non-background pixel (the mover)
        if row[i] != 0 and mover_index == -1:
            mover_index = i
            mover_color = row[i]

            # Look for the block starting immediately after the mover
            if i + 1 < len(row) and row[i+1] != 0:
                block_start_index = i + 1
                block_color = row[block_start_index]
                block_end_index = block_start_index + 1 # Initialize end index

                # Extend the block end index as long as the color matches
                for j in range(block_start_index + 1, len(row)):
                    if row[j] == block_color:
                        block_end_index = j + 1
                    else:
                        # Block ends either due to different color or background
                        break
                # Found the full pattern (mover + block), stop searching the row
                break
            else:
                # Found a mover but no block follows (either end of row or background pixel)
                # According to examples, a block always follows.
                # If this happens, the pattern is not matched as expected.
                # We break here; subsequent check will handle the non-match.
                break

    # Perform the transformation only if the expected pattern was found
    if mover_index != -1 and block_start_index != -1 and block_color != -1:
        block_length = block_end_index - block_start_index

        # Check if the combined length exceeds the row boundary (shouldn't happen with valid ARC data)
        if mover_index + block_length < len(output_row):

            # Write the block into the output starting at the mover's original position
            for i in range(block_length):
                output_row[mover_index + i] = block_color

            # Write the mover pixel into the output right after the newly placed block
            output_row[mover_index + block_length] = mover_color
        else:
            # Pattern found but placement would exceed bounds - indicates unexpected input.
            # Return unchanged row in this edge case.
             pass # output_row remains a copy of row

    # Else: pattern (mover immediately followed by block) was not found, output_row remains unchanged copy.

    # -- Output Formatting --
    # Return the result in the original format (list/numpy, 1D/2D)
    if is_numpy:
        if is_2d_input:
            return np.array([output_row])
        else: # 1D numpy input
            return np.array(output_row)
    elif is_list:
        if is_2d_input:
            return [output_row]
        else: # flat list input
            return output_row
    else:
        # Fallback, should not be reached if initial checks are correct
        return output_row