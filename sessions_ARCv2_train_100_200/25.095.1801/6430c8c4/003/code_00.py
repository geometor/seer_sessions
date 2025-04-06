import numpy as np

"""
Identify the two 4x4 input grids: `grid_A` (rows 0-3 of the input) and `grid_B` (rows 5-8 of the input), ignoring the separator row (row 4).
Create a new 4x4 output grid, initialized with zeros.
Iterate through each cell position `(r, c)` from `(0, 0)` to `(3, 3)`.
For the current position `(r, c)`, check the value of the cell in `grid_A` (i.e., `input[r][c]`) and the value of the corresponding cell in `grid_B` (i.e., `input[r+5][c]`).
If the value in `grid_A` at `(r, c)` is `0` AND the value in `grid_B` at `(r, c)` is `0`, set the value of the output grid at `(r, c)` to `3`.
Otherwise (if either cell in `grid_A` or `grid_B` is not `0`), keep the value of the output grid at `(r, c)` as `0`.
Return the completed 4x4 output grid.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input 9x4 grid into a 4x4 output grid based on an
    element-wise comparison of two 4x4 subgrids within the input.
    """
    
    # Convert input to numpy array for easier slicing and comparison
    input_np = np.array(input_grid, dtype=int)

    # Extract the two relevant 4x4 subgrids
    # grid_A is the top part (rows 0-3)
    grid_A = input_np[0:4, :]
    # grid_B is the bottom part (rows 5-8), skipping the separator row 4
    grid_B = input_np[5:9, :]

    # Initialize the output grid with zeros, matching the dimensions (4x4)
    output_grid = np.zeros_like(grid_A, dtype=int) # Using grid_A shape as reference

    # Apply the core transformation logic using element-wise comparison
    # Find positions where BOTH grid_A and grid_B have a value of 0
    condition = (grid_A == 0) & (grid_B == 0)

    # Where the condition is true, set the output grid value to 3
    output_grid[condition] = 3

    # Convert the result back to a list of lists for the expected output format
    return output_grid.tolist()
