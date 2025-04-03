Warning: Response generation stopped. Finish Reason: MAX_TOKENS (2)
Partial text available:
---
```python
"""
Transforms the input grid based on the following rule:
In each row, find all horizontal contiguous segments of azure (8) pixels.
Identify the segment with the maximum length in that row.
If this maximum length is 4 or greater AND there is exactly one segment
with this maximum length in the row, change the color of the pixels
belonging to that specific segment to maroon (9). Otherwise, the row
remains unchanged.
"""

import numpy as np

def find_segments(row, color):
    """
    Finds contiguous segments of a given color in a 1D array (row).

    Args:
        row (np.array): A 1D numpy array representing a row of the grid.
        color (int): The color value to find segments of.

    Returns:
        list: A list of dictionaries, where each dictionary represents a segment
              and contains 'start' (column index), 'end' (column index, exclusive),
              and 'length'. Returns an empty list if no segments are found.
    """
    segments = []
    start_col = -1
    # Iterate through each pixel in the row along with its column index
    for col, pixel in enumerate(row):
        # Check if the current pixel matches the target color and we are not already inside a segment
        if pixel == color and start_col == -1:
            # Mark the start of a new segment
            start_col = col
        # Check if the current pixel does *not* match the target color and we *were* inside a segment
        elif pixel != color and start_col != -1:
            # Mark the end of the current segment
            length = col - start_col # Calculate segment length
            # Store the segment's start, end (exclusive), and length
            segments.append({'start': start_col, 'end': col, 'length': length})
            # Reset start_col to indicate we are no longer inside a segment
            start_col = -1

    # After the loop, check if a segment was ongoing and reached the end of the row
    if start_col != -1:
        # Calculate the length of the segment ending at the row's end
        length = len(row) - start_col
        # Store this final segment
        segments.append({'start': start_col, 'end': len(row), 'length': length})

    return segments

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input_grid to a numpy array for efficient processing
    # Use int dtype explicitly if input might contain non-integers, although ARC uses 0-9
    input_grid_np = np.array(input_grid, dtype=int) 
    # Create a copy to store the output, preserving the original input_grid
    output_grid = np.copy(input_grid_np
---
