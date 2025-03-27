import numpy as np

"""
Processes an input grid based on horizontal segments of non-white pixels.
1. Copies the input grid to create an output grid.
2. Iterates through the grid to find horizontal segments of non-white pixels.
3. If a white pixel (0) is immediately to the left of the start of a segment, that pixel in the output grid takes the color of the segment.
4. The rightmost pixel of a segment in the output grid is changed to gray (5) if it's at the right grid edge or if the pixel immediately to its right in the input grid was white (0).
5. After processing segments, any remaining white pixels (0) in the output grid are changed to gray (5).
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rules based on horizontal segments.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # --- Step 1: Process Left Expansion ---
    # Iterate through rows and columns (starting from the second column)
    for r in range(height):
        for c in range(1, width):
            # Check if current pixel is non-white and the one to its left is white
            if input_grid[r, c] > 0 and input_grid[r, c - 1] == 0:
                # Apply the segment's color to the white pixel on the left in the output grid
                output_grid[r, c - 1] = input_grid[r, c]

    # --- Step 2: Process Right Termination ---
    # Iterate through rows and columns
    for r in range(height):
        for c in range(width):
            # Check if the current pixel in the input is part of a segment
            if input_grid[r, c] > 0:
                # Determine if this pixel is the end of a segment
                is_end_of_segment = False
                if c == width - 1:  # Is it at the right edge?
                    is_end_of_segment = True
                elif input_grid[r, c + 1] == 0: # Is the pixel to the right white?
                    is_end_of_segment = True

                # If it's the end of the segment, change its color to gray in the output grid
                if is_end_of_segment:
                    output_grid[r, c] = 5

    # --- Step 3: Fill Background ---
    # Change any remaining white (0) pixels to gray (5)
    output_grid[output_grid == 0] = 5

    return output_grid