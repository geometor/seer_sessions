import numpy as np

"""
Transforms a 1D grid by changing the color of contiguous red (2) segments based on their length.
- Segments of size 1 become orange (7).
- Segments of size 2 become maroon (9).
- Segments of size 3 become magenta (6).
- White (0) pixels remain unchanged.
"""

def transform(input_grid):
    """
    Applies a color transformation to red segments in a 1D grid based on segment length.

    Args:
        input_grid (list of lists): A 2D list representing the input grid (expected height 1).

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input grid
    output_grid = grid.copy()
    
    rows, cols = grid.shape
    
    # Since the grid is effectively 1D (height 1), we iterate through columns
    if rows != 1:
        # This implementation assumes a 1-row grid based on examples
        # Handle potential errors or adapt if multi-row inputs are possible
        print("Warning: Expected input grid height of 1.")
        # For now, process only the first row if more than one exists
        # Or return input if logic is strictly for 1D
        # return input_grid 
        pass # Continue processing the first row

    col = 0
    while col < cols:
        # Check if the current pixel is red (2)
        if grid[0, col] == 2:
            # Found the start of a potential red segment
            start_col = col
            segment_size = 0
            # Find the end of the contiguous red segment
            while col < cols and grid[0, col] == 2:
                segment_size += 1
                col += 1
            
            # Determine the output color based on segment size
            output_color = 0 # Default or error color if needed
            if segment_size == 1:
                output_color = 7 # Orange
            elif segment_size == 2:
                output_color = 9 # Maroon
            elif segment_size == 3:
                output_color = 6 # Magenta
            # Note: if segment_size is other than 1, 2, or 3, 
            # the original red pixels will remain in the output
            # unless we explicitly handle other cases (e.g., set to 0 or keep red).
            # Based on examples, only sizes 1, 2, 3 occur.
            # If a valid output color was determined, apply it
            if output_color != 0:
                 output_grid[0, start_col:col] = output_color
            
            # col is already advanced to the position after the segment,
            # so the loop continues correctly
        else:
            # If the pixel is not red (it's white), move to the next column
            col += 1
            
    # Convert the numpy array back to a list of lists for the expected output format
    return output_grid.tolist()
