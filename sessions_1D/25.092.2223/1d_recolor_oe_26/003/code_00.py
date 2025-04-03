import numpy as np

"""
Transforms a 1D grid (represented as a list containing a single inner list) 
by changing contiguous horizontal segments of orange (7) pixels based on their length parity.
Orange segments with an even length are changed to green (3).
Orange segments with an odd length are changed to red (2).
Black (0) pixels remain unchanged.
"""

def find_contiguous_segments(row, target_value):
    """
    Finds contiguous segments of a target value in a 1D list.

    Args:
        row (list): The input list (row of the grid).
        target_value (int): The value to find contiguous segments of.

    Returns:
        list: A list of tuples, where each tuple contains (start_index, end_index, length).
              end_index is exclusive.
    """
    segments = []
    n_cols = len(row)
    i = 0
    while i < n_cols:
        if row[i] == target_value:
            start_index = i
            j = i
            # Find the end of the contiguous segment
            while j < n_cols and row[j] == target_value:
                j += 1
            end_index = j  # exclusive index
            length = end_index - start_index
            segments.append((start_index, end_index, length))
            i = end_index  # Move iterator past the found segment
        else:
            i += 1
    return segments

def transform(input_grid):
    """
    Transforms the input grid according to the rule:
    Orange(7) segments of even length become Green(3).
    Orange(7) segments of odd length become Red(2).
    Black(0) remains Black(0).
    """

    # Convert numpy array to list of lists if necessary
    if isinstance(input_grid, np.ndarray):
        input_grid_list = input_grid.tolist()
    elif isinstance(input_grid, list) and all(isinstance(row, list) for row in input_grid):
         input_grid_list = input_grid
    else:
         raise TypeError("Input must be a numpy array or a list of lists.")


    # Validate input format - must be a single row
    if not input_grid_list or len(input_grid_list) != 1:
        raise ValueError("Input grid must contain exactly one row.")

    input_row = input_grid_list[0]
    
    # Initialize output_row as a copy of the input row
    output_row = list(input_row)

    # Define colors
    ORANGE = 7
    GREEN = 3
    RED = 2
    BLACK = 0 # Implicitly handled by copying and only modifying orange

    # Find all contiguous segments of orange pixels in the input row
    orange_segments = find_contiguous_segments(input_row, ORANGE)

    # Process each identified orange segment
    for start_index, end_index, length in orange_segments:
        # Determine the target color based on segment length parity
        if length % 2 == 0:
            # Even length segments become green
            target_color = GREEN
        else:
            # Odd length segments become red
            target_color = RED

        # Fill the corresponding segment in the output row with the target color
        for i in range(start_index, end_index):
            output_row[i] = target_color

    # Black pixels (0) were already copied and are not modified further.

    # Return the transformed row wrapped in a list to match ARC format
    output_grid = [output_row]
    
    # Optionally convert back to numpy array if that's standard practice?
    # For now, returning list of lists as per typical ARC examples.
    # If using numpy is preferred: return np.array(output_grid, dtype=input_grid.dtype if isinstance(input_grid, np.ndarray) else int)
    return output_grid
