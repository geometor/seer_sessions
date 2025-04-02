import numpy as np

"""
Transformation Rule Natural Language Description:

1.  Identify the dimensions (height H, width W) of the input grid.
2.  Create an output grid of the same dimensions, initialized entirely with white (0).
3.  Process the input grid row by row.
4.  For each row in the input grid:
    a.  Scan the row from left to right (column 0 to W-1) to find the first non-white pixel (the "marker pixel").
    b.  If no marker pixel is found (the row is all white), the corresponding output row remains all white.
    c.  If a marker pixel is found at column index `I` with color `C`:
        i.  Check if the marker pixel is in the very last column (i.e., if `I == W-1`).
        ii. If the marker pixel *is* in the last column (`I == W-1`), color *only* the pixel at index `I` in the corresponding output row with the marker color `C`.
        iii. If the marker pixel is *not* in the last column (`I < W-1`), fill the corresponding output row from column index `I` to the end (column W-1) with the marker color `C`. The pixels before index `I` in the output row remain white.
5.  Return the completed output grid.
"""

def find_first_non_white_pixel(row):
    """
    Finds the index and color of the first non-white pixel in a row.

    Args:
        row (np.array): A 1D numpy array representing a grid row.

    Returns:
        tuple: (index, color) of the first non-white pixel, or (None, None) if the row is all white.
    """
    for index, color in enumerate(row):
        if color != 0: # 0 is the background/white color
            return index, color
    return None, None # No non-white pixel found

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input grid.
    
    Args:
        input_grid (np.ndarray): The 2D input grid.
        
    Returns:
        np.ndarray: The 2D transformed output grid.
    """
    # Ensure input is a numpy array (might be list of lists)
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
            # Check if the marker is in the last column
            if marker_index == width - 1:
                # Color only the marker pixel itself in the output row
                output_grid[r, marker_index] = marker_color
            else:
                # Fill the output row from the marker index onwards
                output_grid[r, marker_index:] = marker_color
        # Else (row was all white), the output row remains all white (already initialized)
            
    return output_grid