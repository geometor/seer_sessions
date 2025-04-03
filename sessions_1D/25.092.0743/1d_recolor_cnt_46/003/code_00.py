import numpy as np

"""
This transformation rule operates on a 1-dimensional grid represented as a 1xN NumPy array.
It identifies contiguous horizontal segments of magenta pixels (color 6) against a white background (color 0).
Each magenta segment is then replaced by a segment of the same length, but with a new color determined by the length of the original magenta segment:
- Segments of length 1 are replaced with green (color 3).
- Segments of length 2 are replaced with blue (color 1).
- Segments of length 3 are replaced with yellow (color 4).
White pixels remain unchanged and are copied to the output.
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid by replacing magenta segments based on their length.

    Args:
        input_grid: A 1xN NumPy array representing the input grid row.

    Returns:
        A 1xN NumPy array representing the transformed output grid row.
    """
    # Ensure input is a 2D numpy array, even if it was passed as 1D list/array
    if input_grid.ndim == 1:
        input_grid = np.array([input_grid])
        
    # Get the dimensions (expecting 1 row)
    rows, cols = input_grid.shape
    
    if rows != 1:
        # This rule is defined for single-row inputs
        # Handle error or adapt if necessary for multi-row inputs
        # For now, let's assume it works row by row if multiple rows are given,
        # though the examples only show 1 row.
        # If strictly 1 row is required, raise ValueError("Input must have exactly one row.")
        pass # Or handle multi-row case if needed

    # Initialize output_grid as a NumPy array of zeros with the same shape
    output_grid = np.zeros_like(input_grid)

    # Iterate through the columns of the single row
    i = 0
    while i < cols:
        # Get the color of the current pixel
        current_pixel = input_grid[0, i]

        if current_pixel == 0:
            # If the pixel is white (background), copy it directly
            # output_grid is already initialized with 0, so we can just advance
            i += 1
        elif current_pixel == 6:
            # If the pixel is magenta, find the length of the contiguous segment
            start_index = i
            length = 0
            # Iterate forward as long as we are within bounds and find magenta pixels
            while i < cols and input_grid[0, i] == 6:
                length += 1
                i += 1 # Move main loop index forward

            # Determine the replacement color based on the segment length
            replacement_color = 0 # Default to white if length doesn't match rules
            if length == 1:
                replacement_color = 3 # Green for length 1
            elif length == 2:
                replacement_color = 1 # Blue for length 2
            elif length == 3:
                replacement_color = 4 # Yellow for length 3
            # Note: Other lengths will result in the segment being replaced by white (0)

            # Fill the corresponding segment in the output grid with the replacement color
            # Use NumPy slicing for efficiency
            if length > 0: # Ensure we only write if a segment was found
                 output_grid[0, start_index : start_index + length] = replacement_color
            # The index 'i' is already positioned at the pixel *after* the segment
        else:
            # Handle any other unexpected pixel colors (e.g., copy them)
            # Based on examples, only 0 and 6 appear in input.
            output_grid[0, i] = current_pixel # Copy unexpected colors
            i += 1
            
    return output_grid