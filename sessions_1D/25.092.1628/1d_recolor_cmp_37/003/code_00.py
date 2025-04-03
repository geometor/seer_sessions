"""
For each row in the input grid, identify all contiguous horizontal segments of gray pixels (5). 
Determine the maximum length among these segments within that row. 
Change the color of all gray segments in that row whose length equals the maximum length to maroon (9). 
Pixels not part of a longest gray segment (including white pixels and shorter gray segments) remain unchanged.
"""

import numpy as np

def find_horizontal_segments(row, target_color):
    """
    Finds contiguous horizontal segments of a target color in a list (row).

    Args:
        row (list or np.array): The input list/array of integers (pixels).
        target_color (int): The color value to find segments of.

    Returns:
        list: A list of tuples, where each tuple represents a segment
              and contains (start_index, end_index, length). Returns an
              empty list if no segments of target_color are found.
    """
    segments = []
    start_index = -1
    row_list = list(row) # Ensure iteration works correctly
    for i, pixel in enumerate(row_list):
        if pixel == target_color and start_index == -1:
            # Start of a new segment
            start_index = i
        elif pixel != target_color and start_index != -1:
            # End of the current segment (just before the current pixel)
            end_index = i - 1
            length = end_index - start_index + 1
            segments.append((start_index, end_index, length))
            start_index = -1 # Reset for the next potential segment

    # Handle a segment that potentially goes to the very end of the row
    if start_index != -1:
        end_index = len(row_list) - 1
        length = end_index - start_index + 1
        segments.append((start_index, end_index, length))

    return segments

def transform(input_grid):
    """
    Transforms the input grid by changing the longest horizontal gray segments 
    in each row to maroon.

    Args:
        input_grid (list of lists): A list of lists representing the input grid.

    Returns:
        list of lists: The transformed grid with the same dimensions.
    """
    # Convert input to numpy array for easier processing
    input_array = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input
    output_array = np.copy(input_array)
    
    # Get grid dimensions
    height, width = input_array.shape

    # Iterate through each row of the grid
    for r in range(height):
        current_row = input_array[r]
        
        # Find all contiguous horizontal segments of gray (5) pixels in the current row
        gray_segments = find_horizontal_segments(current_row, 5)

        # If no gray segments are found in this row, continue to the next row
        if not gray_segments:
            continue

        # Determine the maximum length among the gray segments found in this row
        max_length = 0
        for start, end, length in gray_segments:
            if length > max_length:
                max_length = length
        
        # If max_length is 0 (shouldn't happen if gray_segments is not empty, but safe check)
        if max_length == 0:
            continue

        # Iterate through the found gray segments again
        for start, end, length in gray_segments:
            # If a segment's length is equal to the maximum length for this row
            if length == max_length:
                # Change the color of pixels in that segment in the output grid to maroon (9)
                for c in range(start, end + 1):
                    output_array[r, c] = 9

    # Convert the final numpy array back to a list of lists before returning
    return output_array.tolist()