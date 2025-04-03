```python
import numpy as np

"""
Keep only the endpoints of a horizontal contiguous segment of non-white color, turning the interior points white.

1. Scan the input row to find the contiguous sequence of non-white pixels (the colored segment).
2. Determine the color of this segment.
3. Record the column index of the first pixel of the segment (start index).
4. Record the column index of the last pixel of the segment (end index).
5. Create a new output row with the same length as the input row, and fill it completely with white pixels (0).
6. In the output row, place the recorded segment color at the recorded start index.
7. In the output row, place the recorded segment color at the recorded end index.
8. Return the modified output row.
"""

def find_non_white_segment(row):
    """Finds the start index, end index, and color of the first contiguous non-white segment in a row."""
    start_index = -1
    end_index = -1
    segment_color = 0  # Default to white if no segment found

    for i, pixel in enumerate(row):
        if pixel != 0:  # Found a non-white pixel
            if start_index == -1:  # Start of a new segment
                start_index = i
                segment_color = pixel
            end_index = i # Keep updating end_index as long as we are in the segment
        elif start_index != -1: # We found white after a segment started, segment ends
             break # Assuming only one segment per row based on examples

    return start_index, end_index, segment_color

def transform(input_grid):
    """
    Transforms the input grid by keeping only the endpoints of the horizontal non-white segment.
    Assumes the input is a 1xN grid (a single row).
    """
    # Ensure input is treated as a numpy array
    input_np = np.array(input_grid)

    # Get the dimensions
    rows, cols = input_np.shape

    # Initialize output_grid with the same shape, filled with white (0)
    output_grid = np.zeros_like(input_np)

    # Since the examples only show transformations on the first row (or imply a single row input)
    # We will process the first row. If there were multiple rows, the logic might need adjustment.
    if rows > 0:
        input_row = input_np[0, :] # Get the first (and only) row

        # Find the non-white segment in the row
        start_index, end_index, segment_color = find_non_white_segment(input_row)

        # If a segment was found (start_index is not -1)
        if start_index != -1:
            # Place the segment color at the start index in the output grid
            output_grid[0, start_index] = segment_color
            # Place the segment color at the end index in the output grid
            # This naturally handles segments of length 1 where start_index == end_index
            output_grid[0, end_index] = segment_color

    return output_grid.tolist() # Return as a list of lists

```