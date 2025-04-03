import numpy as np
from typing import Tuple, Optional

"""
Transformation Rule:
Identifies a unique pivot element (color 9) and a single contiguous horizontal segment of another color (non-0, non-9) within the same row of a 2D numpy grid.
The segment is then moved horizontally to the opposite side of the pivot element within that row, while maintaining the exact same number of background pixels (color 0) horizontally separating the segment and the pivot column as existed in the input grid.
The pivot's position remains fixed. The segment's color and length (width) remain unchanged. All other positions in the output grid are filled with the background color (0). The output grid has the same dimensions as the input grid.
"""

def find_pivot(grid: np.ndarray) -> Optional[Tuple[int, int]]:
    """
    Locates the coordinates (row, column) of the pivot element (9).

    Args:
        grid: The 2D input numpy array.

    Returns:
        A tuple (row, column) of the pivot, or None if not found or multiple pivots exist.
    """
    pivot_coords = np.argwhere(grid == 9)
    if len(pivot_coords) == 1:
        # Return standard Python ints for coordinates
        return int(pivot_coords[0, 0]), int(pivot_coords[0, 1])
    elif len(pivot_coords) == 0:
        print("Warning: Pivot element (9) not found.")
        return None
    else:
        print(f"Warning: Expected 1 pivot (9), found {len(pivot_coords)}. Coordinates: {pivot_coords}")
        return None # Ambiguous which pivot to use

def find_horizontal_segment_in_row(grid: np.ndarray, row_index: int, pivot_col: int) -> Optional[Tuple[int, int, int, int]]:
    """
    Finds the single contiguous horizontal segment of non-0, non-9 color in the specified row.

    Args:
        grid: The 2D input numpy array.
        row_index: The row index to search within.
        pivot_col: The column index of the pivot (to ignore).

    Returns:
        A tuple containing (segment_color, start_col, end_col, length),
        or None if no single valid segment is found in that row.
    """
    row_data = grid[row_index, :]
    segment_color = -1
    start_col = -1
    current_length = 0
    found_segment = None # Store potential segment info here

    for col_index, color in enumerate(row_data):
        # Skip background and the pivot itself
        if color == 0 or col_index == pivot_col:
            if start_col != -1:
                # End of a potential segment
                if found_segment is not None:
                     # Found a second segment after already finding one - error
                     print(f"Warning: Found multiple segments in row {row_index}. Previous: {found_segment}, current ends at col {col_index-1}.")
                     return None # Violates single segment assumption
                found_segment = (segment_color, start_col, col_index - 1, current_length)
                # Reset for searching next potential segment (though we expect only one)
                start_col = -1
                current_length = 0
            continue # Move to next column

        # Found a non-background, non-pivot color
        current_color = int(color)

        if start_col == -1:
            # Start of a new potential segment
            segment_color = current_color
            start_col = col_index
            current_length = 1
        elif current_color == segment_color:
            # Continuation of the current segment
            current_length += 1
        else:
            # Found a different color, ending the previous segment
            if found_segment is not None:
                 print(f"Warning: Found multiple segments or colors in row {row_index}.")
                 return None # Violates assumption
            found_segment = (segment_color, start_col, col_index - 1, current_length)
            # Start tracking the new color segment immediately
            segment_color = current_color
            start_col = col_index
            current_length = 1

    # Check if a segment was ongoing when the row ended
    if start_col != -1:
        if found_segment is not None:
             print(f"Warning: Found multiple segments in row {row_index} (one ending at grid edge).")
             return None
        found_segment = (segment_color, start_col, grid.shape[1] - 1, current_length)

    if found_segment is None:
        print(f"Warning: No valid segment found in row {row_index}.")

    return found_segment


def calculate_horizontal_distance(grid: np.ndarray, row_index: int, start_col: int, end_col: int, pivot_col: int) -> int:
    """
    Calculates the number of background (0) pixels horizontally between the segment and the pivot.

    Args:
        grid: The 2D input numpy array.
        row_index: The row index where segment and pivot reside.
        start_col: The starting column index of the segment.
        end_col: The ending column index of the segment.
        pivot_col: The column index of the pivot element.

    Returns:
        The count of background (0) pixels strictly between the segment and pivot column.
    """
    distance = 0
    row_data = grid[row_index, :]

    if end_col < pivot_col: # Segment is to the left
        # Count zeros between segment end (exclusive) and pivot col (exclusive)
        sub_array = row_data[end_col + 1 : pivot_col]
        distance = np.sum(sub_array == 0)
    elif start_col > pivot_col: # Segment is to the right
        # Count zeros between pivot col (exclusive) and segment start (exclusive)
        sub_array = row_data[pivot_col + 1 : start_col]
        distance = np.sum(sub_array == 0)
    # Else: segment is adjacent, distance is 0, handled correctly by slicing

    return int(distance) # Ensure standard int return


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule: moves a colored horizontal segment to the
    opposite side of a pivot (color 9) within the same row, preserving the
    horizontal count of background (0) pixels between them.
    """
    # Ensure input is a numpy array
    if not isinstance(input_grid, np.ndarray):
        input_grid = np.array(input_grid)

    # Basic validation for 2D grid
    if input_grid.ndim != 2:
        print("Error: Input grid must be 2-dimensional.")
        # Return input or empty? Returning input shape filled with 0s.
        return np.zeros_like(input_grid)

    rows, cols = input_grid.shape
    # Initialize output grid with background color (0)
    output_grid = np.zeros((rows, cols), dtype=input_grid.dtype)

    # 1. Find the pivot element (color 9)
    pivot_coords = find_pivot(input_grid)
    if pivot_coords is None:
        # Error message printed in helper, return empty grid
        return output_grid

    pivot_row, pivot_col = pivot_coords

    # 2. Place the pivot in the output grid at its fixed position
    output_grid[pivot_row, pivot_col] = 9

    # 3. Find the contiguous horizontal segment in the pivot's row
    segment_info = find_horizontal_segment_in_row(input_grid, pivot_row, pivot_col)
    if segment_info is None:
        # Warning printed in helper, return grid with only pivot placed
        return output_grid

    segment_color, segment_start_col, segment_end_col, segment_length = segment_info

    # 4. Calculate the horizontal distance (number of 0s) between segment and pivot
    distance = calculate_horizontal_distance(input_grid, pivot_row, segment_start_col, segment_end_col, pivot_col)

    # 5. Determine the new starting column for the segment on the opposite side
    new_segment_start_col = -1
    if segment_end_col < pivot_col: # Segment was to the left, move to the right
        new_segment_start_col = pivot_col + distance + 1
    elif segment_start_col > pivot_col: # Segment was to the right, move to the left
        new_segment_start_col = pivot_col - distance - segment_length
    else:
        # Should not happen if segment/pivot validation is correct and they don't overlap/touch
        print("Error: Segment appears adjacent to or overlapping pivot, cannot determine move direction.")
        return output_grid # Return grid with just pivot

    # 6. Place the segment in the output grid at the new position
    # Check if the calculated new position is valid and within bounds
    new_segment_end_col = new_segment_start_col + segment_length
    if 0 <= new_segment_start_col < cols and new_segment_end_col <= cols:
        output_grid[pivot_row, new_segment_start_col : new_segment_end_col] = segment_color
    else:
        print(f"Warning: Calculated new segment position col:[{new_segment_start_col}:{new_segment_end_col}] in row {pivot_row} is out of bounds for grid cols {cols}.")
        # Fallback: Return grid with only the pivot placed if segment doesn't fit
        output_grid_fallback = np.zeros_like(input_grid)
        output_grid_fallback[pivot_row, pivot_col] = 9
        return output_grid_fallback

    # 7. Return the completed output grid
    return output_grid