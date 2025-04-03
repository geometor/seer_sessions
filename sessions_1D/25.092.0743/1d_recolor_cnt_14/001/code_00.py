import numpy as np

"""
This module transforms an input grid by replacing contiguous horizontal segments 
of azure (8) pixels with different colors based on the length of the segment.

Transformation rules:
- Segments of length 1 are replaced with maroon (9).
- Segments of length 2 are replaced with green (3).
- Segments of length 3 are replaced with red (2).
- White (0) pixels remain unchanged.
"""

def transform(input_grid):
    """
    Transforms the input grid based on the lengths of contiguous azure segments.

    Args:
        input_grid (list of lists or numpy array): The input grid containing 0s and 8s.

    Returns:
        numpy array: The transformed grid with segments replaced by corresponding colors.
    """
    # Convert input to numpy array for easier processing
    grid = np.array(input_grid)
    # Initialize output grid with the same shape and filled with white (0)
    output_grid = np.zeros_like(grid)
    
    # Since the grid is 1xN, we can work with the first row directly
    row = grid[0]
    n = len(row)
    i = 0
    
    # Iterate through the row to find segments of azure (8) pixels
    while i < n:
        if row[i] == 8:
            # Found the start of a potential segment
            start_index = i
            segment_length = 0
            # Count the length of the contiguous azure segment
            while i < n and row[i] == 8:
                segment_length += 1
                i += 1
            # Determine the replacement color based on segment length
            output_color = 0 # Default to white just in case (shouldn't happen with logic)
            if segment_length == 1:
                output_color = 9 # Maroon
            elif segment_length == 2:
                output_color = 3 # Green
            elif segment_length == 3:
                output_color = 2 # Red
            # else: # Handle segments of other lengths if necessary (not specified in examples)
                # output_color = row[start_index] # Or keep original color? Or white?
                # Based on examples, only lengths 1, 2, 3 occur and are transformed.

            # Fill the corresponding positions in the output grid row
            if output_color != 0: # Only fill if a valid transformation color was found
                 output_grid[0, start_index:i] = output_color
        else:
            # If the pixel is not azure, just move to the next pixel
            # The output grid is already initialized to white (0)
            i += 1
            
    return output_grid.tolist() # Return as list of lists per ARC standard
