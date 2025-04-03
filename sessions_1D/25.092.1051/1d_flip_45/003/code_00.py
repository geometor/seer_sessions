import numpy as np
import sys

# Add a print statement to check Python version (for debugging numpy behavior if needed)
# print(f"Using Python version: {sys.version}")
# print(f"Using Numpy version: {np.__version__}")

"""
Transformation Rule:
Identify the contiguous block of non-white (non-zero) pixels in the 1D input grid (assumed to be a single list or 1xN array).
This block must consist of exactly two adjacent sub-objects: 
1. Object A: a single pixel of one non-white color.
2. Object B: a sequence of one or more pixels of another, identical non-white color.
Swap the positions of Object A and Object B within the space originally occupied by the entire block.
Keep the background (white/zero) pixels unchanged.
Return the result as a list containing a single list (1xN grid format).
"""

def _find_non_white_segment(row):
    """
    Finds the start and end indices of the contiguous non-white segment.

    Args:
        row (np.array): The 1D input array.

    Returns:
        tuple: (start_idx, end_idx) or (None, None) if no valid segment found.
    """
    non_white_indices = np.where(row != 0)[0]

    # Check if there are at least two non-white pixels
    if len(non_white_indices) < 2:
        return None, None

    # Check for contiguity
    is_contiguous = np.all(np.diff(non_white_indices) == 1)
    if not is_contiguous:
        # Handle cases where non-white pixels exist but are not adjacent
        return None, None 
        
    start_idx = non_white_indices[0]
    end_idx = non_white_indices[-1]
    
    return start_idx, end_idx

def _identify_sub_objects(segment):
    """
    Identifies the two sub-objects (one single pixel, one sequence) within the segment.

    Args:
        segment (np.array): The contiguous non-white segment.

    Returns:
        tuple: (obj_a_color, obj_a_len, obj_b_color, obj_b_len, a_is_first) 
               or None if the segment doesn't match the pattern.
    """
    # Check if there are exactly two distinct colors in the segment
    unique_colors = np.unique(segment)
    if len(unique_colors) != 2:
        return None

    # Find the index where the color changes
    change_idx_relative = -1
    for i in range(len(segment) - 1):
        if segment[i] != segment[i+1]:
            change_idx_relative = i
            break

    # This should always be found if len(unique_colors) == 2
    if change_idx_relative == -1:
        # This case should theoretically not be reached due to unique_colors check
        return None 

    # Define the two parts based on the change point
    part1_color = segment[0]
    part1_len = change_idx_relative + 1
    part2_color = segment[change_idx_relative + 1]
    part2_len = len(segment) - part1_len

    # Determine which part is Object A (single) and Object B (sequence)
    obj_a_color, obj_a_len = -1, -1
    obj_b_color, obj_b_len = -1, -1
    a_is_first = False 

    if part1_len == 1 and part2_len >= 1:
        obj_a_color, obj_a_len = part1_color, part1_len
        obj_b_color, obj_b_len = part2_color, part2_len
        a_is_first = True
    elif part2_len == 1 and part1_len >= 1:
        obj_a_color, obj_a_len = part2_color, part2_len
        obj_b_color, obj_b_len = part1_color, part1_len
        a_is_first = False
    else:
        # Segment doesn't contain exactly one single pixel object and one sequence object
        return None

    return obj_a_color, obj_a_len, obj_b_color, obj_b_len, a_is_first


def transform(input_grid):
    """
    Swaps adjacent single-pixel and sequence objects in a 1D grid.

    Args:
        input_grid (list or list of lists): Represents the 1xN input grid. 
                                           Can be a flat list [0, 1, 2, ...] 
                                           or a nested list [[0, 1, 2, ...]].

    Returns:
        list of lists: The transformed 1xN grid in the format [[...]].
                       Returns the original grid (in [[...]] format) if 
                       no valid transformation is applicable.
    """
    # --- Input Handling and Initialization ---
    try:
        # Attempt to convert input to a 1D numpy array
        if isinstance(input_grid, list):
            if not input_grid: # Handle empty list case
                 return [[]]
            if isinstance(input_grid[0], list):
                # Input is likely [[...]]
                if len(input_grid) == 1:
                   row_list = input_grid[0]
                elif len(input_grid) == 0: # Handle [[]] case
                    return [[]]
                else: # Not a 1xN grid
                    # Return input as is, assuming it might be valid for another task type
                    # Or raise error if strict 1xN is required:
                    # raise ValueError("Input must be a 1xN grid (list of one list).")
                     print("Warning: Input grid has more than one row. Processing only the first.")
                     row_list = input_grid[0] # Process only first row if multiple given
            else:
                # Input is likely [...]
                row_list = input_grid
        else:
             # Try converting other types like numpy arrays directly
             temp_array = np.array(input_grid)
             if temp_array.ndim == 1:
                 row_list = temp_array.tolist()
             elif temp_array.ndim == 2 and temp_array.shape[0] == 1:
                 row_list = temp_array[0].tolist()
             elif temp_array.ndim == 0: # Handle scalar input
                 row_list = [int(temp_array)]
             else:
                 raise ValueError("Unsupported input grid format.")

        # Ensure row_list contains only integers if conversion succeeded
        if not all(isinstance(x, int) for x in row_list):
             raise ValueError("Grid elements must be integers.")

        input_row = np.array(row_list, dtype=int)
        
    except (ValueError, TypeError) as e:
        # If conversion fails or input is invalid, return it formatted as list of lists
        # print(f"Input handling error: {e}. Returning input as is.")
        # Attempt to return in standard format if possible
        if isinstance(input_grid, list) and input_grid and isinstance(input_grid[0], list):
             return input_grid
        elif isinstance(input_grid, list):
             return [input_grid]
        else:
             # Fallback for non-list inputs that caused errors
             try:
                 return [list(input_grid)] # Try converting the whole thing to a list within a list
             except:
                 return [[str(input_grid)]] # Last resort


    output_row = input_row.copy() # Initialize output as a copy

    # --- Find the non-white segment ---
    start_idx, end_idx = _find_non_white_segment(input_row)

    # If no valid segment found, return the original grid formatted correctly
    if start_idx is None:
        return [output_row.tolist()]

    segment = input_row[start_idx : end_idx + 1]

    # --- Identify the two sub-objects within the segment ---
    object_info = _identify_sub_objects(segment)

    # If segment doesn't match the expected pattern, return original grid
    if object_info is None:
        return [output_row.tolist()]

    obj_a_color, obj_a_len, obj_b_color, obj_b_len, a_is_first = object_info

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

    # --- Return the modified grid in the standard list-of-lists format ---
    return [output_row.tolist()]