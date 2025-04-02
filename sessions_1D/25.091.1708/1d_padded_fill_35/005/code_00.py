import numpy as np

"""
Transformation Rule Natural Language Description:

1.  Receive the input grid. Determine its height (H) and width (W).
2.  Create a new output grid of the same dimensions (H x W), initialized entirely with the background color (white/0).
3.  Iterate through each row of the input grid, using a row index `R` from 0 to H-1.
4.  For the current input row at index `R`:
    a.  Scan the row from left to right (column index 0 to W-1) to find the first pixel that is not white (0), the "marker pixel".
    b.  If no marker pixel is found (the row is all white), the corresponding output row `R` remains all white.
    c.  If a marker pixel is found with color `C` at column index `I`:
        i.  Check if the current row index `R` is even or odd.
        ii. If `R` is even (R % 2 == 0):
            1. Fill the output grid's row `R` from column index `I` to the last column index (W-1) (inclusive) with color `C`.
        iii. If `R` is odd (R % 2 != 0):
            1. Fill the output grid's row `R` from column index 0 to column index `I` (inclusive) with color `C`.
5.  After processing all rows, return the completed output grid.
"""

def find_first_non_white_pixel(row):
    """
    Finds the index and color of the first non-white pixel in a row.

    Args:
        row (np.array): A 1D numpy array representing a grid row.

    Returns:
        tuple: (index, color) of the first non-white pixel, or (None, None) if the row is all white (color 0).
    """
    for index, color in enumerate(row):
        if color != 0: # 0 is the background/white color
            return index, color
    return None, None # No non-white pixel found

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the row-parity-based transformation rule to the input grid.
    """
    # Ensure input is a numpy array
    if not isinstance(input_grid, np.ndarray):
        input_grid = np.array(input_grid, dtype=int)
        
    # Get grid dimensions
    height, width = input_grid.shape
    
    # Initialize output_grid with the background color (white/0)
    output_grid = np.zeros_like(input_grid)
    
    # Iterate through each row of the input grid
    for r in range(height):
        # Get the current row
        input_row = input_grid[r, :]
        
        # Find the first non-white pixel (marker) in the current row
        marker_index, marker_color = find_first_non_white_pixel(input_row)
        
        # If a marker pixel was found
        if marker_index is not None:
            # Check if the row index is even or odd
            if r % 2 == 0:  # Even row index (0, 2, 4, ...)
                # Fill from marker index to the end of the row
                output_grid[r, marker_index:] = marker_color
            else:  # Odd row index (1, 3, 5, ...)
                # Fill from the beginning of the row up to and including the marker index
                output_grid[r, :marker_index + 1] = marker_color
        # Else (row was all white), the output row remains all white (already initialized)
            
    return output_grid
