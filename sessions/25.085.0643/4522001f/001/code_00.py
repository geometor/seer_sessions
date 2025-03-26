import numpy as np

"""
Transforms an input grid by scaling it up by a factor of 3 and applying specific color transformations.

Each pixel in the input grid is expanded into a 3x3 block in the output grid.
The color of the output block is determined by the color of the corresponding input pixel:
- White (0) input pixel becomes a 3x3 block of white (0).
- Green (3) input pixel becomes a 3x3 block of green (3).
- Red (2) input pixel becomes a 3x3 block of green (3).
"""

def transform(input_grid):
    """
    Applies the scaling and color transformation to the input grid.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # 1. Determine the height (H) and width (W) of the input grid.
    input_height, input_width = input_grid.shape

    # 2. Create a new output grid with dimensions (H * 3) rows and (W * 3) columns, initially filled with white (0).
    output_height = input_height * 3
    output_width = input_width * 3
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # 3. Iterate through each pixel of the input grid.
    for r in range(input_height):
        for c in range(input_width):
            # 4a. Identify its color.
            input_color = input_grid[r, c]

            # 4b. Determine the target color for the corresponding output block.
            target_color = 0 # Default to white
            if input_color == 0:
                target_color = 0 # white -> white
            elif input_color == 3:
                target_color = 3 # green -> green
            elif input_color == 2:
                target_color = 3 # red -> green

            # 4c. Identify the 3x3 block in the output grid.
            start_row = r * 3
            end_row = start_row + 3
            start_col = c * 3
            end_col = start_col + 3

            # 4d. Fill this 3x3 output block entirely with the determined target color.
            output_grid[start_row:end_row, start_col:end_col] = target_color

    # 5. Return the completed output grid.
    return output_grid