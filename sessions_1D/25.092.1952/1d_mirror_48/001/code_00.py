import numpy as np
from typing import List, Tuple, Optional

"""
Transformation Rule:
Identify a pivot element (color 9) and a contiguous segment of another color (non-0, non-9).
Move the segment to the opposite side of the pivot, maintaining the same number of background (0) pixels between the segment and the pivot.
The pivot remains fixed, and the segment's color and length remain unchanged. The rest of the grid is filled with the background color (0).
"""

def find_pivot_index(grid: List[int]) -> Optional[int]:
    """Finds the index of the pivot element (9)."""
    try:
        return grid.index(9)
    except ValueError:
        return None # Pivot not found

def find_segment(grid: List[int], pivot_index: Optional[int]) -> Optional[Tuple[int, int, int]]:
    """
    Finds the contiguous segment of non-0, non-9 color.
    Returns: (color, start_index, length) or None if not found.
    """
    segment_color = -1
    segment_start = -1
    segment_length = 0

    for i, color in enumerate(grid):
        if color != 0 and (pivot_index is None or i != pivot_index):
            # Found the start of a potential segment
            if segment_start == -1:
                segment_color = color
                segment_start = i
                segment_length = 1
            # Continuing an existing segment
            elif color == segment_color:
                 segment_length += 1
            # Found a different segment - this shouldn't happen based on examples
            # but good to handle. We assume only one segment.
            else:
                 # If we already found a segment, break (assume first one is THE one)
                 if segment_start != -1:
                     break
                 # Otherwise, start a new segment check
                 segment_color = color
                 segment_start = i
                 segment_length = 1

        # If we were tracking a segment and hit a 0 or pivot, the segment ends
        elif segment_start != -1 and (color == 0 or (pivot_index is not None and i == pivot_index)):
            break # Segment ended

    if segment_start != -1:
        return segment_color, segment_start, segment_length
    else:
        return None # No segment found

def calculate_distance(grid: List[int], segment_start: int, segment_length: int, pivot_index: int) -> int:
    """Calculates the number of background (0) pixels between the segment and the pivot."""
    segment_end = segment_start + segment_length - 1
    distance = 0

    if segment_end < pivot_index: # Segment is to the left of the pivot
        # Count zeros between segment end and pivot start
        for i in range(segment_end + 1, pivot_index):
            if grid[i] == 0:
                distance += 1
    elif segment_start > pivot_index: # Segment is to the right of the pivot
        # Count zeros between pivot end and segment start
         for i in range(pivot_index + 1, segment_start):
            if grid[i] == 0:
                distance += 1
    # Else: segment is adjacent or overlapping? Assume examples prevent overlap.
    # If adjacent, distance is 0, which the loops correctly handle.

    return distance

def transform(input_grid: List[int]) -> List[int]:
    """
    Applies the transformation rule to move the segment across the pivot.
    """
    n = len(input_grid)
    # Initialize output grid with background color (0)
    output_grid = [0] * n

    # 1. Find the pivot
    pivot_index = find_pivot_index(input_grid)
    if pivot_index is None:
        # Should not happen based on task description, but handle defensively
        return input_grid # Or raise an error? Returning input for now.

    # 2. Place the pivot in the output grid
    output_grid[pivot_index] = 9

    # 3. Find the segment
    segment_info = find_segment(input_grid, pivot_index)
    if segment_info is None:
         # No segment found, maybe just return the grid with the pivot?
         # Based on examples, there's always a segment.
         return output_grid # Return grid with only pivot placed

    segment_color, segment_start, segment_length = segment_info
    segment_end = segment_start + segment_length - 1

    # 4. Calculate the distance between segment and pivot
    distance = calculate_distance(input_grid, segment_start, segment_length, pivot_index)

    # 5. Determine the new position for the segment
    new_segment_start = -1
    if segment_end < pivot_index: # Segment was to the left, move to the right
        new_segment_start = pivot_index + distance + 1
    elif segment_start > pivot_index: # Segment was to the right, move to the left
        new_segment_start = pivot_index - distance - segment_length

    # 6. Place the segment in the output grid at the new position
    # Check bounds (though examples suggest it will always fit)
    if new_segment_start >= 0 and new_segment_start + segment_length <= n:
        for i in range(segment_length):
            output_grid[new_segment_start + i] = segment_color
    else:
        # Handle error case: segment doesn't fit
        # This case shouldn't occur based on the symmetrical nature of the examples.
        print(f"Warning: Calculated new segment position {new_segment_start} with length {segment_length} is out of bounds for grid size {n}.")
        # Fallback: maybe just return the grid with the pivot? Or original?
        # Returning grid with just pivot for now.
        output_only_pivot = [0] * n
        output_only_pivot[pivot_index] = 9
        return output_only_pivot


    return output_grid