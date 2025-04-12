import numpy as np

"""
Scales a 3x3 input grid to a 9x9 output grid. Each cell in the input grid 
corresponds to a 3x3 block in the output grid. If the input cell value is 0, 
the corresponding output block is filled with 0s. If the input cell value is 
non-zero, the corresponding output block is filled with 3s.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms an input grid according to the scaling and mapping rule.

    Args:
        input_grid: A 3x3 list of lists representing the input grid.

    Returns:
        A 9x9 list of lists representing the transformed output grid.
    """
    # Get dimensions of the input grid
    input_height = len(input_grid)
    input_width = len(input_grid[0]) if input_height > 0 else 0

    # Define the scaling factor
    scale_factor = 3

    # Calculate dimensions of the output grid
    output_height = input_height * scale_factor
    output_width = input_width * scale_factor

    # Initialize the output grid with zeros
    # Using numpy for easier initialization, but will convert back to list of lists
    output_grid_np = np.zeros((output_height, output_width), dtype=int)

    # Iterate through each cell of the input grid
    for r in range(input_height):
        for c in range(input_width):
            # Get the value from the input grid cell
            input_value = input_grid[r][c]

            # Determine the fill value for the output block
            # If input_value is 0, fill_value is 0
            # If input_value is non-zero, fill_value is 3
            fill_value = 0 if input_value == 0 else 3

            # Calculate the top-left coordinates for the corresponding block in the output grid
            output_r_start = r * scale_factor
            output_c_start = c * scale_factor

            # Fill the corresponding 3x3 block in the output grid
            for i in range(scale_factor):
                for j in range(scale_factor):
                    output_grid_np[output_r_start + i, output_c_start + j] = fill_value

    # Convert the numpy array back to a list of lists for the return value
    output_grid = output_grid_np.tolist()

    return output_grid
