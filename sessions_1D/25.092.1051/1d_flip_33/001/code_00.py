import numpy as np

"""
Transformation Rule:
Identifies a contiguous sequence of non-white pixels (value != 0) in the 1-dimensional input grid (represented as a 1xN grid).
Moves the leftmost pixel of this sequence to the rightmost position within that sequence's original span.
All other pixels within the identified sequence shift one position to the left to fill the gap created by moving the first pixel.
Pixels with value 0 (white) remain unchanged in their positions.
If no non-white sequence exists or the sequence has only one pixel, the grid remains unchanged.
"""

def find_non_white_segment(grid_row):
    """
    Finds the start and end indices (inclusive) of the first contiguous non-white segment.

    Args:
        grid_row (np.array): A 1D numpy array representing the row of the grid.

    Returns:
        tuple: A tuple containing the start index and end index (inclusive)
               of the segment. Returns (None, None) if no non-white segment is found.
    """
    non_white_indices = np.where(grid_row != 0)[0]
    if len(non_white_indices) == 0:
        return None, None  # No non-white pixels found

    start_index = non_white_indices[0]
    end_index = start_index
    # Check for contiguity
    for i in range(1, len(non_white_indices)):
        if non_white_indices[i] == end_index + 1:
            end_index += 1
        else:
            # Break at the first gap, assuming only one segment matters per row based on examples
            break
    return start_index, end_index

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list): A list containing a single list of integers (representing a 1xN grid).

    Returns:
        list: A list containing a single list of integers representing the transformed 1xN grid.
    """
    # Ensure input is valid and has the expected structure (list of lists)
    if not input_grid or not isinstance(input_grid, list) or not input_grid[0] or not isinstance(input_grid[0], list):
        # Return input as is if it's empty or not in the expected format
        return input_grid

    # Convert the first (and only) row to a numpy array for easier processing
    grid_row_np = np.array(input_grid[0], dtype=int)

    # Find the contiguous block of non-white pixels
    start_index, end_index = find_non_white_segment(grid_row_np)

    # If no segment is found, or the segment has only one pixel, no change is needed
    if start_index is None or start_index == end_index:
        # Return the original grid in the list-of-lists format
        return input_grid

    # Create a copy of the row to modify for the output
    output_row_np = grid_row_np.copy()

    # Extract the segment that needs transformation
    segment = grid_row_np[start_index : end_index + 1]

    # Perform the rotation: move the first element to the end
    # Check segment length again just in case, although covered by start_index == end_index check
    if len(segment) > 1:
        first_element = segment[0]
        remaining_elements = segment[1:]
        # Concatenate remaining elements with the first element at the end
        rearranged_segment = np.concatenate((remaining_elements, [first_element]))

        # Place the rearranged segment back into the output row
        output_row_np[start_index : end_index + 1] = rearranged_segment

    # Convert the transformed numpy row back to a list
    output_row_list = output_row_np.tolist()

    # Return the result in the original list-of-lists format
    return [output_row_list]