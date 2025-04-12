"""
Transformation Rule:
1. Identify columns in the input grid composed entirely of the background color (0) ("empty columns").
2. Filter out these empty columns, keeping the remaining "non-empty" columns.
3. The non-empty columns form the basis of the output grid, maintaining their relative horizontal order. The output grid has the same height (H) as the input grid.
4. Determine the mapping from each original non-empty column index `c` to its new destination index `c_new` in the output grid (0-based, preserving order).
5. For each non-empty column, calculate a vertical cyclic shift amount `S`.
6. Apply this vertical cyclic shift `S` to the column data. A pixel originally at row `r` moves to row `(r + S) % H`.
7. Assemble the output grid by placing these shifted columns into their corresponding `c_new` positions.

Key Challenge: The rule for determining the shift amount `S` is not consistent across all examples.
- The rule S = c_new // H (integer division of the *new* column index by grid height) correctly describes the transformation for Example 1.
- This rule fails for Examples 2, 3, and 4, which require different sequences of shifts:
    - Ex 2 Shifts: [0, 0, 2, 2, 1, 1, 1, 1]
    - Ex 3 Shifts: [0, 0, 0, 2, 2, 0, 0, 0]
    - Ex 4 Shifts: [0, 0, 2, 2, 0, 0, 0]
- The code below implements the rule S = c_new // H as the current best hypothesis, while acknowledging its limitations for other examples.
"""

import numpy as np

def _find_non_empty_columns_and_map(grid: np.ndarray) -> tuple[list[int], dict[int, int]]:
    """
    Identifies non-empty columns (not all background color 0) and creates a mapping.

    Args:
        grid: The input grid as a numpy array.

    Returns:
        A tuple containing:
        - A list of indices of non-empty columns in the original grid, preserving order.
        - A dictionary mapping original non-empty column indices (c) to their new 0-based indices (c_new).
    """
    height, width = grid.shape
    background_color = 0
    non_empty_col_indices = []
    col_mapping = {}
    new_col_idx = 0
    # Iterate through each original column index
    for c in range(width):
        # Check if the column contains any non-background pixel
        # Using np.any is efficient for this check
        is_non_empty = np.any(grid[:, c] != background_color)
        # If the column is not empty
        if is_non_empty:
            # Record the original index
            non_empty_col_indices.append(c)
            # Map original index to the new index
            col_mapping[c] = new_col_idx
            # Increment the new index for the next non-empty column
            new_col_idx += 1
    return non_empty_col_indices, col_mapping

def transform(input_grid_list: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by removing empty columns and applying a vertical
    cyclic shift to the remaining columns based on their destination index.

    Args:
        input_grid_list: The input grid as a list of lists of integers.

    Returns:
        The transformed grid as a list of lists of integers.
    """
    # Convert input list of lists to a NumPy array for efficient processing
    input_grid = np.array(input_grid_list, dtype=int)

    # Handle empty input grid edge cases
    if input_grid.size == 0:
        return [] # Input was []

    height, width = input_grid.shape
    background_color = 0

    # Handle cases with zero height or width post-conversion
    if height == 0: # e.g., input was [[]]
         return [] # Return empty list for zero height input
    if width == 0: # e.g., input was [[], [], []]
        # Output should have original height but zero width
        return [[] for _ in range(height)]

    # --- Step 1 & 2: Identify non-empty columns and create the c -> c_new mapping ---
    non_empty_col_indices, col_mapping = _find_non_empty_columns_and_map(input_grid)

    # --- Step 3: Determine output grid dimensions ---
    output_height = height
    output_width = len(non_empty_col_indices)
    H = output_height # Alias for height, useful for shift calculation

    # Handle case where all columns were empty
    if output_width == 0:
         # Output should have original height but zero width
         return [[] for _ in range(output_height)]

    # --- Step 4: Create the output grid, initialized with background color ---
    output_grid = np.full((output_height, output_width), background_color, dtype=int)

    # --- Step 5, 6, 7: Process each non-empty column ---
    for c in non_empty_col_indices:
        # Get the destination column index in the output grid
        c_new = col_mapping[c]

        # Extract the original column data from the input grid
        original_column = input_grid[:, c]

        # --- Calculate the vertical shift amount S ---
        # Using the candidate rule S = c_new // H derived from Example 1.
        # !!! IMPORTANT NOTE: This rule is KNOWN to be INCORRECT for Examples 2, 3, and 4. !!!
        # !!! The correct general rule for determining the shift remains unknown.       !!!
        shift_amount = c_new // H if H > 0 else 0

        # --- Apply the vertical cyclic shift S to the column ---
        # np.roll shifts elements: positive shift moves elements downwards (towards higher indices)
        shifted_column = np.roll(original_column, shift_amount)

        # --- Place the shifted column into the output grid ---
        output_grid[:, c_new] = shifted_column

    # Convert the final NumPy grid back to a standard Python list of lists format
    return output_grid.tolist()