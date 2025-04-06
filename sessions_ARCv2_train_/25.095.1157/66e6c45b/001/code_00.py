import numpy as np

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms a 4x4 input grid by moving the values from the central 2x2 block
    (rows 1-2, columns 1-2) to the four corner positions of a new 4x4 grid,
    filling the rest with zeros.
    - Input (1,1) goes to Output (0,0)
    - Input (1,2) goes to Output (0,3)
    - Input (2,1) goes to Output (3,0)
    - Input (2,2) goes to Output (3,3)
    """
    # Assume input is always 4x4 based on examples
    rows = 4
    cols = 4

    # 1. Create a new 4x4 grid initialized with all zeros; this will be the output grid.
    # Using numpy for easier grid creation, but could use nested lists too
    output_grid = np.zeros((rows, cols), dtype=int)

    # Perform transformations by mapping central block elements to corners
    # 2. Copy the value from the input grid at position (row 1, column 1) to the output grid at position (row 0, column 0).
    output_grid[0, 0] = input_grid[1][1]

    # 3. Copy the value from the input grid at position (row 1, column 2) to the output grid at position (row 0, column 3).
    output_grid[0, 3] = input_grid[1][2]

    # 4. Copy the value from the input grid at position (row 2, column 1) to the output grid at position (row 3, column 0).
    output_grid[3, 0] = input_grid[2][1]

    # 5. Copy the value from the input grid at position (row 2, column 2) to the output grid at position (row 3, column 3).
    output_grid[3, 3] = input_grid[2][2]

    # 6. Return the modified output grid.
    # Convert back to list of lists if required by the interface
    return output_grid.tolist()
