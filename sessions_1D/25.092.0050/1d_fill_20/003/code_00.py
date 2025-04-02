"""
Identifies the two non-white pixels in a 1D input grid (potentially represented as a 1xN 2D grid). 
Fills the segment between these two pixels (inclusive) with their color. 
Pixels outside this segment remain white (0). The output format matches the input format (list or list of list).
"""

import numpy as np

def transform(input_grid):
    """
    Fills the segment between two identical non-white marker pixels in a 1D grid,
    handling both list and list-of-list input formats.

    Args:
        input_grid (list or list[list]): A list representing the 1D input grid 
                                         (e.g., [0, 0, 7, 0, 0, 7, 0]) or a 
                                         list containing one list for a 1xN grid 
                                         (e.g., [[0, 0, 7, 0, 0, 7, 0]]).

    Returns:
        list or list[list]: The transformed grid in the same format as the input.
    """

    # Determine input format and convert to a 1D NumPy array for processing
    is_list_of_lists = isinstance(input_grid, list) and len(input_grid) > 0 and isinstance(input_grid[0], list)
    
    if is_list_of_lists:
        # Input is likely [[...]], extract the inner list
        if len(input_grid) == 1:
            grid_1d = np.array(input_grid[0])
        else:
            # Handle unexpected multi-row input, maybe raise error or return input
            print("Warning: Expected input with a single row (list of list with one inner list).")
            return input_grid # Return original for unexpected format
    elif isinstance(input_grid, list):
        # Input is likely [...]
        grid_1d = np.array(input_grid)
    else:
        # Handle other unexpected input types
        print(f"Warning: Unexpected input type: {type(input_grid)}")
        return input_grid # Return original

    # Find the non-white color
    non_white_colors = np.unique(grid_1d[grid_1d != 0])
    if len(non_white_colors) == 0:
        # No markers found, return original grid in the original format
        return input_grid
    if len(non_white_colors) != 1:
        # More than one non-white color found, this contradicts task assumption
        print(f"Warning: Expected exactly one non-white marker color, found {non_white_colors}. Using the first one.")
        # Fallback: proceed with the first non-white color found
        # Alternatively, could return input_grid here if stricter adherence is needed.
        
    marker_color = non_white_colors[0]

    # Find the indices (positions) of the marker color
    marker_indices = np.where(grid_1d == marker_color)[0]

    if len(marker_indices) != 2:
        # Did not find exactly two markers as expected
        print(f"Warning: Expected exactly two markers of color {marker_color}, found {len(marker_indices)}.")
        # Return original grid in the original format if assumptions aren't met
        return input_grid

    # Determine the start and end indices of the segment to fill
    start_index = np.min(marker_indices)
    end_index = np.max(marker_indices)

    # Create the output array as a copy of the 1D input array
    output_grid_1d = grid_1d.copy()

    # Fill the range from start_index to end_index (inclusive) with the marker color
    output_grid_1d[start_index : end_index + 1] = marker_color

    # Convert the 1D NumPy array back to the original input format
    if is_list_of_lists:
        # Convert back to list of list: [[...]]
        output_grid = [output_grid_1d.tolist()]
    else:
        # Convert back to simple list: [...]
        output_grid = output_grid_1d.tolist()

    return output_grid