import numpy as np
from collections import Counter

"""
Identifies a contiguous horizontal segment of non-white pixels in the input row.
Within this segment, there is always one pixel of a 'singleton' color and multiple pixels of a 'repeated' color.
The transformation swaps the position of the singleton pixel with the block of repeated pixels.
Effectively, the singleton pixel moves to the opposite end of the contiguous non-white segment.
White pixels remain unchanged.
"""

def find_non_white_segment(row):
    """Finds the start and end indices of the first contiguous non-white segment."""
    start_idx = -1
    end_idx = -1
    for i, pixel in enumerate(row):
        if pixel != 0:
            if start_idx == -1:
                start_idx = i
            end_idx = i
        elif start_idx != -1:
            # Segment ended before this white pixel
            break
    return start_idx, end_idx

def transform(input_grid):
    """
    Transforms the input grid according to the rule:
    1. Find the contiguous non-white segment in the single row.
    2. Identify the singleton pixel within that segment (the one different from its adjacent pixel within the segment).
    3. Move the singleton pixel to the other end of the segment.
    4. Return the modified grid.
    """
    # Input is always a single row, convert to list for easier manipulation
    input_row = list(input_grid[0])
    output_row = list(input_row) # Create a copy to modify

    # 1. Find the contiguous non-white segment
    start_idx, end_idx = find_non_white_segment(input_row)

    # If no non-white segment found, or segment is just one pixel, return original
    if start_idx == -1 or start_idx == end_idx:
        return [output_row] # Return as list of lists

    # 2. Extract the segment
    segment = input_row[start_idx : end_idx + 1]
    
    # Handle edge case where segment might be too short for comparison (shouldn't happen based on examples)
    if len(segment) < 2:
        return [output_row]

    # 3. Identify the singleton and its position (start or end)
    # The singleton is the element that differs from its neighbor within the segment.
    # If the first element is different from the second, the singleton is at the start.
    # Otherwise, the singleton must be at the end (given the problem constraints).
    singleton_at_start = (segment[0] != segment[1])

    # 4. Create the new segment by moving the singleton to the other end
    if singleton_at_start:
        # Move the start element (singleton) to the end
        new_segment = segment[1:] + [segment[0]]
    else:
        # The singleton must be at the end, move it to the start
        new_segment = [segment[-1]] + segment[:-1]

    # 5. Place the new segment back into the output row
    output_row[start_idx : end_idx + 1] = new_segment

    # Return the modified row, wrapped in a list
    return [output_row]