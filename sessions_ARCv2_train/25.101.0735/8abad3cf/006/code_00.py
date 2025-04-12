import numpy as np
import math

def analyze_o1_transformation(input_grid_list, expected_output_list, example_name):
    print(f"--- Analysis for {example_name} ---")
    I = np.array(input_grid_list, dtype=int)
    I_rows, I_cols = I.shape

    O_rows = math.floor(I_cols / 2) + 1
    O1_cols = I_cols - 1

    # Extract Expected O1
    O_expected = np.array(expected_output_list, dtype=int)
    if O_expected.shape[1] < O1_cols:
         print(f"Error: Expected output has fewer columns ({O_expected.shape[1]}) than needed for O1 ({O1_cols}).")
         return
    O1_expected = O_expected[:, 0:O1_cols]

    # Extract Subgrid S
    s_row_start = I_rows - O_rows
    s_row_end = I_rows
    s_col_start = 1
    s_col_end = I_cols
    S = I[s_row_start:s_row_end, s_col_start:s_col_end]

    # Calculate O1 based on hypothesis (flipud + swap cols 1&2)
    Temp = np.flipud(S)
    O1_calculated = Temp.copy()
    if O1_cols >= 3:
        col1 = O1_calculated[:, 1].copy()
        col2 = O1_calculated[:, 2].copy()
        O1_calculated[:, 1] = col2
        O1_calculated[:, 2] = col1

    print(f"Input Shape: {I.shape}, I_cols Parity: {'Odd' if I_cols % 2 != 0 else 'Even'}")
    print(f"Expected O1 Shape: {O1_expected.shape}")
    print(f"Subgrid S (I[{s_row_start}:{s_row_end}, {s_col_start}:{s_col_end}]):\n{S.tolist()}")
    print(f"Expected O1:\n{O1_expected.tolist()}")
    print(f"Calculated O1 (using 'Even I_cols' rule: flipud(S) then swap cols 1&2):\n{O1_calculated.tolist()}")
    match = np.array_equal(O1_expected, O1_calculated)
    print(f"O1 Match: {match}")
    print("-" * 30)


# Example 1
input_1 = [
    [4, 4, 4, 4, 4, 7, 7], [4, 7, 7, 7, 4, 7, 5], [4, 7, 1, 7, 4, 7, 5],
    [4, 7, 7, 7, 4, 7, 7], [4, 4, 4, 4, 4, 7, 5], [7, 7, 7, 7, 7, 7, 5],
    [5, 5, 5, 5, 5, 7, 7]
]
output_1 = [
    [7, 7, 7, 7, 7, 7, 4, 4, 4, 4], [7, 7, 5, 5, 5, 7, 4, 4, 4, 4],
    [7, 7, 5, 5, 5, 7, 4, 4, 4, 4], [1, 7, 5, 5, 5, 7, 4, 4, 4, 4]
]
analyze_o1_transformation(input_1, output_1, "Train Example 1")

# Example 2
input_2 = [
    [9, 9, 9, 9], [7, 7, 9, 7], [9, 9, 9, 9], [7, 7, 7, 7],
    [7, 6, 7, 6], [7, 6, 7, 6], [7, 7, 7, 7]
]
output_2 = [
    [7, 7, 7, 9, 9, 9], [6, 6, 7, 9, 9, 9], [6, 6, 7, 9, 9, 9]
]
analyze_o1_transformation(input_2, output_2, "Train Example 2")