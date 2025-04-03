"""
Recolors contiguous horizontal segments of orange pixels (7) within a single-row grid based on the length of the segment. Segments of length 1 become blue (1), length 2 become gray (5), and length 3 become red (2). White pixels (0) remain unchanged. The input and output are 2D grids (assumed 1xN).
"""

import copy

# Define constants for colors and the mapping rule
TARGET_COLOR = 7 # orange
BACKGROUND_COLOR = 0 # white
LENGTH_TO_COLOR_MAP = {
    1: 1, # blue
    2: 5, # gray
    3: 2, # red
}

def measure_segment_length(row, start_col, target_color):
    """Measures the length of a contiguous segment of target_color starting at start_col."""
    width = len(row)
    length = 0
    current_col = start_col
    while current_col < width and row[current_col] == target_color:
        length += 1
        current_col += 1
    return length

def recolor_segment(output_row, start_col, length, color):
    """Recolors a segment in the output row."""
    for i in range(length):
        if start_col + i < len(output_row): # Bounds check just in case
             output_row[start_col + i] = color

def process_row(input_row, output_row):
    """Processes a single row to find and recolor segments."""
    width = len(input_row)
    col = 0
    while col < width:
        # Check if the current pixel is the target color
        if input_row[col] == TARGET_COLOR:
            start_col = col
            # Measure the length of the contiguous orange segment
            segment_length = measure_segment_length(input_row, start_col, TARGET_COLOR)

            # Determine the replacement color based on the segment length using the map
            replacement_color = LENGTH_TO_COLOR_MAP.get(segment_length)

            # If a valid replacement color is found (length 1, 2, or 3)
            if replacement_color is not None:
                # Recolor the corresponding segment in the output row
                recolor_segment(output_row, start_col, segment_length, replacement_color)

            # Advance the main column index past the processed segment
            # This works correctly even if no replacement was made (e.g., length > 3)
            col += segment_length

        else:
            # If the current pixel is not the target color (it's background),
            # simply move to the next column. The output_row already has the
            # correct background color from the deepcopy.
            col += 1


def transform(input_grid):
    """
    Applies the segment length-based recoloring transformation to a 1xN grid.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid (expected to be 1xN).

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    # Handle empty input grid case
    if not input_grid or not input_grid[0]:
        return []

    # Create a deep copy of the input grid to modify and return as output
    output_grid = copy.deepcopy(input_grid)

    # Since the task operates on a single row (1xN grid), extract the first row
    # from both input and output grids.
    input_row = input_grid[0]
    output_row = output_grid[0] # Modify the row within the output_grid structure

    # Process the row to find and recolor segments based on length
    process_row(input_row, output_row)

    # Return the modified grid
    return output_grid