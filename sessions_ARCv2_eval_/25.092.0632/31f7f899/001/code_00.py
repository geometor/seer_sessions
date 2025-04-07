import numpy as np
import copy

"""
Transforms the input grid based on vertical color propagation towards a horizontal separator line.

1. Identifies the background color (azure, 8) and the separator color (magenta, 6).
2. Locates the row index of the horizontal magenta (6) separator line.
3. Iterates through each column of the grid.
4. For each column:
    a. Finds the non-background, non-separator color closest to the separator line from above. If found, propagates this color downwards, replacing background pixels, until the row just above the separator line.
    b. Finds the non-background, non-separator color closest to the separator line from below. If found, propagates this color upwards, replacing background pixels, until the row just below the separator line.
5. The separator line itself remains unchanged.
"""

def transform(input_grid):
    """
    Applies the vertical color propagation transformation.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Define known colors
    background_color = 8
    separator_color = 6

    # Initialize output_grid as a copy of the input
    output_grid = copy.deepcopy(input_grid)
    height, width = output_grid.shape

    # Find the separator row
    separator_row = -1
    for r in range(height):
        if np.all(input_grid[r, :] == separator_color) or separator_color in input_grid[r, :]: # Check if the whole row or part of the row contains the separator color
             # More robust check: find the first row containing the separator color
             rows_with_separator = np.where(np.any(input_grid == separator_color, axis=1))[0]
             if len(rows_with_separator) > 0:
                 separator_row = rows_with_separator[0] # Assume the first occurrence is the separator line
                 break
    
    if separator_row == -1:
        # Handle cases where no separator is found (e.g., return input?)
        # For this specific task based on examples, a separator is always expected.
        # If not found, it might indicate an issue or an edge case not covered.
        # Let's assume it's always present based on training data.
        print("Warning: Separator row not found. Returning original grid.")
        return input_grid


    # Iterate through each column
    for c in range(width):
        # --- Process Above Separator ---
        color_above = None
        source_row_above = -1
        # Scan downwards from just above the separator to the top
        for r in range(separator_row - 1, -1, -1):
            pixel_color = input_grid[r, c]
            if pixel_color != background_color and pixel_color != separator_color:
                color_above = pixel_color
                source_row_above = r
                break # Found the closest color source above

        # If a color source was found above, propagate it downwards
        if color_above is not None:
            # Iterate from the source row up to (but not including) the separator row
            # In the original description, it says propagate *downwards*. Let's adjust.
            # Propagate from the found source row towards the separator
            # It should fill the background pixels between the source and the separator
            for r_fill in range(source_row_above + 1, separator_row):
                 if output_grid[r_fill, c] == background_color:
                     output_grid[r_fill, c] = color_above
            # Correction: The natural language said "Iterate from r = source_row_above up to separator_row - 1".
            # Let's re-read: "Propagate this color downwards, replacing background pixels, until the row just above the separator line."
            # This means fill from source_row_above + 1 to separator_row - 1.
            # Let's rethink the loop based on the *output* examples.
            # Example 1, col 1: gray(5) at (2,1) propagates down to row 5.
            # Example 1, col 6: red(2) at (3,6) propagates down to row 5.
            # Example 1, col 8: blue(1) at (5,8) propagates down to row 5.
            # It seems the color *below* the source gets filled.
            # Let's try filling from source_row_above + 1 to separator_row - 1
            for r_fill in range(source_row_above + 1, separator_row):
                 if output_grid[r_fill, c] == background_color:
                     output_grid[r_fill, c] = color_above


        # --- Process Below Separator ---
        color_below = None
        source_row_below = -1
        # Scan upwards from just below the separator to the bottom
        for r in range(separator_row + 1, height):
            pixel_color = input_grid[r, c]
            if pixel_color != background_color and pixel_color != separator_color:
                color_below = pixel_color
                source_row_below = r
                break # Found the closest color source below

        # If a color source was found below, propagate it upwards
        if color_below is not None:
            # Propagate upwards from the source row towards the separator
            # Fill background pixels between the source and the separator
            # Iterate from source_row_below - 1 down to separator_row + 1
            for r_fill in range(source_row_below - 1, separator_row, -1):
                 if output_grid[r_fill, c] == background_color:
                     output_grid[r_fill, c] = color_below

    return output_grid