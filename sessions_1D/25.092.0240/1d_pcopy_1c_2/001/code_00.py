"""
Transforms an input grid (represented as a 1D array) based on the length of contiguous non-white segments.

1.  Create a copy of the input grid to serve as the initial output grid.
2.  Identify all contiguous horizontal segments of non-white pixels within the input grid. For each segment, note its color, starting index, and length.
3.  Iterate through the identified segments.
4.  For each segment:
    a.  If the segment's length is exactly 1:
        i.  Get the index `P` of this single pixel and its color `C`.
        ii. Check if positions `P+1` and `P+2` are within the grid boundaries.
        iii. Check if the pixels at positions `P+1` and `P+2` in the *original input grid* are both white (color 0).
        iv. If both boundary and color checks are met, update the *output grid* by setting the pixels at positions `P+1` and `P+2` to the color `C`.
    b.  If the segment's length is greater than 1, no changes are made for this segment.
5.  Return the modified output grid.
"""

import numpy as np
from typing import List, Tuple

def find_segments(row: np.ndarray) -> List[Tuple[int, int, int]]:
    """
    Identifies contiguous horizontal segments of non-white pixels in a 1D array.

    Args:
        row: A 1D numpy array representing a row of the grid.

    Returns:
        A list of tuples, where each tuple represents a segment
        (color, start_index, length).
    """
    segments = []
    n = len(row)
    i = 0
    while i < n:
        # Check for the start of a non-white segment
        if row[i] != 0:
            color = row[i]
            start_index = i
            j = i + 1
            # Find the end of the segment
            while j < n and row[j] == color:
                j += 1
            length = j - start_index
            segments.append((color, start_index, length))
            # Move index past the found segment
            i = j
        else:
            # Move to the next pixel if current is white
            i += 1
    return segments

def transform(input_grid: List[int]) -> List[int]:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list of integers representing the input grid (1D).

    Returns:
        A list of integers representing the transformed output grid (1D).
    """
    # Convert input list to numpy array for easier handling
    inp_arr = np.array(input_grid, dtype=int)
    
    # Initialize output grid as a copy of the input
    output_arr = inp_arr.copy()
    
    # Get the dimensions (length) of the 1D grid
    n = len(inp_arr)

    # Find all non-white segments in the input grid
    segments = find_segments(inp_arr)

    # Process each segment based on its length
    for color, start_index, length in segments:
        # If the segment length is 1
        if length == 1:
            # Check boundary conditions for extension (need two spots to the right)
            if start_index + 1 < n and start_index + 2 < n:
                # Check if the two pixels to the right in the *original* input are white
                if inp_arr[start_index + 1] == 0 and inp_arr[start_index + 2] == 0:
                    # Apply the extension in the output grid
                    output_arr[start_index + 1] = color
                    output_arr[start_index + 2] = color
        # If segment length is greater than 1, no action needed as it's already copied

    # Convert the result back to a list before returning
    return output_arr.tolist()
