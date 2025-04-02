import numpy as np

"""
Transforms the input grid by identifying horizontally isolated, non-white pixels. 
Each identified isolated pixel becomes the center of a horizontal line of three 
pixels of the same color in the output grid. The expansion occurs by changing 
the pixel itself and its immediate left and right neighbors (if within bounds) 
to the color of the isolated pixel. Existing horizontal lines of three identical 
non-white pixels and background pixels remain unchanged unless overwritten by 
the expansion of an isolated pixel.

1. Initialize the output grid as a copy of the input grid.
2. Identify all horizontally isolated non-white pixels in the input grid. 
   A pixel at (r, c) with color C > 0 is isolated if:
   - Its left neighbor (r, c-1) either doesn't exist (c=0) or has a color different from C.
   - Its right neighbor (r, c+1) either doesn't exist (c=width-1) or has a color different from C.
3. Store the coordinates (r, c) and color C of these isolated pixels.
4. Iterate through the stored list of isolated pixels. For each isolated pixel (r, c) with color C:
   a. Set the pixel at (r, c) in the output grid to color C.
   b. If the left neighbor (r, c-1) exists (c > 0), set it to color C in the output grid.
   c. If the right neighbor (r, c+1) exists (c < width - 1), set it to color C in the output grid.
5. Return the modified output grid.
"""

def is_horizontally_isolated(grid, r, c):
    """Checks if a non-white pixel at (r, c) is horizontally isolated."""
    height, width = grid.shape
    pixel_color = grid[r, c]

    if pixel_color == 0:
        return False # Only check non-white pixels

    # Check left neighbor
    left_diff = True
    if c > 0:
        if grid[r, c - 1] == pixel_color:
            left_diff = False

    # Check right neighbor
    right_diff = True
    if c < width - 1:
        if grid[r, c + 1] == pixel_color:
            right_diff = False

    return left_diff and right_diff

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (np.ndarray): A 2D NumPy array representing the input grid.

    Returns:
        np.ndarray: A 2D NumPy array representing the transformed output grid.
    """
    # Get grid dimensions
    height, width = input_grid.shape

    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)

    # Find all isolated pixels in the *input* grid first
    isolated_pixels = []
    for r in range(height):
        for c in range(width):
            if is_horizontally_isolated(input_grid, r, c):
                isolated_pixels.append((r, c, input_grid[r, c])) # Store row, col, color

    # Apply the expansion transformation based on the identified isolated pixels
    for r, c, pixel_color in isolated_pixels:
        # Set the center pixel (already correct from copy, but explicit is fine)
        output_grid[r, c] = pixel_color

        # Set the left pixel if within bounds
        if c > 0:
            output_grid[r, c - 1] = pixel_color

        # Set the right pixel if within bounds
        if c < width - 1:
            output_grid[r, c + 1] = pixel_color

    return output_grid