import numpy as np

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms a 4x4 input grid by taking the values from the central 2x2 subgrid 
    (cells at (1,1), (1,2), (2,1), (2,2)) and placing them into the corner cells 
    of a new 4x4 output grid ((0,0), (0,3), (3,0), (3,3) respectively). 
    All other cells in the output grid are filled with 0.

    Args:
        input_grid: A 4x4 list of lists representing the input grid.

    Returns:
        A 4x4 list of lists representing the transformed output grid.
    """
    # Get the dimensions of the input grid (assuming it's always 4x4 based on examples)
    rows = len(input_grid)
    cols = len(input_grid[0]) if rows > 0 else 0

    # Initialize a new 4x4 output grid with all zeros
    # Using numpy for easier grid manipulation, but can be done with lists too
    output_grid_np = np.zeros((rows, cols), dtype=int)

    # Extract the values from the central 2x2 subgrid of the input grid
    # (using 0-based indexing)
    val_1_1 = input_grid[1][1]
    val_1_2 = input_grid[1][2]
    val_2_1 = input_grid[2][1]
    val_2_2 = input_grid[2][2]

    # Place the extracted values into the corner positions of the output grid
    output_grid_np[0, 0] = val_1_1  # Top-left corner gets value from input (1,1)
    output_grid_np[0, 3] = val_1_2  # Top-right corner gets value from input (1,2)
    output_grid_np[3, 0] = val_2_1  # Bottom-left corner gets value from input (2,1)
    output_grid_np[3, 3] = val_2_2  # Bottom-right corner gets value from input (2,2)

    # Convert the numpy array back to a list of lists for the return type
    output_grid = output_grid_np.tolist()

    return output_grid
