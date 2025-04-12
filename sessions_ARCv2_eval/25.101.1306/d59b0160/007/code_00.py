import numpy as np
import copy

"""
Transforms an input grid based on a row-specific condition determined by the pixel color in column index 2 (the 'control column'). The transformation affects only the pixels to the right of column index 3 (the 'separator column').

The rule, derived primarily from inconsistent observations across examples and representing a hypothesis that failed validation, is as follows:
1. Identify the background color (orange, 7) and white color (0).
2. Identify the control column index (2) and the separator column index (3).
3. Create an output grid by copying the input grid.
4. Iterate through each row `r`.
5. Get the color of the control pixel: `control_color = input[r, 2]`.
6. Check the control condition:
   - If `control_color` is NEITHER the background color (7) NOR white (0), then modify the output grid for row `r`: Set all pixels in columns `c > 3` to the background color (7).
   - If `control_color` IS the background color (7) OR white (0), make no changes to the output grid for row `r` in columns `c > 3`.
7. Pixels in columns `c <= 3` always retain their original input color.
8. Return the modified output grid.

Note: This rule failed validation against the provided training examples, indicating the true transformation logic is different or more complex. Example 1, in particular, deviates significantly.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies a hypothesized transformation rule based on the control pixel in column 2.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid according to the
        hypothesized (but incorrect) rule.
    """
    # Convert input to a numpy array for efficient slicing and modification
    input_np = np.array(input_grid, dtype=int)

    # Initialize the output grid as a copy of the input grid
    output_np = np.copy(input_np)

    # Define constants based on observations (background color, significant colors/columns)
    background_color = 7
    white_color = 0
    control_column_index = 2
    separator_column_index = 3

    # Get grid dimensions
    num_rows, num_cols = input_np.shape

    # Iterate through each row to apply the row-dependent rule
    for r in range(num_rows):
        # Ensure the control column exists before attempting access
        if control_column_index < num_cols:
            # Get the color of the control pixel for this row
            control_pixel_color = input_np[r, control_column_index]

            # Check the hypothesized condition:
            # if the control pixel is NOT background AND NOT white
            if control_pixel_color != background_color and control_pixel_color != white_color:
                # Modify the right region (columns > separator_column_index)
                # Set all pixels in this region of the output grid to the background color
                # Check if there are columns to the right of the separator
                if separator_column_index + 1 < num_cols:
                     output_np[r, separator_column_index + 1:] = background_color
            # else: (control_pixel_color == background_color or control_pixel_color == white_color)
                # If the control pixel IS background or white, according to this hypothesis,
                # do nothing to the right region. The output row already contains
                # the correct copied values from the input.
                pass
        # else: handle case where grid is too narrow for the control column index
            # No action needed as the output is already a copy

    # Convert the result back to a list of lists format
    output_grid = output_np.tolist()

    return output_grid