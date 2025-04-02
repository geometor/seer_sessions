import numpy as np

"""
Transforms a 1D grid (represented as a 1xN array) by expanding isolated 
non-white pixels horizontally into a sequence of three identical pixels. 

Specifically:
1.  Creates a copy of the input grid.
2.  Iterates through each pixel of the input grid.
3.  If a pixel is non-white (color C) and its immediate left and right neighbors 
    (if they exist within the grid bounds) are *not* color C, then this pixel 
    is considered "isolated".
4.  For each isolated pixel found at index `i`, the corresponding pixel at `i` 
    in the output grid, as well as its left neighbor (`i-1`, if `i>0`) and 
    right neighbor (`i+1`, if `i<width-1`), are set to color C.
5.  Pixels in the output grid that are not part of an expansion (i.e., 
    original white pixels or non-white pixels that were already adjacent to 
    pixels of the same color) retain their original color from the input grid copy.
6.  Returns the modified output grid.
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A 1xN numpy array representing the input grid row.

    Returns:
        A 1xN numpy array representing the transformed output grid row.
    """
    # Ensure input is a numpy array
    if not isinstance(input_grid, np.ndarray):
        input_grid = np.array(input_grid)

    # Get grid dimensions (assuming 1 row)
    height, width = input_grid.shape
    if height != 1:
        # This implementation assumes a single row based on examples
        # Could be adapted for multiple rows if needed, but sticking to pattern
        raise ValueError("Input grid must have exactly one row.")

    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)

    # Iterate through each pixel column in the single row
    for i in range(width):
        current_color = input_grid[0, i]

        # Skip background/white pixels
        if current_color == 0:
            continue

        # Check if the current non-white pixel is isolated
        is_isolated = True

        # Check left neighbor (handle boundary condition i=0)
        if i > 0 and input_grid[0, i - 1] == current_color:
            is_isolated = False

        # Check right neighbor (handle boundary condition i=width-1)
        if i < width - 1 and input_grid[0, i + 1] == current_color:
            is_isolated = False

        # If the pixel is isolated, expand it in the output grid
        if is_isolated:
            # Set the center pixel (already correct from copy, but explicit)
            # output_grid[0, i] = current_color 
            
            # Set the left pixel, checking boundary
            if i > 0:
                output_grid[0, i - 1] = current_color
                
            # Set the right pixel, checking boundary
            if i < width - 1:
                output_grid[0, i + 1] = current_color
            
            # Note: The center pixel output_grid[0, i] retains its color 
            # from the initial copy. The logic covers cases where i=0 or i=width-1 
            # correctly by only modifying existing neighbours.

    # Return the modified grid
    return output_grid