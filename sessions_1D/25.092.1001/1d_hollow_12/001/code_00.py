import numpy as np

"""
Identify horizontal segments of non-white pixels in each row. For segments longer 
than two pixels, keep only the first and last pixel of the segment, turning 
the interior pixels white (0). Segments of length 1 or 2 remain unchanged. 
Pixels outside any segment also remain unchanged.
"""

def find_horizontal_segments(row_array):
    """
    Finds contiguous horizontal segments of non-white pixels in a 1D numpy array.

    Args:
        row_array: A 1D numpy array representing a row of the grid.

    Returns:
        A list of tuples, where each tuple contains the (start_col, end_col)
        indices of a non-white segment.
    """
    segments = []
    start_col = -1
    n_cols = len(row_array)

    for col_idx, pixel in enumerate(row_array):
        is_non_white = pixel != 0
        
        # Start of a new segment
        if is_non_white and start_col == -1:
            start_col = col_idx

        # End of the current segment (found white pixel or end of row)
        if (not is_non_white or col_idx == n_cols - 1) and start_col != -1:
            # Determine the correct end column index
            end_col = col_idx -1 if not is_non_white else col_idx
            segments.append((start_col, end_col))
            start_col = -1 # Reset for the next potential segment
            
    return segments

def transform(input_grid):
    """
    Transforms the input grid by hollowing out horizontal segments.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    n_rows, n_cols = output_grid.shape

    # Iterate through each row of the grid
    for r in range(n_rows):
        current_row = output_grid[r, :]
        
        # Find all non-white horizontal segments in the current row
        segments = find_horizontal_segments(current_row)
        
        # Process each found segment
        for start_col, end_col in segments:
            segment_length = end_col - start_col + 1
            
            # If the segment is longer than 2 pixels, hollow it out
            if segment_length > 2:
                # Iterate through the interior columns of the segment
                for c in range(start_col + 1, end_col):
                    # Set the interior pixel to white (0) in the output grid
                    output_grid[r, c] = 0
                    
    # Return the modified grid
    return output_grid
