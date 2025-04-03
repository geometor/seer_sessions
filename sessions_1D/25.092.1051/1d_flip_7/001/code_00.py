import numpy as np

"""
Identify the first contiguous sequence of non-background (non-zero) pixels in the input grid (assumed to be 1xN).
This sequence should consist of a single 'head' pixel followed by one or more 'body' pixels.
The 'body' pixels must all be the same color, and this color must be different from the 'head' pixel's color.
If such a sequence is found, move the 'head' pixel to the end of the sequence and shift the 'body' pixels one position to the left to fill the gap.
If no such sequence is found, or the structure doesn't match (e.g., sequence length 1, body not uniform, head/body same color), return the grid unchanged.
"""

def find_first_non_white_sequence(row):
    """Finds the start and end indices of the first contiguous non-white sequence."""
    start_index = -1
    end_index = -1
    in_sequence = False
    for i, pixel in enumerate(row):
        if pixel != 0 and not in_sequence:
            # Start of a potential sequence
            start_index = i
            in_sequence = True
        elif pixel == 0 and in_sequence:
            # End of the sequence found
            end_index = i - 1
            break
        # Handle sequence reaching the very end of the row
        if in_sequence and i == len(row) - 1:
            end_index = i
            break
            
    if start_index != -1 and end_index != -1:
        return start_index, end_index
    else:
        return None, None # No sequence found

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid by moving the 'head' of a specific non-white sequence to its end.

    Args:
        input_grid: A numpy array representing the input grid. Expected to be 1xN.

    Returns:
        A numpy array representing the transformed grid. Returns a copy of the input if
        the transformation conditions are not met.
    """
    # Check if the input grid is 1xN as expected from examples
    if input_grid.shape[0] != 1:
        # If not 1xN, we cannot apply the logic derived from examples.
        # Return a copy of the input unchanged.
        # Or potentially raise an error, but returning unchanged is safer.
        # print("Warning: Input grid is not 1xN. Returning unchanged.")
        return input_grid.copy()

    # Work on a copy to avoid modifying the original input grid
    output_grid = input_grid.copy()
    row = output_grid[0] # Get the single row

    # 1. Find the contiguous sequence of non-white pixels
    start_index, end_index = find_first_non_white_sequence(row)

    # If no sequence found, return the original grid copy
    if start_index is None:
        return output_grid

    # 2. Check sequence length (must be at least 2 for head + body)
    sequence_len = end_index - start_index + 1
    if sequence_len < 2:
        return output_grid # Sequence too short

    # 3. Identify the 'head' and 'body'
    head_color = row[start_index]
    body_slice = row[start_index + 1 : end_index + 1]

    # 4. Validate the 'body' structure
    # Check if body is non-empty (already covered by sequence_len check)
    # Check if all body pixels have the same color
    if len(body_slice) > 0:
        body_color = body_slice[0]
        is_uniform = np.all(body_slice == body_color)
        if not is_uniform:
            return output_grid # Body is not uniform color
    else:
        # This case should not happen if sequence_len >= 2, but for safety:
        return output_grid

    # Check if head color is different from body color
    if head_color == body_color:
        return output_grid # Head and body are the same color

    # 5. Perform the transformation if all conditions met
    # a. Copy the body pixels
    body_values = body_slice.copy() 
    # b. Shift body left
    row[start_index : end_index] = body_values
    # c. Place head at the end
    row[end_index] = head_color

    return output_grid