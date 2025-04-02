import copy

"""
Identify the first contiguous sequence of a non-white color (the 'template segment').
Then, iterate through the rest of the row. Whenever a pixel matching the template color is found, 
replace the pixels in the output row starting at that position with the template segment.
Handles potential boundary truncation if the template segment extends past the end of the row.
Assumes the input is a 1xN grid (a list containing a single list).
"""

def find_first_non_white_segment(row):
    """
    Finds the first contiguous segment of non-white pixels in a row.

    Args:
        row: A list of integers representing a row of pixels.

    Returns:
        A tuple containing:
        - template_segment (list): The sequence of pixels in the segment.
        - segment_color (int): The color of the segment.
        - end_index (int): The index immediately following the segment.
        Returns (None, None, None) if no non-white segment is found.
    """
    start_index = -1
    segment_color = -1
    
    # Find the start of the first non-white segment
    for i, pixel in enumerate(row):
        if pixel != 0:
            start_index = i
            segment_color = pixel
            break
            
    if start_index == -1:
        # No non-white pixels found
        return None, None, None
        
    # Find the end of the segment
    end_index = start_index
    while end_index < len(row) and row[end_index] == segment_color:
        end_index += 1
        
    template_segment = row[start_index:end_index]
    
    return template_segment, segment_color, end_index

def transform(input_grid):
    """
    Transforms the input grid based on the rule:
    Find the first non-white segment, and replace subsequent occurrences
    of its color with copies of the segment.

    Args:
        input_grid: A list of lists representing the input grid (expected 1xN).

    Returns:
        A list of lists representing the transformed grid.
    """
    # Ensure input is treated as a single row, even if nested [[...]]
    if not input_grid or not input_grid[0]:
        return copy.deepcopy(input_grid) # Return empty or original if invalid

    input_row = input_grid[0]
    output_row = list(input_row) # Create a mutable copy
    row_length = len(input_row)

    # 1. Find the template segment and its properties
    template_segment, segment_color, scan_start_index = find_first_non_white_segment(input_row)

    # If no non-white segment found, return the original
    if template_segment is None:
        # Wrap the row back into a list of lists format
        return [output_row] 

    template_length = len(template_segment)

    # 2. Iterate through the rest of the row after the template
    i = scan_start_index
    while i < row_length:
        # 3. Check if the current pixel matches the segment color (trigger pixel)
        if input_row[i] == segment_color:
            # 4. Copy the template segment into the output row starting at index i
            # Handle boundary conditions: determine how much of the template fits
            num_pixels_to_copy = min(template_length, row_length - i)
            
            for j in range(num_pixels_to_copy):
                output_row[i + j] = template_segment[j]
            
            # Optimization: Skip checking pixels that were just overwritten by the template
            # We can jump ahead by the length of the copied segment.
            # If we don't do this, we might re-trigger on a pixel within the
            # segment we just copied if the template contained the trigger color
            # more than once (though not the case in examples).
            # Start next check *after* the copied segment.
            i += num_pixels_to_copy 
        else:
             # Move to the next pixel if it wasn't a trigger
            i += 1

    # Wrap the transformed row back into a list of lists format
    return [output_row]
