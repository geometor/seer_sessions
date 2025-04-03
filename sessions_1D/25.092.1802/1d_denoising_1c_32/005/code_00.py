import numpy as np
import itertools

"""
For each row in the input grid, identify the longest contiguous horizontal 
segment of non-white pixels. Keep only that segment in the output grid, 
replacing all other pixels in that row with the background color (white, 0). 
If multiple segments share the maximum length in a row, keep the one 
that appears earliest (leftmost). If a row contains no non-white pixels, 
or no segments of the primary non-white color, the corresponding output row 
will be entirely white. It is assumed each row contains at most one 
non-white color.
"""

def find_segments(grid_row, target_color):
    """
    Finds contiguous segments of a specific color in a 1D numpy array (grid row).

    Args:
        grid_row (np.array): The input 1D array representing a row of the grid.
        target_color (int): The color of the segments to find.

    Returns:
        list: A list of tuples, where each tuple represents a segment
              (start_index, end_index, length). end_index is exclusive.
              Returns an empty list if no segments are found.
    """
    segments = []
    start_index = -1
    for i, pixel in enumerate(grid_row):
        if pixel == target_color and start_index == -1:
            # Start of a potential segment
            start_index = i
        elif pixel != target_color and start_index != -1:
            # End of the current segment (pixel at i is not part of it)
            end_index = i
            length = end_index - start_index
            segments.append((start_index, end_index, length))
            start_index = -1 # Reset for the next segment

    # Check if the row ends with an active segment
    if start_index != -1:
        # The segment runs to the end of the row
        end_index = len(grid_row)
        length = end_index - start_index
        segments.append((start_index, end_index, length))

    return segments

def transform(input_grid):
    """
    Transforms the input grid according to the rule described above.

    Args:
        input_grid (list): A list of lists representing the input grid.

    Returns:
        list: A list of lists representing the transformed output grid.
    """
    # Convert input list of lists to a NumPy array for easier processing
    input_array = np.array(input_grid, dtype=int)
    
    # Initialize output grid with the same dimensions, filled with background color (0)
    output_array = np.zeros_like(input_array)
    
    # Get the number of rows in the grid
    num_rows = input_array.shape[0]

    # Iterate through each row of the input grid
    for r in range(num_rows):
        # Get the current row
        input_row = input_array[r]
        
        # Identify the unique non-white color(s) present in the row
        non_white_colors = np.unique(input_row[input_row != 0])
        
        # If no non-white colors exist in this row, the output row remains all zeros, so continue
        if non_white_colors.size == 0:
            continue
            
        # Assume only one non-white color per row based on examples and problem description
        target_color = non_white_colors[0]
        
        # Find all contiguous segments of the target color in the current row
        segments = find_segments(input_row, target_color)
        
        # If segments were found in this row
        if segments:
            # Select the segment with the maximum length.
            # max() with a key naturally handles ties by selecting the first element encountered,
            # which corresponds to the leftmost segment in case of length ties.
            longest_segment = max(segments, key=lambda item: item[2]) # item[2] is the length
            
            # Extract the start and end indices of the longest segment
            start, end, _ = longest_segment
            
            # Copy the pixels of the longest segment from the input row 
            # to the corresponding positions in the output row
            output_array[r, start:end] = input_row[start:end]
            
    # Convert the final NumPy array back to a list of lists for the required output format
    output_grid = output_array.tolist()
    
    return output_grid