"""
Identifies all contiguous horizontal segments of blue (1) pixels in the input row.
Calculates the length of each blue segment.
Finds the maximum length among all blue segments.
Changes the color of all blue segments that have the maximum length to magenta (6).
Leaves all other pixels (white pixels and shorter blue segments) unchanged.
"""

import copy

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.

    Args:
        input_grid: A list of integers representing the input row.

    Returns:
        A list of integers representing the transformed output row.
    """
    # Initialize output_grid as a copy of the input
    output_grid = list(input_grid)
    n = len(input_grid)
    
    # Find all contiguous segments of blue pixels (1)
    segments = []
    current_start = -1
    current_length = 0
    max_length = 0

    for i, pixel in enumerate(input_grid):
        if pixel == 1:
            # If this is the start of a new blue segment
            if current_start == -1:
                current_start = i
            current_length += 1
        else:
            # If we were tracking a blue segment, it just ended
            if current_start != -1:
                segments.append({'start': current_start, 'length': current_length})
                # Update max_length if this segment is the longest so far
                if current_length > max_length:
                    max_length = current_length
                # Reset tracking for the next potential segment
                current_start = -1
                current_length = 0

    # Handle case where the grid ends with a blue segment
    if current_start != -1:
        segments.append({'start': current_start, 'length': current_length})
        if current_length > max_length:
            max_length = current_length

    # Transform the segments that match the maximum length
    # Only proceed if there was at least one blue segment found
    if max_length > 0:
        for segment in segments:
            # If a segment's length is equal to the maximum length found
            if segment['length'] == max_length:
                # Change the pixels in the output grid for this segment to magenta (6)
                start_index = segment['start']
                end_index = start_index + segment['length']
                for i in range(start_index, end_index):
                    output_grid[i] = 6

    return output_grid