import numpy as np
from collections import Counter

"""
Transformation rule:
1. Create an output grid with 3 rows and the same width as the input grid.
2. Copy the first row (row 0) of the input grid to the first row (row 0) of the output grid.
3. Copy the second row (row 1) of the input grid to the second row (row 1) of the output grid.
4. Determine the 'background' color by finding the color of the second pixel (index 1) in the second row (index 1) of the input grid.
5. Determine the 'foreground' color by finding the color in the first row (row 0) of the input grid that is not the 'background' color.
6. Generate the third row (row 2) of the output grid: Iterate through the first row of the input grid. If a pixel's color matches the 'background' color, keep it. If it matches the 'foreground' color, replace it with magenta (6).
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the output grid.
    """
    # Get dimensions
    input_height, input_width = input_grid.shape

    # Initialize output_grid with 3 rows and same width
    output_grid = np.zeros((3, input_width), dtype=int)

    # Step 2: Copy the first row of the input to the first row of the output
    output_grid[0, :] = input_grid[0, :]

    # Step 3: Copy the second row of the input to the second row of the output
    output_grid[1, :] = input_grid[1, :]

    # Step 4: Identify the background color from the second pixel of the second row
    # Based on examples, the second pixel [1, 1] seems sufficient to identify background
    background_color = input_grid[1, 1]

    # Step 5: Identify the foreground color from the first row
    foreground_color = -1 # Initialize with an invalid color
    for color in input_grid[0, :]:
        if color != background_color:
            foreground_color = color
            break # Found the foreground color

    # Handle case where only background color exists in the first row (though unlikely based on examples)
    if foreground_color == -1:
         foreground_color = background_color # Or handle as an error/edge case

    # Step 6: Generate the third row of the output grid
    for col_index in range(input_width):
        pixel_color = input_grid[0, col_index]
        if pixel_color == background_color:
            output_grid[2, col_index] = background_color
        elif pixel_color == foreground_color:
            output_grid[2, col_index] = 6 # Replace with magenta
        else:
            # This case shouldn't happen based on the logic, but good to consider
            # If other colors exist, they are treated like background in examples
             output_grid[2, col_index] = pixel_color # Keep original color if neither FG nor BG

    return output_grid