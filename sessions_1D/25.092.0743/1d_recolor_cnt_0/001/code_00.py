import numpy as np

def find_red_segments(input_row):
    """
    Identifies contiguous horizontal segments of red (2) pixels.

    Args:
        input_row (list): A single row (list of integers) representing the input grid.

    Returns:
        list: A list of tuples, where each tuple contains (start_index, length)
              of a red segment.
    """
    segments = []
    start_index = -1
    current_length = 0
    for i, pixel in enumerate(input_row):
        if pixel == 2:  # Red pixel
            if start_index == -1:
                start_index = i
            current_length += 1
        else:  # Not a red pixel (or end of a segment)
            if start_index != -1:
                # End of a red segment
                segments.append((start_index, current_length))
                start_index = -1
                current_length = 0
    # Check if a segment ends at the very end of the row
    if start_index != -1:
        segments.append((start_index, current_length))
    return segments

def transform(input_grid):
    """
    Transforms the input grid by recoloring contiguous red (2) segments based on their length.
    - Length 1 becomes blue (1).
    - Length 2 becomes azure (8).
    - Length 3 becomes gray (5).
    White (0) pixels remain unchanged.

    Args:
        input_grid (list): A 1D list of integers representing the input row.

    Returns:
        list: The transformed 1D list.
    """
    # The input is expected to be a single row (1D list)
    input_row = input_grid

    # Initialize output_grid as a copy of the input row
    # We will modify it based on the segments found
    output_row = list(input_row) # Create a mutable copy

    # Find all segments of red pixels
    red_segments = find_red_segments(input_row)

    # Map segment lengths to output colors
    length_to_color_map = {
        1: 1,  # Blue
        2: 8,  # Azure
        3: 5   # Gray
    }

    # Iterate through the identified red segments and modify the output row
    for start_index, length in red_segments:
        # Determine the output color based on the segment length
        output_color = length_to_color_map.get(length)

        # If the length is one we handle (e.g., length 4 was not in examples)
        if output_color is not None:
            # Recolor the segment in the output row
            for i in range(start_index, start_index + length):
                output_row[i] = output_color
        # If length is not in the map, pixels retain their original value (which was 2)
        # However, the problem description implies all red pixels change,
        # and only lengths 1, 2, 3 were observed. We'll stick to the observed pattern.
        # White pixels (0) were already copied and remain unchanged unless they were part of a red segment start index mistake (which find_red_segments prevents).


    return output_row