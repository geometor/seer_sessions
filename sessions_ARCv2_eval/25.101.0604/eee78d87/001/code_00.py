import numpy as np
from typing import List

"""
Transforms a 6x6 input grid of digits into a 16x16 output grid based on the following rules:

1.  **Initialize Base Grid:** Create a 16x16 grid by tiling a 4x4 base pattern `P7` four times horizontally and four times vertically. The `P7` pattern is:
    ```
    [[0, 0, 0, 0],
     [0, 7, 7, 0],
     [0, 7, 7, 0],
     [0, 0, 0, 0]]
    ```
2.  **Identify Central Input:** Extract the 3x3 subgrid from the input grid located at rows 1 through 3 and columns 1 through 3 (using 0-based indexing). Call this `central_input`.
3.  **Apply Base Modification (if needed):** Check if any digit in `central_input` is not equal to 7.
    *   If a non-7 digit exists, modify the base grid in the central 6x7 region (rows 4-9, columns 4-10) by placing '9's at specific locations defined by a fixed mask (`M_base`).
4.  **Apply Specific Modification for '3' (if needed):** Check if the digit '3' exists anywhere within the `central_input`.
    *   If '3' exists, apply further specific changes to the grid within the central region:
        *   Set cell (4, 8) to 7.
        *   Set cell (4, 10) to 0.
        *   Set cell (5, 8) to 7.
        *   Set cell (7, 8) to 7.
        *   Set cell (8, 8) to 7.
5.  **Final Output:** The resulting 16x16 grid is the final output.
"""

def transform(input_grid_str: List[List[str]]) -> List[List[int]]:
    """
    Applies the transformation rule to convert the input grid string
    to the output integer grid.

    Args:
        input_grid_str: A 6x6 list of lists of strings representing digits.

    Returns:
        A 16x16 list of lists of integers representing the transformed grid.
    """

    # Convert input strings to integers
    try:
        input_grid = [[int(c) for c in row] for row in input_grid_str]
        input_np = np.array(input_grid, dtype=int)
        if input_np.shape != (6, 6):
             raise ValueError("Input grid must be 6x6")
    except (ValueError, TypeError) as e:
        print(f"Error converting input grid: {e}")
        # Handle error appropriately, e.g., return an empty grid or raise exception
        return []


    # 1. Define Base Pattern P7
    p7 = np.array([
        [0, 0, 0, 0],
        [0, 7, 7, 0],
        [0, 7, 7, 0],
        [0, 0, 0, 0]
    ], dtype=int)

    # 2. Generate Base Grid B (16x16) by tiling P7
    output_grid = np.tile(p7, (4, 4))

    # 3. Extract Central Input Ic (3x3)
    # Rows 1-3, Cols 1-3 (0-based indexing)
    central_input = input_np[1:4, 1:4]

    # 4. Apply Base Modification (if needed)
    # Check if any non-7 value exists in central_input
    has_non_7 = np.any(central_input != 7)

    if has_non_7:
        # Define the relative row/column indices within the 6x7 modification
        # region where '9's should be placed based on the base mask (M_base).
        # These coordinates correspond to the '9' locations observed in examples
        # where the central input contained '1' or '6'.
        rows_9_rel = [1, 1, 2, 2, 2, 2, 3, 3, 4, 4, 5, 5, 5, 5]
        cols_9_rel = [3, 6, 3, 4, 5, 6, 3, 6, 3, 6, 3, 4, 5, 6]

        # Define the top-left corner of the 6x7 modification region (Oc_region)
        oc_region_start_row = 4
        oc_region_start_col = 4

        # Calculate absolute output grid coordinates for the '9's
        output_rows_9 = np.array(rows_9_rel) + oc_region_start_row
        output_cols_9 = np.array(cols_9_rel) + oc_region_start_col

        # Apply the '9' overlay to the output grid
        output_grid[output_rows_9, output_cols_9] = 9

    # 5. Apply Specific Modification for '3' (if needed)
    # Check if any '3' exists in central_input
    has_3 = np.any(central_input == 3)

    if has_3:
        # Apply the specific modifications observed when '3' is present
        output_grid[4, 8] = 7
        output_grid[4, 10] = 0
        output_grid[5, 8] = 7
        output_grid[7, 8] = 7
        output_grid[8, 8] = 7

    # 6. Final Output
    # Convert the final numpy array back to a list of lists
    final_output_grid = output_grid.tolist()

    return final_output_grid