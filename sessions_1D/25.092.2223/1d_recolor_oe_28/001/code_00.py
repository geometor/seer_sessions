import numpy as np

"""
Transforms an input grid by identifying contiguous segments of orange (7) pixels. 
If a segment's length is greater than 3, it's recolored to gray (5). 
If the length is 3 or less, it's recolored to green (3). 
White (0) pixels remain unchanged.
"""

def find_contiguous_segments(row, target_color):
    """
    Identifies contiguous segments of a specific color in a 1D list.

    Args:
        row (list): The input list (row of the grid).
        target_color (int): The color value to find segments of.

    Returns:
        list: A list of tuples, where each tuple represents a segment
              (start_index, end_index, length).
    """
    segments = []
    i = 0
    n = len(row)
    while i < n:
        if row[i] == target_color:
            start_index = i
            while i < n and row[i] == target_color:
                i += 1
            end_index = i - 1
            length = end_index - start_index + 1
            segments.append((start_index, end_index, length))
        else:
            i += 1
    return segments

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list): A 2D list representing the input grid (expected to be 1xN).

    Returns:
        list: A 2D list representing the transformed output grid.
    """
    # Assuming input is always 1xN based on examples
    input_row = input_grid[0]
    output_row = list(input_row) # Initialize output as a copy of input

    # Find all segments of orange (7) pixels
    orange_segments = find_contiguous_segments(input_row, 7)

    # Process each orange segment
    for start, end, length in orange_segments:
        # Determine the replacement color based on length
        if length > 3:
            replacement_color = 5 # gray
        else:
            replacement_color = 3 # green

        # Recolor the segment in the output row
        for i in range(start, end + 1):
            output_row[i] = replacement_color

    # Return the modified row wrapped in a list (to match ARC format)
    return [output_row]
