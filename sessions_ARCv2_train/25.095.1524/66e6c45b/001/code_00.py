import numpy as np

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms a 4x4 input grid by moving the values from the central 2x2
    subgrid to the corners of a new 4x4 grid, filling the rest with zeros.

    Specifically:
    - Input[1][1] maps to Output[0][0]
    - Input[1][2] maps to Output[0][3]
    - Input[2][1] maps to Output[3][0]
    - Input[2][2] maps to Output[3][3]
    """

    # Determine grid dimensions (assuming square grid from examples)
    # Although examples are 4x4, let's try to be slightly more general
    # if possible, but the core logic is fixed to the 4x4 structure.
    # For this specific task, 4x4 is fixed.
    rows = 4
    cols = 4

    # Initialize output_grid as a 4x4 grid filled with zeros
    # Using numpy for potentially easier array manipulation, though list comprehensions work too.
    output_grid_np = np.zeros((rows, cols), dtype=int)

    # Perform transformations: Map central 2x2 block to corners
    # Input[1][1] -> Output[0][0]
    output_grid_np[0, 0] = input_grid[1][1]

    # Input[1][2] -> Output[0][3]
    output_grid_np[0, 3] = input_grid[1][2]

    # Input[2][1] -> Output[3][0]
    output_grid_np[3, 0] = input_grid[2][1]

    # Input[2][2] -> Output[3][3]
    output_grid_np[3, 3] = input_grid[2][2]

    # Convert numpy array back to list of lists for the return type
    output_grid = output_grid_np.tolist()

    return output_grid
