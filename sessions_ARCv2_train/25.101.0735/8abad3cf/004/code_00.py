import numpy as np
import math

def analyze_o1_transformation(input_grid_list, expected_output_list):
    I = np.array(input_grid_list, dtype=int)
    I_rows, I_cols = I.shape

    O_rows = math.floor(I_cols / 2) + 1
    O2_cols = O_rows
    O1_cols = I_cols - 1

    # Extract Expected O1 from expected_output_list
    O_expected = np.array(expected_output_list, dtype=int)
    O1_expected = O_expected[:, 0:O1_cols]

    # Extract Subgrid S
    s_row_start = I_rows - O_rows
    s_row_end = I_rows
    s_col_start = 1
    s_col_end = I_cols
    # Basic validation
    if s_row_start < 0 or s_col_start < 0 or s_row_end > I_rows or s_col_end > I_cols or s_row_start >= s_row_end or s_col_start >= s_col_end:
         S_str = "Error: Invalid S indices"
    else:
        S = I[s_row_start:s_row_end, s_col_start:s_col_end]
        if S.shape != (O_rows, O1_cols):
            S_str = f"Error: S shape mismatch. Expected ({O_rows},{O1_cols}), Got {S.shape}"
        else:
            S_str = f"Subgrid S (I[{s_row_start}:{s_row_end}, {s_col_start}:{s_col_end}]):\n{S.tolist()}"
            
            # Calculate O1 based on hypothesis (flipud + swap cols 1&2)
            Temp = np.flipud(S)
            O1_calculated = Temp.copy()
            if O1_cols >= 3:
                col1 = O1_calculated[:, 1].copy()
                col2 = O1_calculated[:, 2].copy()
                O1_calculated[:, 1] = col2
                O1_calculated[:, 2] = col1
            O1_calculated_str = f"Calculated O1 (flipud(S) then swap cols 1&2):\n{O1_calculated.tolist()}"


    print(f"Input Shape: {I.shape}")
    print(f"Expected O1 Shape: {O1_expected.shape}")
    print(S_str)
    print(f"Expected O1:\n{O1_expected.tolist()}")
    if 'O1_calculated_str' in locals(): # Check if calculation happened
      print(O1_calculated_str)
      match = np.array_equal(O1_expected, O1_calculated)
      print(f"O1 Match: {match}")
    else:
      print("O1 calculation skipped due to errors.")
    print("-" * 30)


# Example 1
input_1 = [
    [4, 4, 4, 4, 4, 7, 7],
    [4, 7, 7, 7, 4, 7, 5],
    [4, 7, 1, 7, 4, 7, 5],
    [4, 7, 7, 7, 4, 7, 7],
    [4, 4, 4, 4, 4, 7, 5],
    [7, 7, 7, 7, 7, 7, 5],
    [5, 5, 5, 5, 5, 7, 7]
]
output_1 = [
    [7, 7, 7, 7, 7, 7, 4, 4, 4, 4],
    [7, 7, 5, 5, 5, 7, 4, 4, 4, 4],
    [7, 7, 5, 5, 5, 7, 4, 4, 4, 4],
    [1, 7, 5, 5, 5, 7, 4, 4, 4, 4]
]
analyze_o1_transformation(input_1, output_1)

# Example 2
input_2 = [
    [9, 9, 9, 9],
    [7, 7, 9, 7],
    [9, 9, 9, 9],
    [7, 7, 7, 7],
    [7, 6, 7, 6],
    [7, 6, 7, 6],
    [7, 7, 7, 7]
]
output_2 = [
    [7, 7, 7, 9, 9, 9],
    [6, 6, 7, 9, 9, 9],
    [6, 6, 7, 9, 9, 9]
]
analyze_o1_transformation(input_2, output_2)