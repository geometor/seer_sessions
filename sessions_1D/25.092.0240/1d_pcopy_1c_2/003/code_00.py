"""
Transforms a 2D input grid by modifying horizontal segments within each row independently.
Specifically, it identifies contiguous horizontal segments of non-white pixels in each row.
If a segment consists of only a single pixel, the transformation attempts to extend it 
to the right into a 1x3 segment of the same color. This extension only occurs if the 
two pixels immediately to the right of the single pixel are within the grid boundaries 
and were both white (0) in the original input grid. Segments initially longer than 
one pixel are left unchanged. The process is applied row by row, based on the state 
of the input grid.
"""

import numpy as np
from typing import List, Tuple

def find_segments_in_row(row: np.ndarray) -> List[Tuple[int, int, int]]:
    """
    Identifies contiguous horizontal segments of non-white pixels in a 1D array (row).

    Args:
        row: A 1D numpy array representing a single row of the grid.

    Returns:
        A list of tuples, where each tuple represents a segment
        (color, start_col_index, length). Returns an empty list if no non-white
        pixels are found.
    """
    segments = []
    n_cols = len(row)
    c = 0
    while c < n_cols:
        # Check for the start of a non-white segment
        if row[c] != 0:
            color = row[c]
            start_col = c
            j = c + 1
            # Find the end of the segment
            while j < n_cols and row[j] == color:
                j += 1
            length = j - start_col
            segments.append((int(color), start_col, length))
            # Move index past the found segment
            c = j
        else:
            # Move to the next pixel if current is white
            c += 1
    return segments

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list of lists of integers representing the input 2D grid.

    Returns:
        A list of lists of integers representing the transformed output 2D grid.
    """
    # Convert input list of lists to a numpy array
    input_np = np.array(input_grid, dtype=int)
    
    # Initialize output grid as a copy of the input
    output_np = input_np.copy()
    
    # Get grid dimensions
    n_rows, n_cols = input_np.shape

    # Iterate through each row of the grid
    for r in range(n_rows):
        # Get the current row from the input grid
        current_input_row = input_np[r, :]
        
        # Find all non-white segments in this row of the input grid
        segments = find_segments_in_row(current_input_row)

        # Process each segment found in the row
        for color, start_col, length in segments:
            # Check if the segment is a single pixel
            if length == 1:
                # Define the columns to check for potential expansion
                col_plus_1 = start_col + 1
                col_plus_2 = start_col + 2

                # Check boundary conditions for expansion (need two spots to the right)
                if col_plus_1 < n_cols and col_plus_2 < n_cols:
                    # Check if the two pixels to the right in the *original input row* are white (0)
                    if current_input_row[col_plus_1] == 0 and current_input_row[col_plus_2] == 0:
                        # If conditions met, apply the extension in the corresponding output row
                        output_np[r, col_plus_1] = color
                        output_np[r, col_plus_2] = color
            # else: segment length > 1, no action needed as it's already copied correctly

    # Convert the result back to a list of lists before returning
    return output_np.tolist()