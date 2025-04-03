import copy

"""
Identifies contiguous horizontal segments of maroon (9) pixels in a single-row input grid.
Replaces each maroon segment with a segment of the same length but with a new color based on the length:
- Length 1: Replaced by yellow (4).
- Length 2: Replaced by orange (7).
- Length 3: Replaced by green (3).
White (0) pixels remain unchanged.
"""

def transform(input_grid):
    """
    Transforms the input grid based on the length of contiguous maroon segments.

    Args:
        input_grid (list[list[int]]): A 1xN grid represented as a list containing one list of integers.

    Returns:
        list[list[int]]: The transformed 1xN grid.
    """
    # Ensure input is a single row grid
    if len(input_grid) != 1:
        raise ValueError("Input grid must have exactly one row.")

    input_row = input_grid[0]
    output_row = copy.deepcopy(input_row) # Start with a copy of the input row
    n = len(input_row)
    i = 0

    # Iterate through the row
    while i < n:
        # Check if the current pixel is maroon
        if input_row[i] == 9:
            # Found the start of a potential maroon segment
            segment_start = i
            segment_length = 0
            # Measure the length of the contiguous maroon segment
            while i < n and input_row[i] == 9:
                segment_length += 1
                i += 1 # Move index forward within the segment

            # Determine the replacement color based on segment length
            replacement_color = -1 # Default/error value
            if segment_length == 1:
                replacement_color = 4 # Yellow
            elif segment_length == 2:
                replacement_color = 7 # Orange
            elif segment_length == 3:
                replacement_color = 3 # Green
            # Add other cases here if needed based on future examples

            # Fill the output row with the replacement color for the segment's length
            if replacement_color != -1:
                for j in range(segment_start, segment_start + segment_length):
                    output_row[j] = replacement_color
            # 'i' is already advanced past the segment by the inner while loop
        else:
            # If the pixel is not maroon (must be white), just move to the next pixel
            i += 1

    # Return the modified row within a list to match the grid format
    return [output_row]
