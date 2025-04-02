import numpy as np

"""
Transforms an input grid based on column position and pixel color.

1.  Pixels in columns 0 through 8 (the left section) are set to white (0).
2.  Pixels in columns 9 and greater (the right section) are modified based on their original color:
    - Green (3) pixels become gray (5).
    - Orange (7) pixels become gray (5).
    - All other pixel colors remain unchanged.
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    # Get the dimensions of the input grid
    height, width = input_grid.shape

    # Initialize the output grid as a copy of the input grid
    # This handles the cases where pixels in the right section don't change
    output_grid = np.copy(input_grid)

    # Iterate through each pixel of the grid
    for r in range(height):
        for c in range(width):
            # Check if the pixel is in the left section (columns 0-8)
            if c < 9:
                # Set the corresponding output pixel to white (0)
                output_grid[r, c] = 0
            # Check if the pixel is in the right section (columns 9 onwards)
            else:
                # Get the color of the input pixel
                input_color = input_grid[r, c]
                # Check if the input color needs replacement
                if input_color == 3 or input_color == 7:
                    # Set the corresponding output pixel to gray (5)
                    output_grid[r, c] = 5
                # Otherwise, the pixel retains its original color (already handled by the copy)

    return output_grid
