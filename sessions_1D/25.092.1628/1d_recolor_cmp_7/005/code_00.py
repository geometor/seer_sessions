"""
Transforms an input grid by processing each row independently. 
In each row, it identifies the longest contiguous horizontal segment(s) 
of gray pixels (value 5) and changes their color to orange (value 7). 
If multiple segments in a row share the maximum length, all of them are changed. 
Pixels that are not part of the longest gray segment(s) in their respective rows remain unchanged.
"""

import copy

# Helper function to find contiguous segments of a specific color in a row
def find_color_segments(row, target_color):
    """
    Finds all contiguous segments of a specified color in a row.

    Args:
        row: A list of integers representing a row of pixels.
        target_color: The integer value of the color to find segments of.

    Returns:
        A list of tuples, where each tuple represents a segment
        (start_index, end_index, length). Returns an empty list if no
        such segments are found.
    """
    segments = []
    in_segment = False
    start_index = -1
    row_length = len(row)
    
    for i, pixel in enumerate(row):
        is_target = (pixel == target_color)
        
        # Start of a new segment
        if is_target and not in_segment:
            in_segment = True
            start_index = i
            
        # End of the current segment (pixel is different or end of row)
        if (not is_target or i == row_length - 1) and in_segment:
            in_segment = False
            # Adjust end_index if the segment ends exactly at the last pixel
            end_index = i if is_target else i - 1
            length = end_index - start_index + 1
            segments.append((start_index, end_index, length))
            start_index = -1 # Reset start index
            
    return segments

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # 1. Initialize output_grid as a deep copy of input_grid
    # Ensures the original input is not modified.
    output_grid = copy.deepcopy(input_grid)
    
    # Define colors
    gray_color = 5
    orange_color = 7

    # 2. Iterate through each row of the grid
    num_rows = len(output_grid)
    for r in range(num_rows):
        current_row = output_grid[r] # Reference to the row in the output grid

        # 3. Find all contiguous segments of gray (5) pixels in this row
        gray_segments = find_color_segments(current_row, gray_color)

        # 4. If no gray segments are found in this row, continue to the next row
        if not gray_segments:
            continue

        # 5. Determine the maximum length among the found segments in this row
        max_length = 0
        for _, _, length in gray_segments:
            if length > max_length:
                max_length = length
                
        # 6. Identify all segments in this row that have the maximum length
        longest_segments_in_row = []
        for start, end, length in gray_segments:
            if length == max_length:
                longest_segments_in_row.append((start, end))

        # 7. Recolor the longest segments to orange (7) in the output_grid's current row
        for start, end in longest_segments_in_row:
            # Iterate through the column indices of the segment
            for c in range(start, end + 1):
                # Change the pixel color in the current row of the output grid
                output_grid[r][c] = orange_color
            
    # 8. Return the modified output_grid
    return output_grid