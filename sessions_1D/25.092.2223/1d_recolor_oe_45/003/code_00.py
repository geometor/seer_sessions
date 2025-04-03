"""
Transforms an input grid (represented as a 1xN 2D NumPy array) by identifying 
contiguous horizontal segments of orange pixels (7) within the single row. If a 
segment has a length of exactly 6, it is replaced with red pixels (2) in the 
output grid. If the segment length is not 6, it is replaced with green pixels (3). 
White pixels (0) remain unchanged. The output grid has the same dimensions as the 
input grid.
"""

import numpy as np

def find_segments(row, target_color):
    """
    Finds contiguous segments of a target color in a 1D array (row).

    Args:
        row (np.array): The 1D array representing the grid row.
        target_color (int): The color value to find segments of.

    Returns:
        list: A list of dictionaries, each containing 'start_col' and 'length'
              for a found segment.
    """
    segments = []
    n_cols = len(row)
    i = 0
    while i < n_cols:
        if row[i] == target_color:
            # Found the start of a potential segment
            start_index = i
            current_length = 0
            # Count the length of the contiguous segment
            while i < n_cols and row[i] == target_color:
                current_length += 1
                i += 1
            # Record the found segment
            segments.append({'start_col': start_index, 'length': current_length})
            # Continue the outer loop from the end of the processed segment
            # 'i' is already incremented correctly by the inner while loop
        else:
            # If not the target color, just move to the next pixel
            i += 1
    return segments

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (np.array): A 2D NumPy array (expected shape 1xN) 
                               representing the input grid.

    Returns:
        np.array: A 2D NumPy array representing the transformed output grid.
    """
    # Ensure input is a 2D numpy array with at least one row
    if not isinstance(input_grid, np.ndarray) or input_grid.ndim != 2 or input_grid.shape[0] == 0:
         raise ValueError("Input must be a 2D NumPy array with at least one row.")

    # Although task implies 1xN, handle potential multi-row inputs gracefully by processing only the first row
    # If the task strictly guarantees 1xN, this check could be more stringent.
    # For this specific task based on examples, we assume 1xN is guaranteed.
    if input_grid.shape[0] != 1:
        print(f"Warning: Input grid has shape {input_grid.shape}. Processing only the first row as per observed pattern.")

    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    
    # Define constants based on the analysis
    target_color = 7      # Orange
    special_length = 6
    color_for_special_length = 2 # Red
    color_for_other_length = 3   # Green

    # Extract the first (and assumed only) row
    row_to_process = input_grid[0, :]

    # Find all segments of the target color (orange) in the row
    orange_segments = find_segments(row_to_process, target_color)

    # Process each found segment
    for segment in orange_segments:
        start_col = segment['start_col']
        length = segment['length']
        end_col = start_col + length # End column index (exclusive)

        # Determine the replacement color based on segment length
        if length == special_length:
            replacement_color = color_for_special_length
        else:
            replacement_color = color_for_other_length

        # Modify the corresponding slice in the output grid's first row
        output_grid[0, start_col:end_col] = replacement_color

    return output_grid