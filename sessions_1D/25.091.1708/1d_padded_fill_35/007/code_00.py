import numpy as np

"""
Transformation Rule Natural Language Description:

1.  Determine the height (H) and width (W) of the input grid.
2.  Create an output grid of the same dimensions (H x W), initially filled with the background color (white/0).
3.  Iterate through each row of the input grid, using a row index `R` from 0 to H-1.
4.  For the current input row `R`:
    a.  Scan the row from left (column 0) to right (column W-1) to find the first pixel that is not white (0). Call this the "marker pixel".
    b.  If no marker pixel is found (the row is all white), leave the corresponding output row `R` as all white and proceed to the next input row.
    c.  If a marker pixel is found with color `C` at column index `I`:
        i.  Check if the row index `R` is even (`R % 2 == 0`).
        ii. If `R` is even: Fill the output grid's row `R` from column index `I` to the last column (W-1), inclusive, with color `C`.
        iii. If `R` is odd: Fill the output grid's row `R` from the first column (0) up to and including column index `I`, with color `C`.
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
    # Ensure input is a numpy array (it might be passed as a list of lists)
    if not isinstance(input_grid, np.ndarray):
        input_grid = np.array(input_grid, dtype=int)
        
    # Get grid dimensions: height (H) and width (W)
    height, width = input_grid.shape
    
    # Initialize output_grid with the same dimensions as the input, filled with background color (white/0)
    output_grid = np.zeros_like(input_grid)
    
    # Iterate through each row of the input grid using its index R
    for r in range(height):
        # Get the current row from the input grid
        input_row = input_grid[r, :]
        
        # Find the first non-white pixel (marker) in the current input row
        marker_index, marker_color = find_first_non_white_pixel(input_row)
        
        # Check if a marker pixel was actually found in this row
        if marker_index is not None:
            # Determine if the current row index R is even or odd
            is_even_row = (r % 2 == 0)
            
            if is_even_row:
                # For even rows, fill the corresponding output row from the marker's column index to the end
                output_grid[r, marker_index:] = marker_color
            else:
                # For odd rows, fill the corresponding output row from the beginning up to and including the marker's column index
                output_grid[r, :marker_index + 1] = marker_color
        # Else (no marker found), the output row remains all white (as initialized) - no action needed.
            
    # Return the completed output grid
    return output_grid