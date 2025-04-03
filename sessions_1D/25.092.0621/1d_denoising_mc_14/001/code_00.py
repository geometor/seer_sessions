"""
Locate the contiguous block of non-white pixels in the input 1D grid.
Within this block (the target segment), determine the most frequent color (dominant color).
Create a new grid identical to the input.
Replace all pixels within the bounds of the original target segment in the new grid with the dominant color.
Return the modified grid.
"""

import collections

def find_non_white_segment(grid_row):
    """
    Finds the start and end indices of the contiguous non-white segment.

    Args:
        grid_row: A list representing the 1D grid row.

    Returns:
        A tuple (start_index, end_index) or None if no non-white segment is found.
    """
    start_index = -1
    end_index = -1
    for i, pixel in enumerate(grid_row):
        if pixel != 0:
            if start_index == -1:
                start_index = i
            end_index = i # Keep updating end_index as long as we see non-white

    if start_index == -1:
        return None
    else:
        return start_index, end_index

def find_dominant_color(segment):
    """
    Finds the most frequent color in a list of pixels.

    Args:
        segment: A list of pixel color values.

    Returns:
        The most frequent color value. Returns None if segment is empty.
    """
    if not segment:
        return None
    # Count occurrences of each color
    color_counts = collections.Counter(segment)
    # Find the color with the highest count
    # most_common(1) returns a list of tuples [(color, count)]
    dominant_color, _ = color_counts.most_common(1)[0]
    return dominant_color

def transform(input_grid):
    """
    Transforms the input grid by homogenizing the central non-white segment
    based on its dominant color.

    Args:
        input_grid: A list representing the 1D input grid.

    Returns:
        A list representing the transformed 1D output grid.
    """
    # Initialize output_grid as a copy of the input
    # Check if input is a list of lists (like [[...]]) or just a list ([...])
    # The examples provided look like 1D lists, but ARC typically uses list of lists
    # Assuming it's a 1D list based on the problem description format
    if not isinstance(input_grid[0], list):
         # It's a 1D list like [0, 0, 9, 3, 9, 0, 0]
        input_row = input_grid
    else:
         # It's a list containing one row [[0, 0, 9, 3, 9, 0, 0]]
         # This case assumes there's only ever one row. If multi-row grids are possible
         # for this task, the logic needs adjustment.
         if len(input_grid) != 1:
             # Handle unexpected multi-row input, maybe raise error or return input
             print("Warning: Expected 1D grid (list or list-of-lists with one row). Returning input.")
             return input_grid
         input_row = input_grid[0]


    output_row = list(input_row) # Make a copy

    # 1. Locate the contiguous block of non-white pixels (target segment)
    segment_indices = find_non_white_segment(input_row)

    # If no non-white segment exists, return the original grid
    if segment_indices is None:
         if not isinstance(input_grid[0], list):
             return output_row # Return 1D list
         else:
             return [output_row] # Return list of lists

    start_index, end_index = segment_indices

    # 2. Extract the target segment
    target_segment = input_row[start_index : end_index + 1]

    # 3. Identify the dominant color within the target segment
    dominant_color = find_dominant_color(target_segment)

    # If segment was somehow empty (shouldn't happen if indices found), return copy
    if dominant_color is None:
        if not isinstance(input_grid[0], list):
            return output_row # Return 1D list
        else:
            return [output_row] # Return list of lists


    # 4. Create the output grid (already done by copying)

    # 5. Modify the output grid: set pixels in the segment range to dominant color
    for i in range(start_index, end_index + 1):
        output_row[i] = dominant_color

    # 6. Return the modified grid in the original format
    if not isinstance(input_grid[0], list):
        return output_row # Return 1D list
    else:
        return [output_row] # Return list of lists
