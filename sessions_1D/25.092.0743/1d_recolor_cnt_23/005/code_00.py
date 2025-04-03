"""
Recolor contiguous horizontal segments of orange pixels (7) within a single-row grid based on the length of the segment. Segments of length 1 become blue (1), length 2 become gray (5), and length 3 become red (2). White pixels (0) remain unchanged. The input and output are 2D grids (assumed 1xN).
"""

import copy

# Defines the mapping from segment length to output color
LENGTH_TO_COLOR_MAP = {
    1: 1, # blue
    2: 5, # gray
    3: 2, # red
}
TARGET_COLOR = 7 # orange
BACKGROUND_COLOR = 0 # white


def find_and_recolor_segments(input_row, output_row):
    """
    Identifies segments of the target color in the input row and recolors them
    in the output row based on their length.

    Args:
        input_row (list[int]): The single row from the input grid.
        output_row (list[int]): The corresponding row from the output grid to modify.
    """
    width = len(input_row)
    col = 0
    while col < width:
        # Check if the current pixel is the target color we want to process
        if input_row[col] == TARGET_COLOR:
            start_col = col
            segment_length = 0
            # Measure the length of the contiguous segment of the target color
            temp_col = col
            while temp_col < width and input_row[temp_col] == TARGET_COLOR:
                segment_length += 1
                temp_col += 1

            # Determine the replacement color based on the segment length
            replacement_color = LENGTH_TO_COLOR_MAP.get(segment_length)

            # If a mapping exists for this length, apply the replacement color
            if replacement_color is not None:
                for i in range(segment_length):
                    # Modify the output row directly
                    output_row[start_col + i] = replacement_color

            # Advance the main column index past the processed segment
            # If segment_length is 0 (shouldn't happen if TARGET_COLOR found),
            # this still works by advancing 'col' by the length found.
            col += segment_length

        else:
            # If the current pixel is not the target color, just move to the next column
            col += 1


def transform(input_grid):
    """
    Applies the segment length-based recoloring transformation to a 1xN grid.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid (expected to be 1xN).

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    # Ensure the input is not empty and has at least one row
    if not input_grid or not input_grid[0]:
        return [] # Return empty for empty input

    # Initialize output_grid as a deep copy to avoid modifying the original
    output_grid = copy.deepcopy(input_grid)

    # We are assuming the grid is 1xN, so we process only the first row
    input_row = input_grid[0]
    output_row = output_grid[0] # Get the corresponding row from the copy

    # Find segments in the input row and apply recoloring rules to the output row
    find_and_recolor_segments(input_row, output_row)

    # Return the modified output grid
    return output_grid