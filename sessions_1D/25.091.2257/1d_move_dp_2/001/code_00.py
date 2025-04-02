"""
Identifies a contiguous horizontal segment of a single non-white, non-azure color and a single azure marker pixel (8) within a 1D input grid. The transformation moves the colored segment so that its rightmost end is immediately adjacent to the left of the azure marker pixel's position. All other pixels become white (0).
"""

import numpy as np

def find_azure_marker(grid_row):
    """Finds the column index of the azure marker (8)."""
    for idx, pixel in enumerate(grid_row):
        if pixel == 8:
            return idx
    return -1 # Should not happen based on examples

def find_colored_segment(grid_row):
    """Finds the start index, length, and color of the colored segment."""
    segment_color = -1
    segment_start = -1
    segment_length = 0

    for idx, pixel in enumerate(grid_row):
        # Find the start of a potential segment (not white, not azure)
        if pixel != 0 and pixel != 8 and segment_start == -1:
            segment_start = idx
            segment_color = pixel
            segment_length = 1
        # Continue the segment if the color matches
        elif pixel == segment_color and segment_start != -1:
            segment_length += 1
        # End the segment if a different color is found or the segment started
        elif segment_start != -1:
            break # Found the end of the segment

    if segment_start != -1:
        return segment_start, segment_length, segment_color
    else:
        return -1, 0, -1 # Should not happen based on examples


def transform(input_grid):
    """
    Transforms the input grid by moving the colored segment adjacent to the azure marker.

    Args:
        input_grid: A list of lists representing the input grid (expected 1xN).

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert to numpy array for easier handling (assuming 1 row)
    input_row = np.array(input_grid[0], dtype=int)
    height = 1
    width = len(input_row)

    # Initialize output_grid with the same dimensions, filled with white (0)
    output_grid = np.zeros((height, width), dtype=int)

    # 1. Find the position of the azure marker (8)
    azure_pos = find_azure_marker(input_row)
    if azure_pos == -1:
        # Handle case where marker isn't found (though examples guarantee it)
        return output_grid.tolist() # Return empty grid or raise error

    # 2. Find the colored segment (non-white, non-azure) properties
    segment_start_input, segment_length, segment_color = find_colored_segment(input_row)
    if segment_start_input == -1:
         # Handle case where segment isn't found (though examples guarantee it)
        return output_grid.tolist() # Return empty grid or raise error

    # 3. Place the azure marker in the output grid
    output_grid[0, azure_pos] = 8

    # 4. Calculate the new starting position for the colored segment
    # The segment should end at azure_pos - 1
    # So it starts at (azure_pos - 1) - (segment_length - 1) = azure_pos - segment_length
    segment_start_output = azure_pos - segment_length

    # 5. Place the colored segment in the output grid
    if segment_start_output >= 0 and segment_start_output + segment_length <= width:
        output_grid[0, segment_start_output : segment_start_output + segment_length] = segment_color
    else:
        # Handle edge case if placement goes out of bounds (shouldn't based on examples)
        print(f"Warning: Segment placement out of bounds. Azure Pos: {azure_pos}, Seg Len: {segment_length}")


    # Convert back to list of lists for the standard ARC format
    return output_grid.tolist()