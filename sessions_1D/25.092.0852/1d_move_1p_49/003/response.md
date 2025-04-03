```python
"""
Transforms the input grid (a single row 2D numpy array) by shifting the single contiguous horizontal segment of non-white pixels one position to the right.
The background is white (0). The segment retains its color and length.
The position vacated by the segment's leftmost pixel becomes white.
"""

import numpy as np

def find_horizontal_segment(row):
    """
    Finds the start index, end index, and color of the first contiguous non-zero segment in a 1D numpy array.

    Args:
        row (np.array): A 1D numpy array representing a row of pixels.

    Returns:
        tuple: A tuple containing (start_index, end_index, segment_color).
               Returns (None, None, None) if no non-zero segment is found.
    """
    start_index = -1
    end_index = -1
    segment_color = 0
    in_segment = False
    for i, pixel in enumerate(row):
        # Found the start of a non-zero segment
        if pixel != 0 and not in_segment:
            start_index = i
            segment_color = pixel
            in_segment = True
            end_index = i # Initialize end_index
        # Still inside the non-zero segment
        elif pixel != 0 and in_segment:
            # Ensure all pixels in the segment have the same color (as per observation)
            # Although the examples don't violate this, it's good practice
            if pixel == segment_color:
                end_index = i
            else:
                # Found a different color, segment ends here.
                # This case shouldn't happen based on examples.
                break
        # Found the first zero pixel *after* being in a segment
        elif pixel == 0 and in_segment:
            break # Segment ended
        # Else: pixel is 0 and we are not in a segment (before the segment) - continue scanning

    if start_index == -1: # No segment was found
        return None, None, None

    return start_index, end_index, segment_color

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Shifts the horizontal non-white segment in the single-row input grid one step right.

    Args:
        input_grid (np.ndarray): A 2D numpy array with shape (1, width).

    Returns:
        np.ndarray: A new 2D numpy array with the segment shifted right.
    """
    # Get the dimensions (height should be 1) and initialize output_grid
    height, width = input_grid.shape
    output_grid = np.zeros_like(input_grid) # Initialize with background color 0

    # Operate on the first (and only) row
    input_row = input_grid[0]

    # Find the non-white segment in the input row
    start_index, end_index, segment_color = find_horizontal_segment(input_row)

    # If a segment is found, proceed with the shift
    if start_index is not None:
        # Calculate the new start and end positions for the shifted segment
        new_start_index = start_index + 1
        new_end_index = end_index + 1

        # Check if the entire shifted segment fits within the grid width
        if new_end_index < width:
            # Copy the segment to the new position in the output grid's first row
            # Iterate using the original indices and write to the offset position.
            for i in range(start_index, end_index + 1):
                 output_grid[0, i + 1] = segment_color
        else:
            # Handle the case where the segment might shift partially off the grid
            # Copy only the parts that fit within the bounds.
             for i in range(start_index, end_index + 1):
                 new_pos = i + 1
                 if new_pos < width:
                     output_grid[0, new_pos] = segment_color
            # Note: Based on examples, the segment always fits after shifting.

    # If no segment was found, output_grid remains all zeros, which is correct.
    # If the input was all zeros, the output is also all zeros.

    return output_grid
```