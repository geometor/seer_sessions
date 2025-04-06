import numpy as np # Using numpy for easier grid initialization, but can be done with lists
import math # Math library is available, though not used in this specific logic

"""
Transforms a 12x4 input grid (represented as a list of lists) into a 6x4 output grid.
The input logically consists of two 6x4 grids stacked vertically.
Grid A: Input rows 0-5. Contains values 0 and 3.
Grid B: Input rows 6-11. Contains values 0 and 5.
The transformation rule is applied element-wise to produce the 6x4 output grid:
For each position (r, c) in the 6x4 grid:
- If the value in Grid A at (r, c) is 3 OR the value in Grid B at (r, c) is 5,
  the output value at (r, c) is 4.
- Otherwise, the output value at (r, c) is 0.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the element-wise transformation rule to combine two logical 6x4
    grids from the 12x4 input into a single 6x4 output grid.
    """

    # Assume input_grid is a list of 12 lists, each with 4 integers.
    # Extract dimensions for clarity, expecting 12 rows, 4 columns.
    input_rows = len(input_grid)
    if input_rows == 0:
        return [] # Handle empty input case
    input_cols = len(input_grid[0])

    # Define the dimensions of the logical grids and the output grid.
    output_rows = 6
    output_cols = 4 # Based on problem examples

    # Check if input dimensions match expectations (12x4)
    if input_rows != 12 or input_cols != 4:
        # Handle potential dimension mismatches, e.g., raise error or log warning.
        # For now, we'll proceed assuming the core logic might still apply
        # if the first 6 and next 6 rows exist.
        # This behavior might need adjustment based on stricter requirements.
        print(f"Warning: Expected input dimensions 12x4, but received {input_rows}x{input_cols}.")
        # Adjust output rows if input is too short, ensuring we don't index out of bounds.
        output_rows = min(output_rows, input_rows // 2)
        if output_rows == 0 and input_rows > 0 : # if there is input but less than 2 rows
             output_rows = 1 # default to at least one row if possible
        if input_rows < 6 : # If grid A is not complete
             pass # allow partial processing if desired, check logic below

    # Initialize the output grid with zeros. Using numpy for concise initialization.
    # Can be replaced with: output_grid = [[0 for _ in range(output_cols)] for _ in range(output_rows)]
    output_grid = np.zeros((output_rows, output_cols), dtype=int).tolist()

    # Iterate through each cell position (row r, column c) of the output grid.
    for r in range(output_rows):
         # Ensure we don't access grid B beyond the actual input rows
        if r + output_rows >= input_rows:
             break # Stop if we can't access the corresponding row in the second half

        for c in range(output_cols):
            # Get the corresponding values from the two logical input grids.
            # Grid A value is at input_grid[r][c]
            # Grid B value is at input_grid[r + output_rows][c] (e.g., row 0 + 6 = row 6)
            val_A = input_grid[r][c]
            val_B = input_grid[r + output_rows][c]

            # Apply the transformation rule:
            # If value in Grid A is 3 OR value in Grid B is 5, output is 4.
            if val_A == 3 or val_B == 5:
                output_grid[r][c] = 4
            # Otherwise, the output remains 0 (as initialized).

    # Return the resulting 6x4 grid.
    return output_grid