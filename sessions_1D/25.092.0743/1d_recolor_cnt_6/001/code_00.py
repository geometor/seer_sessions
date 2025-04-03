import numpy as np

"""
Identifies contiguous horizontal segments of yellow (4) pixels in the input grid (which is always a single row in the examples). 
Replaces each yellow segment with a new color based on its length:
- Length 1: Replace with gray (5).
- Length 2: Replace with orange (7).
- Length 3: Replace with magenta (6).
White (0) pixels remain unchanged.
"""

def find_segments(row, target_color):
    """
    Finds contiguous segments of a target color in a 1D array (row).

    Args:
        row (np.array): The 1D array to search within.
        target_color (int): The color value to find segments of.

    Returns:
        list: A list of tuples, where each tuple contains (start_index, end_index, length).
              end_index is exclusive (like Python slicing).
    """
    segments = []
    n = len(row)
    i = 0
    while i < n:
        if row[i] == target_color:
            start_index = i
            # Find the end of the segment
            while i < n and row[i] == target_color:
                i += 1
            end_index = i
            length = end_index - start_index
            segments.append((start_index, end_index, length))
        else:
            i += 1
    return segments

def transform(input_grid):
    """
    Transforms the input grid by recoloring yellow segments based on their length.

    Args:
        input_grid (list of lists): A grid represented as a list of lists.
                                     Expected to be 1xN for this specific task based on examples.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to numpy array for easier processing
    # Assuming input is always 1 row based on examples
    input_row = np.array(input_grid[0])

    # Initialize output_row as a copy of the input_row
    output_row = input_row.copy()

    # Define the color mapping based on segment length
    color_map = {
        1: 5,  # gray
        2: 7,  # orange
        3: 6,  # magenta
    }

    # Find all segments of yellow (4) pixels
    yellow_segments = find_segments(input_row, 4)

    # Iterate through the found segments and apply transformations
    for start, end, length in yellow_segments:
        # Determine the replacement color based on length
        if length in color_map:
            replacement_color = color_map[length]
            # Update the corresponding slice in the output row
            output_row[start:end] = replacement_color
        # else: # Optional: handle lengths not in the map if necessary
            # If a yellow segment has a length not specified (e.g., 4),
            # it remains yellow in the current logic.
            # pass

    # Convert the transformed row back to the list of lists format
    output_grid = [output_row.tolist()]

    return output_grid