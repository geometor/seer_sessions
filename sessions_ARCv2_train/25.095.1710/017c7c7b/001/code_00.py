import copy

"""
Transforms a 6x3 input grid containing 0s and 1s into a 9x3 output grid containing 0s and 2s.

The transformation involves two main steps:
1. Value transformation: All 1s in the input grid are replaced with 2s. 0s remain unchanged.
2. Conditional row appending: 
   - Compare the 4th and 6th rows of the *original* input grid.
   - If they are identical, append the first 3 rows of the value-transformed grid to its end.
   - If they are different, append the 3rd, 4th, and 5th rows of the value-transformed grid to its end.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the described transformation to the input grid.

    Args:
        input_grid: A 6x3 list of lists containing 0s and 1s.

    Returns:
        A 9x3 list of lists containing 0s and 2s, resulting from the transformation.
    """

    # --- Step 1: Value Transformation ---
    # Create a deep copy to avoid modifying the original input if needed elsewhere
    # and perform the value transformation (1 -> 2).
    transformed_grid = []
    for r in range(len(input_grid)):
        new_row = []
        for c in range(len(input_grid[0])):
            if input_grid[r][c] == 1:
                new_row.append(2)
            else:
                new_row.append(0)
        transformed_grid.append(new_row)

    # --- Step 2: Conditional Row Appending ---
    # Check the condition: Compare the 4th and 6th rows of the ORIGINAL input grid.
    # Remember 0-based indexing: 4th row is index 3, 6th row is index 5.
    rows_to_append = []
    if input_grid[3] == input_grid[5]:
        # Condition met: Append the first 3 rows (indices 0, 1, 2) of the transformed grid.
        rows_to_append = transformed_grid[0:3]
    else:
        # Condition not met: Append the middle 3 rows (indices 2, 3, 4) of the transformed grid.
        rows_to_append = transformed_grid[2:5]

    # --- Construct the Output Grid ---
    # Start with the transformed grid and extend it with the selected rows.
    # Use copy() for rows_to_append to ensure independence if needed later, though extending list creates copies anyway.
    output_grid = copy.deepcopy(transformed_grid) 
    output_grid.extend(rows_to_append)

    return output_grid
