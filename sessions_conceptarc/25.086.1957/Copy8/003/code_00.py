import numpy as np
import math

"""
Reflects non-background pixels from the left side of a central vertical
separator block onto the right side.

1. Identifies a central vertical block of columns composed entirely of the
   background color (0). This block defines the axis of symmetry. It prioritizes
   blocks not touching the grid edges (column 0 or width-1).
2. Calculates the reflection axis coordinate based on the start and end
   indices of this central separator block.
3. Initializes the output grid as a copy of the input grid.
4. Iterates through each pixel (r, c) to the *left* of the central separator block
   in the input grid.
5. If the pixel's color is not background (0), calculates its reflected column
   position c_reflected using the formula round(2 * axis - c).
6. If c_reflected is a valid column index within the grid, updates the pixel at 
   (r, c_reflected) in the output grid with the color from the input pixel (r, c). 
   Existing pixels (including non-background ones from the original input) at 
   the target location are overwritten by the reflection.
"""

def find_contiguous_blocks(indices):
    """
    Finds contiguous blocks in a sorted list of indices.
    E.g., [0, 1, 3, 4, 5, 7] -> [[0, 1], [3, 4, 5], [7]]
    """
    if not indices:
        return []
    blocks = []
    current_block = [indices[0]]
    for i in range(1, len(indices)):
        if indices[i] == indices[i-1] + 1:
            current_block.append(indices[i])
        else:
            blocks.append(current_block)
            current_block = [indices[i]]
    blocks.append(current_block)
    return blocks

def find_central_separator_indices(grid):
    """
    Finds the start and end column indices of the central vertical separator block.
    A separator column consists entirely of the background color (0).
    The central block is prioritized as one not touching the grid edges (col 0 or width-1).
    If only edge blocks exist, and there's only one block total, that block is returned
    (e.g., a single column separator in a 3-wide grid).
    Returns a tuple (start_col, end_col) or None if no suitable block is found.
    """
    num_rows, num_cols = grid.shape
    # Need at least 3 columns for a non-edge separator, or 1 column for an edge-case single separator.
    if num_cols < 1: 
        return None

    # Find all column indices that consist entirely of the background color (0)
    all_sep_cols = [c for c in range(num_cols) if np.all(grid[:, c] == 0)]
    if not all_sep_cols:
        # No separator columns found at all
        return None

    # Identify contiguous blocks of separator columns
    blocks = find_contiguous_blocks(sorted(all_sep_cols))

    # Filter blocks: Keep only blocks that do NOT contain column 0 AND do NOT contain column num_cols - 1
    central_blocks = []
    for block in blocks:
        touches_left_edge = (block[0] == 0)
        touches_right_edge = (block[-1] == num_cols - 1)
        if not touches_left_edge and not touches_right_edge:
            central_blocks.append(block)

    # If one or more non-edge blocks were found, choose the first one (assuming only one truly central block exists per task rule)
    if central_blocks:
        chosen_block = central_blocks[0] 
        return (chosen_block[0], chosen_block[-1])

    # If NO non-edge blocks were found, check if there was exactly one block overall.
    # This handles cases like [[1, 0, 1]] where the only separator is central by definition.
    if not central_blocks and len(blocks) == 1:
         chosen_block = blocks[0]
         # Return this single block's indices
         return (chosen_block[0], chosen_block[-1])

    # Otherwise (e.g., multiple blocks, all touching edges, or no separators) return None
    return None


def transform(input_grid):
    # Convert input list of lists to numpy array for efficient processing
    input_arr = np.array(input_grid, dtype=int)
    num_rows, num_cols = input_arr.shape

    # Initialize output grid as a direct copy of the input grid.
    # Reflection will overwrite pixels on this copy.
    output_arr = np.copy(input_arr)

    # Find the start and end indices of the central separator block
    separator_info = find_central_separator_indices(input_arr)

    # If no suitable central separator block is found, return the original grid unchanged.
    if separator_info is None:
        return input_grid 

    s_start, s_end = separator_info

    # Calculate the vertical reflection axis (can be fractional if separator width is even)
    axis_col = (s_start + s_end) / 2.0

    # Iterate through each row
    for r in range(num_rows):
        # Iterate through each column strictly to the *left* of the separator block
        for c in range(s_start): 
            color = input_arr[r, c]

            # Only reflect non-background pixels
            if color != 0:
                # Calculate the reflected column index using the axis.
                # Round to nearest integer for the grid index.
                c_reflected = round(2 * axis_col - c)

                # Check if the calculated reflected column index is valid (within grid bounds)
                if 0 <= c_reflected < num_cols:
                    # Update the output grid at the reflected position with the color
                    # from the left side. This overwrites whatever was originally
                    # at output_arr[r, c_reflected].
                    output_arr[r, c_reflected] = color

    # Convert the final output numpy array back to a list of lists
    output_grid = output_arr.tolist()
    
    return output_grid