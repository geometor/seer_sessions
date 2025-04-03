"""
Filters horizontal segments in the first row based on whether any non-white pixel 
exists directly below them in the second row of the input grid. The second row 
of the output is always white (0).

1. Initialize an output grid of the same dimensions as the input, filled with white (0).
2. Identify all maximal contiguous horizontal segments of non-white pixels in the first row (row 0) of the input grid.
3. For each identified segment:
   a. Check the corresponding columns in the second row (row 1) of the input grid.
   b. If any pixel in the second row directly below the segment is non-white (value > 0), then copy the segment from the input's first row to the output's first row.
4. The second row of the output grid remains entirely white (as initialized).
5. Return the output grid.
"""

import numpy as np

def _find_horizontal_segments(row):
    """
    Identifies maximal contiguous horizontal segments of non-white pixels in a row.

    Args:
        row (np.array): A 1D numpy array representing a grid row.

    Returns:
        list: A list of tuples, where each tuple represents a segment:
              (color, start_col, end_col_exclusive).
              Returns an empty list if no non-white segments are found.
    """
    segments = []
    width = len(row)
    col = 0
    while col < width:
        if row[col] != 0:  # Start of a potential segment (non-white pixel)
            color = row[col]
            start_col = col
            # Find the end of the segment (where color changes or row ends)
            while col < width and row[col] == color:
                col += 1
            end_col_exclusive = col
            segments.append((int(color), start_col, end_col_exclusive))
            # col is already advanced past the segment, continue search from here
        else:
            col += 1 # Move to the next pixel if current is white
    return segments

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list): A list of lists representing the input grid (expected 2xN).

    Returns:
        list: A list of lists representing the output grid.
    """
    # Convert input to numpy array for easier slicing and operations
    input_np = np.array(input_grid, dtype=int)
    
    # Handle edge case of empty input
    if input_np.size == 0:
        return []
    if input_np.ndim == 1: # Ensure 2D if input was like [[...]]
         input_np = input_np.reshape(1, -1)

    height, width = input_np.shape

    # Based on examples, we expect 2 rows. Handle deviations if necessary.
    if height != 2:
        print(f"Warning: Input grid has {height} rows, expected 2. Processing based on first two rows.")
        # Or raise ValueError("Input grid must have exactly 2 rows.")

    # 1. Initialize output_grid with the same dimensions, filled with white (0)
    output_grid = np.zeros_like(input_np)

    # Extract the first and second rows of the input
    first_row_input = input_np[0, :]
    # Ensure second_row_input exists even if input height < 2 (though handled by warning above)
    second_row_input = input_np[1, :] if height >= 2 else np.zeros(width, dtype=int) 

    # 2. Identify segments in the first row of the input
    segments = _find_horizontal_segments(first_row_input)

    # 3. Iterate through segments, check for support, and copy if supported
    for color, start_col, end_col_exclusive in segments:
        # a. Define the segment slice in the second row to check for support
        support_slice = second_row_input[start_col:end_col_exclusive]
        
        # b. Check if any pixel in the support slice is non-white
        # np.any returns True if at least one element is True (non-zero for numbers)
        is_supported = np.any(support_slice != 0)

        # c. If supported, copy the segment to the output's first row
        if is_supported:
            output_grid[0, start_col:end_col_exclusive] = color
            
    # 4. The second row of the output grid remains white (as initialized)
    # No action needed here as output_grid[1, :] is already zeros.

    # 5. Convert the numpy array back to a list of lists and return
    return output_grid.tolist()