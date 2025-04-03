import numpy as np

"""
Transformation Rule:
Identify the contiguous block of non-white (non-zero) pixels in the 1D input grid.
This block consists of two adjacent sub-objects: one is a single pixel of one color (Object A), and the other is a sequence of one or more pixels of another identical color (Object B).
Swap the positions of Object A and Object B within the space originally occupied by the entire block.
Keep the background (white/zero) pixels unchanged.
"""

def transform(input_grid):
    """
    Swaps the positions of two adjacent, non-white objects within a 1D grid.
    One object is a single pixel, the other is a sequence of one or more pixels.

    Args:
        input_grid (list of lists): A 1xN grid represented as a list containing one list of integers.

    Returns:
        list of lists: The transformed 1xN grid.
    """

    # Ensure input is a numpy array for easier manipulation
    # Expecting input like [[0, 0, 2, 4, 4, 0]]
    if not isinstance(input_grid, list) or not input_grid or not isinstance(input_grid[0], list):
         raise ValueError("Input grid must be a non-empty list of lists.")
         
    grid = np.array(input_grid, dtype=int)

    # Handle potential shapes (e.g., direct 1D array input during testing)
    if grid.ndim == 1:
       # If input was accidentally flattened, reshape to 1xN
       grid = grid.reshape(1, -1)
    elif grid.ndim == 2 and grid.shape[0] != 1:
         raise ValueError("Input grid must have exactly one row.")
         
    # Work with the single row
    row = grid[0]
    output_row = row.copy() # Initialize output as a copy of the input row

    # --- Find the non-white segment ---
    non_white_indices = np.where(row != 0)[0]
    
    # If no non-white pixels or only one, return the original grid
    if len(non_white_indices) < 2:
        return input_grid 

    start_idx = non_white_indices[0]
    end_idx = non_white_indices[-1]
    segment = row[start_idx : end_idx + 1]
    
    # If the segment contains only one color, no swap is possible/needed
    if len(np.unique(segment)) < 2:
        return input_grid

    # --- Identify the two sub-objects within the segment ---
    # Find the index where the color changes
    change_idx_relative = -1
    for i in range(len(segment) - 1):
        if segment[i] != segment[i+1]:
            change_idx_relative = i
            break
            
    # This should always be found if len(np.unique(segment)) >= 2
    if change_idx_relative == -1:
         # Should not happen based on previous check, but added for robustness
         print(f"Warning: Could not find color change in segment: {segment}")
         return input_grid

    # Define the two parts based on the change point
    part1_color = segment[0]
    part1_len = change_idx_relative + 1
    part2_color = segment[change_idx_relative + 1]
    part2_len = len(segment) - part1_len

    # --- Determine which part is Object A (single) and Object B (sequence) ---
    obj_a_color, obj_a_len = -1, -1
    obj_b_color, obj_b_len = -1, -1
    a_is_first = False # Flag to track if Object A appeared first in the input segment

    if part1_len == 1 and part2_len >= 1:
        obj_a_color, obj_a_len = part1_color, part1_len
        obj_b_color, obj_b_len = part2_color, part2_len
        a_is_first = True
    elif part2_len == 1 and part1_len >= 1:
        obj_a_color, obj_a_len = part2_color, part2_len
        obj_b_color, obj_b_len = part1_color, part1_len
        a_is_first = False
    else:
        # If neither part has length 1, the input doesn't match the expected pattern
        print(f"Warning: Segment {segment} does not contain one single pixel object and one sequence object.")
        return input_grid # Return original grid if pattern doesn't match

    # --- Perform the swap in the output grid ---
    current_write_idx = start_idx # Start writing at the beginning of the segment's original position

    if a_is_first:
        # If A was first in input, write B first in output
        output_row[current_write_idx : current_write_idx + obj_b_len] = obj_b_color
        current_write_idx += obj_b_len
        # Then write A
        output_row[current_write_idx : current_write_idx + obj_a_len] = obj_a_color
    else:
        # If B was first in input, write A first in output
        output_row[current_write_idx : current_write_idx + obj_a_len] = obj_a_color
        current_write_idx += obj_a_len
        # Then write B
        output_row[current_write_idx : current_write_idx + obj_b_len] = obj_b_color

    # --- Return the modified grid in the original list-of-lists format ---
    output_grid = output_row.reshape(1, -1)
    return output_grid.tolist()
