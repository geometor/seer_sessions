"""
Transforms a 1D input grid by finding the contiguous segment of non-white (non-zero) pixels
and swapping the colors of the first and last pixels within that segment.
If no non-white segment is found, or the segment consists of only one pixel,
the input grid is returned unchanged.
"""

import numpy as np

def find_non_white_segment_indices(row):
    """
    Finds the start and end indices of the contiguous non-white segment in a 1D array.

    Args:
        row (np.array): A 1D numpy array representing a row of the grid.

    Returns:
        tuple: A tuple containing the start index and end index of the segment.
               Returns (None, None) if no non-white segment is found or if it's invalid.
    """
    non_white_indices = np.where(row != 0)[0]
    if len(non_white_indices) < 2: # Need at least two non-white pixels to swap
        return None, None

    start_index = non_white_indices[0]
    end_index = non_white_indices[-1]

    # Check for contiguity (although the examples imply it, good practice to check)
    # A simple check: are all indices between start and end present in non_white_indices?
    # However, the problem description just says "contiguous sequence", implying we only care about the first and last overall non-zero elements.
    # Let's stick to the simpler interpretation based on the examples: find the first and last non-zero.
    # If there were gaps, the logic might need adjustment, but based on examples, this is sufficient.

    # Verify the segment length is the difference between end and start + 1
    # If not, it means there are white pixels *within* the bounds defined by the first and last non-white pixel.
    # The examples show solid blocks. Let's assume this holds.
    if len(non_white_indices) != (end_index - start_index + 1):
         # This handles cases like [0, 1, 1, 0, 1, 1, 0] where np.where finds indices [1, 2, 4, 5]
         # start = 1, end = 5. Length = 4. end-start+1 = 5. Not contiguous.
         # However, the examples *only* show fully contiguous blocks.
         # For this specific task based *only* on the examples, we can simplify and just use the min and max index found.
         pass # Let's proceed assuming the examples define the scope.


    return start_index, end_index

def transform(input_grid):
    """
    Transforms the input grid by swapping the first and last pixels of the non-white segment.

    Args:
        input_grid (list or np.array): A 2D list or numpy array representing the input grid.
                                      Expected to have only one row based on examples.

    Returns:
        np.array: The transformed grid as a numpy array.
    """
    # Convert input to numpy array for easier handling
    input_array = np.array(input_grid, dtype=int)

    # Ensure it's effectively 1D as per examples (check if only 1 row)
    if input_array.shape[0] != 1:
        # Handle potential multi-row cases if necessary, or raise error
        # For now, assume it's always 1 row based on examples.
        # If it can be multi-row, the logic needs clarification.
        # Let's proceed assuming 1 row.
        pass

    # Extract the single row
    row = input_array[0]

    # Find the start and end indices of the non-white segment
    start_index, end_index = find_non_white_segment_indices(row)

    # Initialize output_grid as a copy of the input
    output_grid = input_array.copy()

    # If a valid segment for swapping is found
    if start_index is not None and end_index is not None and start_index != end_index:
        # Get the colors to swap
        start_color = row[start_index]
        end_color = row[end_index]

        # Perform the swap in the output grid's row
        output_grid[0, start_index] = end_color
        output_grid[0, end_index] = start_color

    # Return the (potentially modified) output grid
    return output_grid.tolist() # Return as list of lists matching ARC format