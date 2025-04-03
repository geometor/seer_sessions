```python
"""
Identifies all horizontal contiguous segments of azure (8) pixels across all rows 
of the input 2D grid. Determines the segment with the overall maximum length. If 
multiple segments share this maximum length, the one encountered first during a 
top-to-bottom, left-to-right scan is chosen. Changes the color of all pixels 
within this single chosen segment from azure (8) to orange (7) in the output grid. 
All other pixels remain unchanged.
"""

import numpy as np
import copy

def find_longest_azure_segment(input_grid):
    """
    Finds the single longest horizontal segment of azure (8) pixels in the grid.

    Args:
        input_grid (np.array): The 2D input grid.

    Returns:
        tuple: A tuple containing (row, start_col, end_col, length) for the 
               longest segment, or None if no azure segments are found.
               In case of ties in length, returns the first one encountered.
    """
    max_len = 0
    longest_segment_details = None
    rows, cols = input_grid.shape

    # Iterate through each row
    for r in range(rows):
        in_segment = False
        start_col = -1
        # Iterate through columns in the current row
        for c in range(cols):
            pixel = input_grid[r, c]
            # Start of a new azure segment
            if pixel == 8 and not in_segment:
                in_segment = True
                start_col = c
            # End of the current azure segment (found non-azure pixel or end of row)
            elif (pixel != 8 or c == cols - 1) and in_segment:
                in_segment = False
                # Determine the end column index correctly
                end_col = c - 1 if pixel != 8 else c 
                length = end_col - start_col + 1
                
                # Check if this segment is the new longest or ties the first longest
                if length > max_len:
                    max_len = length
                    longest_segment_details = (r, start_col, end_col, length)
                # Implicitly handles tie-breaking: only update if strictly greater,
                # so the first one found with max_len is kept.
                
    return longest_segment_details


def transform(input_grid):
    """
    Transforms the input grid by finding the globally longest horizontal segment 
    of azure (8) pixels and changing its color to orange (7).
    """
    # Find the details of the longest azure segment
    longest_segment_info = find_longest_azure_segment(input_grid)

    # Create a copy of the input grid to modify
    output_grid = np.copy(input_grid) # Use np.copy for numpy arrays

    # If a longest segment was found, recolor it
    if longest_segment_info:
        r, start_col, end_col, _ = longest_segment_info
        # Iterate through the columns of the longest segment in the specific row
        for c in range(start_col, end_col + 1):
             # Ensure we only change azure pixels (safety check)
             if output_grid[r, c] == 8:
                output_grid[r, c] = 7 # Change color to orange

    # Return the modified grid (or the original copy if no segment was found)
    return output_grid
```