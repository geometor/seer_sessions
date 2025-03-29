```python
import numpy as np

"""
Vertically flips horizontal bands of the grid if the pattern within the band is 
not vertically symmetric. A band is defined as a maximal contiguous set of one 
or more rows where all non-background pixels share the same single color. 
Bands are separated by rows containing only background pixels (0) or rows 
containing pixels of multiple different non-background colors.
"""

def _get_bands(grid):
    """
    Identifies maximal vertical bands of uniform non-background color.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list[dict]: A list of dictionaries, where each dictionary represents a band 
                    and contains 'color' (int) and 'rows' (list of ints).
                    Returns an empty list if no bands are found.
    """
    rows, cols = grid.shape
    bands = []
    current_band_color = -1 # -1: no active band, 0: background/mixed row
    start_row = 0
    
    for r in range(rows):
        # Find unique non-background colors in the current row
        unique_colors = np.unique(grid[r, :])
        non_background_colors = unique_colors[unique_colors != 0]
        
        current_row_color_type = -1 # Default: mixed colors or error
        if len(non_background_colors) == 1:
            current_row_color_type = non_background_colors[0] # Single non-background color
        elif len(non_background_colors) == 0:
             current_row_color_type = 0 # Pure background row
        # else: mixed colors, keep -1
             
        # --- State machine for band detection ---
        if r == 0:
            # First row initializes the state
            if current_row_color_type > 0: # Start of a potential band
                 current_band_color = current_row_color_type
                 start_row = r
            # If background/mixed, current_band_color remains -1 (no active band)
        else:
            # Subsequent rows
            if current_band_color > 0: 
                # Currently inside a band of color `current_band_color`
                if current_row_color_type == current_band_color:
                    # Row continues the current band, do nothing
                    pass
                else: 
                    # Row breaks the current band (different color, background, or mixed)
                    # Finalize the previous band
                    bands.append({"color": current_band_color, "rows": list(range(start_row, r))})
                    # Check if this row starts a new band
                    if current_row_color_type > 0:
                        current_band_color = current_row_color_type
                        start_row = r
                    else: # Background or mixed row, reset band state
                        current_band_color = -1 
            else: 
                # Not currently in a band (last row was background/mixed or start)
                if current_row_color_type > 0: # Start a new band
                    current_band_color = current_row_color_type
                    start_row = r
                # else: Still background/mixed, remain outside a band

    # After loop, check if the last rows formed a band that needs to be added
    if current_band_color > 0:
        bands.append({"color": current_band_color, "rows": list(range(start_row, rows))})
        
    return bands

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid by identifying uniform color vertical bands and 
    flipping the rows within a band if the band's pattern is not vertically 
    symmetric.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    
    # Initialize output_grid as a copy of the input grid.
    # Modifications will be applied based on band symmetry.
    output_grid = np.copy(input_grid)
    
    # Identify all maximal vertical color bands.
    bands = _get_bands(input_grid)
    
    # Iterate through each identified band.
    for band in bands:
        # Get the row indices for the band.
        rows = band["rows"]
        if not rows: # Skip if somehow an empty band was generated
             continue
             
        min_row = rows[0]
        max_row = rows[-1]
        
        # Extract the grid slice corresponding to the band's rows.
        input_slice = input_grid[min_row : max_row + 1, :]
        
        # Check if the extracted slice is vertically symmetric.
        # A slice is symmetric if it's identical to its vertically flipped version.
        # Note: Single row slices are always symmetric.
        flipped_slice_for_check = np.flipud(input_slice)
        is_symmetric = np.array_equal(input_slice, flipped_slice_for_check)
        
        # If the slice is NOT vertically symmetric, flip it in the output grid.
        if not is_symmetric:
            # Use the already computed flipped slice
            output_grid[min_row : max_row + 1, :] = flipped_slice_for_check
            
        # If the slice IS vertically symmetric, do nothing, as the output_grid 
        # already contains the original (unflipped) rows from the initial copy.
            
    return output_grid
```