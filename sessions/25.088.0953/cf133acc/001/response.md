```python
import numpy as np

"""
Transforms the input grid based on horizontal and vertical segments.

1.  Identify vertical segments: For each non-white pixel at (r, c) with color C in the input, project color C leftwards across the output grid in row r, from column 0 up to and including column c.
2.  Identify horizontal segments: For each non-white pixel at (r, c) with color C in the input, project color C downwards across the output grid in column c, from row 0 down to and including row r. Downward projections overwrite leftward projections where they overlap.
3.  Restore original non-white pixels: Any pixel that was non-white in the input grid retains its original color in the output grid, overwriting any projections at that specific location.
"""

def transform(input_grid):
    """
    Applies the transformation rules to the input grid.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    input_grid = np.array(input_grid)
    height, width = input_grid.shape
    output_grid = np.zeros_like(input_grid) # Initialize with white (0)

    # Step 1: Perform Leftward Projections (from vertical segments/pixels)
    # Iterate through each pixel of the input grid
    for r in range(height):
        for c in range(width):
            color = input_grid[r, c]
            # If the pixel is not white
            if color != 0:
                # Fill the output grid row 'r' from column 0 up to 'c' (inclusive) with this color
                # This effectively projects the color leftwards from its vertical position
                output_grid[r, 0:c+1] = color

    # Step 2: Perform Downward Projections (from horizontal segments/pixels)
    # Iterate through each pixel of the input grid again
    for r in range(height):
        for c in range(width):
            color = input_grid[r, c]
            # If the pixel is not white
            if color != 0:
                # Fill the output grid column 'c' from row 0 down to 'r' (inclusive) with this color
                # This effectively projects the color downwards from its horizontal position
                # This overwrites any color placed by the leftward projection in Step 1
                output_grid[0:r+1, c] = color

    # Step 3: Restore Original Non-White Pixels
    # Iterate through each pixel one last time
    for r in range(height):
        for c in range(width):
            original_color = input_grid[r, c]
            # If the original pixel was not white
            if original_color != 0:
                # Ensure the output grid at this exact position has the original color
                # This overwrites any projection color at the pixel's specific location
                output_grid[r, c] = original_color

    return output_grid.tolist() # Return as list of lists per ARC format
```