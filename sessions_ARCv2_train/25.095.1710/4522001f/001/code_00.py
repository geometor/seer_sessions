import numpy as np

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Upscales a grid by a factor of 3 and transforms cell values.

    Creates a new output grid with dimensions three times larger than the input grid.
    Iterates through each cell of the input grid.
    Determines the value of the input cell.
    Identifies the corresponding 3x3 block in the output grid.
    If the input value is 0, fills the output block with 0.
    If the input value is non-zero, fills the output block with 3.
    Returns the completed output grid.
    """

    # Convert input to numpy array for easier handling
    input_array = np.array(input_grid, dtype=int)
    input_height, input_width = input_array.shape

    # Calculate output dimensions
    output_height = input_height * 3
    output_width = input_width * 3

    # Initialize output grid with zeros
    output_array = np.zeros((output_height, output_width), dtype=int)

    # Iterate through each cell of the input grid
    for r in range(input_height):
        for c in range(input_width):
            # Get the value from the input cell
            input_value = input_array[r, c]

            # Determine the value to fill the output block
            # If input is 0, output is 0; otherwise, output is 3
            output_value = 0 if input_value == 0 else 3

            # Calculate the start coordinates for the 3x3 block in the output grid
            start_row = r * 3
            start_col = c * 3

            # Fill the corresponding 3x3 block in the output grid
            # Slicing makes this efficient with numpy
            output_array[start_row:start_row + 3, start_col:start_col + 3] = output_value

    # Convert the numpy array back to a list of lists for the return type
    output_grid = output_array.tolist()

    return output_grid
