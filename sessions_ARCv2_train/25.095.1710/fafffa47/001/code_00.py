import numpy as np

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms a 6x3 input grid into a 3x3 output grid based on element-wise comparison.

    The input grid consists of two 3x3 grids stacked vertically.
    The upper 3x3 grid contains values 0 and 9.
    The lower 3x3 grid contains values 0 and 1.

    The transformation rule is applied element-wise:
    1. If the value in the upper grid cell is 9, the output cell value is 0.
    2. Else if the value in the lower grid cell is 1, the output cell value is 0.
    3. Else if the value in the upper grid cell is 0 AND the value in the lower grid cell is 0, the output cell value is 2.
    4. Otherwise (implicitly covered by rules 1 and 2), the output cell is 0.
    """

    # Convert input list of lists to a NumPy array for easier slicing
    input_array = np.array(input_grid)

    # Separate the input into upper and lower 3x3 grids
    upper_grid = input_array[:3, :]
    lower_grid = input_array[3:, :]

    # Get the dimensions (should be 3x3)
    rows, cols = upper_grid.shape

    # Initialize the output grid with zeros
    output_grid = np.zeros((rows, cols), dtype=int)

    # Iterate through each cell position (row i, column j)
    for i in range(rows):
        for j in range(cols):
            # Get the values from the corresponding cells in the upper and lower grids
            upper_val = upper_grid[i, j]
            lower_val = lower_grid[i, j]

            # Apply the transformation logic
            if upper_val == 9:
                output_grid[i, j] = 0  # Rule 1
            elif lower_val == 1:
                output_grid[i, j] = 0  # Rule 2
            elif upper_val == 0 and lower_val == 0:
                output_grid[i, j] = 2  # Rule 3
            # else: # Rule 4 (implicit - already initialized to 0)
            #   output_grid[i, j] = 0

    # Convert the NumPy output array back to a list of lists before returning
    return output_grid.tolist()
