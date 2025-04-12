import numpy as np

"""
Scales the input grid by a factor of 3. Each pixel in the input grid determines the 
color of a corresponding 3x3 block in the output grid. If the input pixel color 
is red (2), the corresponding 3x3 output block is filled with white (0). Otherwise, 
the 3x3 output block is filled with the input pixel's color.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms an input grid by scaling it 3x and applying a color replacement rule.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    input_np = np.array(input_grid, dtype=int)
    input_height, input_width = input_np.shape

    # Calculate output dimensions
    output_height = input_height * 3
    output_width = input_width * 3

    # Initialize output grid with white (0)
    # Using white as the default handles the red (2) -> white (0) case automatically
    # if we only overwrite for non-red colors.
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through each pixel of the input grid
    for r in range(input_height):
        for c in range(input_width):
            input_color = input_np[r, c]

            # Determine the color for the output block
            # If input is red (2), output block remains white (0) as initialized.
            # Otherwise, output block takes the input color.
            if input_color != 2:
                output_color = input_color

                # Define the top-left corner of the 3x3 block in the output grid
                start_row = r * 3
                start_col = c * 3

                # Fill the 3x3 block in the output grid
                for i in range(3):
                    for j in range(3):
                        output_grid[start_row + i, start_col + j] = output_color

    # Convert back to list of lists for the expected output format
    return output_grid.tolist()