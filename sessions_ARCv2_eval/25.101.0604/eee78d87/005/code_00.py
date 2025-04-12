import numpy as np
from collections import Counter
from typing import List, Optional, Tuple

"""
Transforms a 6x6 input grid of digits into a 16x16 output grid based on the following rules:

1.  **Analyze Outer Input:** Examine the input 6x6 grid. Identify all digits located *outside* the central 3x3 region (defined by rows 1-3 and columns 1-3, using 0-based indexing). Find the most frequent digit among these outer cells, ignoring any '7's.
2.  **Select Base Pattern:** Based on the most frequent non-'7' digit found in the outer input region:
    *   If it is '1', select the 4x4 base pattern `P_base_1`.
    *   If it is '6', select the 4x4 base pattern `P_base_6`.
    *   Otherwise (if no non-'7' digit exists in the outer region, or the most frequent is something else), select the 4x4 base pattern `P_base_0`.
3.  **Generate Base Grid:** Create a 16x16 grid (`output_grid`) by tiling the selected 4x4 base pattern (`P_base_0`, `P_base_1`, or `P_base_6`) four times horizontally and four times vertically.
4.  **Analyze Central Input:** Extract the central 3x3 subgrid from the input grid (rows 1-3, columns 1-3). Find the most frequent digit within this 3x3 subgrid, ignoring any '7's.
5.  **Select Modification Pattern:** Based on the most frequent non-'7' digit found in the central 3x3 input subgrid:
    *   If it is '1', select the 6x7 modification pattern `M1`.
    *   If it is '3', select the 6x7 modification pattern `M3`.
    *   If it is '6', select the 6x7 modification pattern `M6`.
    *   If the central 3x3 subgrid contains only '7's (or no non-'7' digits), no modification pattern is selected.
6.  **Apply Modification:**
    *   If a modification pattern (`M1`, `M3`, or `M6`) was selected in the previous step, replace the content of the `output_grid` within the region defined by rows 4 through 9 (inclusive) and columns 4 through 10 (inclusive) with the selected 6x7 modification pattern.
    *   If no modification pattern was selected, the `output_grid` remains unchanged from step 3.
7.  **Finalize:** The `output_grid` now holds the final result.
"""


# --- Helper Functions ---

def get_most_frequent_non_7(values: np.ndarray) -> Optional[int]:
    """
    Finds the most frequent digit other than 7 in a given numpy array of values.

    Args:
        values: A numpy array containing digits.

    Returns:
        The most frequent non-7 digit, or None if only 7s are present or the array is empty.
    """
    # Filter out the number 7
    non_7_digits = values[values != 7]

    if non_7_digits.size == 0:
        return None

    # Count occurrences of each digit
    counts = Counter(non_7_digits)

    # Find the digit with the highest count
    # If there's a tie, the behavior of most_common(1) is sufficient for the observed examples.
    most_common_digit, _ = counts.most_common(1)[0]
    return most_common_digit

# --- Pattern Definitions ---

P_base_0 = np.array([
    [0, 0, 0, 0],
    [0, 7, 7, 0],
    [0, 7, 7, 0],
    [0, 0, 0, 0]
], dtype=int)

P_base_1 = np.array([
    [0, 0, 0, 0],
    [7, 0, 0, 7],
    [7, 0, 0, 7],
    [0, 0, 0, 0]
], dtype=int)

P_base_6 = np.array([
    [0, 7, 7, 0],
    [7, 0, 0, 7],
    [7, 0, 0, 7],
    [0, 7, 7, 0]
], dtype=int)

M1 = np.array([
    [7, 0, 0, 7, 0, 0, 7],
    [7, 0, 9, 7, 9, 9, 7],
    [0, 0, 9, 9, 9, 9, 9],
    [7, 0, 9, 7, 9, 9, 7],
    [7, 0, 9, 7, 9, 9, 7],
    [0, 0, 9, 9, 9, 9, 9]
], dtype=int)

M3 = np.array([
    [0, 7, 7, 0, 7, 7, 0],
    [0, 7, 7, 9, 7, 7, 9],
    [0, 0, 0, 9, 9, 9, 9],
    [0, 7, 7, 9, 7, 7, 9],
    [0, 7, 7, 9, 7, 7, 9],
    [0, 0, 0, 9, 9, 9, 9]
], dtype=int)

M6 = np.array([
    [7, 0, 0, 7, 0, 0, 7],
    [7, 0, 9, 7, 9, 9, 7],
    [0, 7, 7, 9, 7, 7, 9],
    [7, 0, 9, 7, 9, 9, 7],
    [7, 0, 9, 7, 9, 9, 7],
    [0, 7, 7, 9, 7, 7, 9]
], dtype=int)


# --- Main Transformation Function ---

def transform(input_grid_list: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid_list: A 6x6 list of lists representing the input grid digits.

    Returns:
        A 16x16 list of lists representing the transformed grid digits.
    """
    # Convert input to numpy array for easier manipulation
    input_grid = np.array(input_grid_list, dtype=int)
    if input_grid.shape != (6, 6):
         raise ValueError("Input grid must be 6x6")

    # 1. Determine Base Pattern based on Outer Input Region
    # Create a boolean mask: True for outer cells, False for central 3x3
    outer_mask = np.ones_like(input_grid, dtype=bool)
    outer_mask[1:4, 1:4] = False
    # Extract the digits from the outer region
    outer_region_values = input_grid[outer_mask]
    # Find the most frequent non-7 digit in the outer region
    outer_key_digit = get_most_frequent_non_7(outer_region_values)

    # 2. Select Base Pattern
    if outer_key_digit == 1:
        base_pattern = P_base_1
    elif outer_key_digit == 6:
        base_pattern = P_base_6
    else: # Default to P_base_0 if key digit is None or anything else
        base_pattern = P_base_0

    # 3. Generate Base Grid by tiling the selected pattern
    output_grid = np.tile(base_pattern, (4, 4))

    # 4. Determine Modification Pattern based on Central Input Region
    # Extract the central 3x3 input subgrid (rows 1-3, cols 1-3)
    central_input = input_grid[1:4, 1:4]
    # Find the most frequent non-7 digit in the central region
    central_key_digit = get_most_frequent_non_7(central_input.flatten()) # flatten needed for get_most_frequent_non_7

    # 5. Select Modification Pattern
    modification_pattern = None
    if central_key_digit == 1:
        modification_pattern = M1
    elif central_key_digit == 3:
        modification_pattern = M3
    elif central_key_digit == 6:
        modification_pattern = M6

    # 6. Apply Modification if a pattern was selected
    if modification_pattern is not None:
        # Define the target region slices in the output grid
        # Rows 4 through 9 (exclusive of 10) -> slice(4, 10)
        # Columns 4 through 10 (exclusive of 11) -> slice(4, 11)
        mod_rows_slice = slice(4, 10)
        mod_cols_slice = slice(4, 11)

        # Replace the content of the target region with the modification pattern
        output_grid[mod_rows_slice, mod_cols_slice] = modification_pattern

    # 7. Finalize: Convert the resulting numpy array back to a list of lists
    final_output_grid = output_grid.tolist()

    return final_output_grid