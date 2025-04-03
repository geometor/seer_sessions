import numpy as np
from typing import Tuple, Optional

"""
Transformation Rule:
Identify a unique pivot element (color 9) and a single contiguous segment of another color (non-0, non-9) within a 1D numpy array.
Move the segment to the opposite side of the pivot, preserving the number of background (0) pixels originally separating the segment and the pivot.
The pivot's position remains unchanged, as do the segment's color and length. The remaining positions in the array are filled with the background color (0).
"""

def find_pivot(grid: np.ndarray) -> Optional[int]:
    """
    Locates the index of the pivot element (9).

    Args:
        grid: The 1D input numpy array.

    Returns:
        The index of the pivot element (9), or None if not found.
    """
    pivot_indices = np.where(grid == 9)[0]
    if len(pivot_indices) == 1:
        return int(pivot_indices[0]) # Convert from np.int64 if needed
    return None

def find_segment(grid: np.ndarray, pivot_index: Optional[int]) -> Optional[Tuple[int, int, int]]:
    """
    Finds the contiguous segment of non-0, non-9 color.

    Args:
        grid: The 1D input numpy array.
        pivot_index: The index of the pivot element, or None.

    Returns:
        A tuple containing (segment_color, segment_start_index, segment_length),
        or None if no valid segment is found.
    """
    # Find indices of all potential segment cells (non-zero and not the pivot)
    mask = (grid != 0)
    if pivot_index is not None:
        mask &= (np.arange(len(grid)) != pivot_index)
        
    segment_indices = np.where(mask)[0]

    if len(segment_indices) == 0:
        return None # No segment cells found

    # Check for contiguity: differences between consecutive indices should all be 1
    if len(segment_indices) > 1 and not np.all(np.diff(segment_indices) == 1):
        # Found multiple segments or non-contiguous cells matching criteria,
        # which violates task constraints based on examples.
        # Assuming the first contiguous block is the target.
        # Find the first index where the difference is not 1
        diffs = np.diff(segment_indices)
        split_point = np.where(diffs != 1)[0]
        if len(split_point) > 0:
             # Take only the indices before the first break
             segment_indices = segment_indices[:split_point[0] + 1]
        # If still not contiguous after this refinement, there's an issue
        if len(segment_indices) > 1 and not np.all(np.diff(segment_indices) == 1):
             print("Warning: Could not isolate a single contiguous segment.")
             return None # Or handle error differently

    segment_start = int(segment_indices[0])
    segment_length = len(segment_indices)
    segment_color = int(grid[segment_start]) # Get color from the first cell

    return segment_color, segment_start, segment_length

def calculate_distance(grid: np.ndarray, segment_start: int, segment_length: int, pivot_index: int) -> int:
    """
    Calculates the number of background (0) pixels between the segment and the pivot.

    Args:
        grid: The 1D input numpy array.
        segment_start: The starting index of the segment.
        segment_length: The length of the segment.
        pivot_index: The index of the pivot element.

    Returns:
        The count of background (0) pixels between the segment and pivot.
    """
    segment_end = segment_start + segment_length - 1
    distance = 0

    if segment_end < pivot_index: # Segment is to the left
        # Slice between segment end (exclusive) and pivot index (exclusive)
        sub_array = grid[segment_end + 1 : pivot_index]
        distance = np.sum(sub_array == 0)
    elif segment_start > pivot_index: # Segment is to the right
        # Slice between pivot index (exclusive) and segment start (exclusive)
        sub_array = grid[pivot_index + 1 : segment_start]
        distance = np.sum(sub_array == 0)
    # Else: segment is adjacent, distance is 0, handled correctly by slicing

    return int(distance) # Ensure standard int return


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to move the segment across the pivot.

    Args:
        input_grid: A 1D numpy array representing the input state.

    Returns:
        A 1D numpy array representing the transformed state.
    """
    n = len(input_grid)
    # Initialize output grid with background color (0)
    output_grid = np.zeros_like(input_grid)

    # 1. Find the pivot
    pivot_index = find_pivot(input_grid)
    if pivot_index is None:
        print("Warning: Pivot element (9) not found.")
        return output_grid # Return empty grid or input_grid? Returning empty for now.

    # 2. Place the pivot in the output grid
    output_grid[pivot_index] = 9

    # 3. Find the segment
    segment_info = find_segment(input_grid, pivot_index)
    if segment_info is None:
        print("Warning: No valid segment found.")
        # Return grid with only the pivot placed
        return output_grid

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
    else:
        # This case (segment adjacent or overlapping pivot) shouldn't occur based on examples.
        # If it did, the logic might need adjustment depending on desired behavior.
        print("Warning: Segment is adjacent to pivot? This case might not be fully handled.")
        # Assuming move to other side still applies. If adjacent left, move right; if adjacent right, move left.
        if segment_end == pivot_index -1: # adjacent left
             new_segment_start = pivot_index + 1
        elif segment_start == pivot_index + 1: # adjacent right
             new_segment_start = pivot_index - segment_length
        else: # Overlap - error state
            print("Error: Segment overlaps pivot.")
            return output_grid # return grid with just pivot


    # 6. Place the segment in the output grid at the new position
    # Check bounds before placing
    if 0 <= new_segment_start < n and new_segment_start + segment_length <= n:
        output_grid[new_segment_start : new_segment_start + segment_length] = segment_color
    else:
        print(f"Warning: Calculated new segment position {new_segment_start} with length {segment_length} is out of bounds for grid size {n}.")
        # Return grid with only the pivot placed as a fallback
        output_grid_fallback = np.zeros_like(input_grid)
        output_grid_fallback[pivot_index] = 9
        return output_grid_fallback

    return output_grid