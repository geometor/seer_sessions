"""
Transforms a 2D input grid (I) into a 2D output grid (O) with different dimensions.

The transformation involves:
1. Determining output dimensions based on input columns (I_cols):
   - Output rows: O_rows = floor(I_cols / 2) + 1
   - Right part (O2) columns: O2_cols = O_rows
   - Left part (O1) columns: O1_cols = I_cols - 1
   - Total output columns: O_cols = O1_cols + O2_cols
2. Constructing the right part (O2) by vertically tiling the first O_rows elements of the input's first row.
3. Constructing the left part (O1) based on the parity of I_cols:
   - If I_cols is even:
     a. Extract a source subgrid S from the input: S = I[(I_rows - O_rows):I_rows, 1:I_cols].
     b. Flip S vertically (upside-down) to create Temp.
     c. If Temp has 3 or more columns (O1_cols >= 3), swap its second (index 1) and third (index 2) columns.
     d. The resulting grid is O1.
   - If I_cols is odd:
     The rule is undetermined. A placeholder (e.g., grid of zeros) is used.
4. Horizontally concatenating the calculated O1 and O2 to form the final output grid O.
"""

import numpy as np
import math

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation described above to the input grid.
    """
    # Convert input list of lists to a NumPy array for efficient manipulation
    I = np.array(input_grid, dtype=int)
    I_rows, I_cols = I.shape

    # Step 1: Determine the dimensions of the output grid O and its parts
    O_rows = math.floor(I_cols / 2) + 1
    O2_cols = O_rows
    O1_cols = I_cols - 1
    # O_cols = O1_cols + O2_cols # Total output columns, calculated implicitly by hstack

    # Step 2: Construct the right part O2
    # Select the first O_rows elements from the first row of the input grid
    slice_O2 = I[0, 0:O_rows]
    # Reshape slice_O2 to be 2D (1, O_rows) for vertical tiling
    if slice_O2.ndim == 1:
        slice_O2 = slice_O2.reshape(1, -1)
    # Create O2 by repeating (tiling) the slice vertically O_rows times
    O2 = np.tile(slice_O2, (O_rows, 1))
    # Validate O2 shape (should match O_rows x O2_cols)
    if O2.shape != (O_rows, O2_cols):
         # This is a safeguard; based on the logic O2_cols = O_rows = len(slice), it shouldn't mismatch.
         print(f"Warning: O2 shape mismatch during creation. Expected ({O_rows},{O2_cols}), Got {O2.shape}. Resizing.")
         O2 = np.resize(O2, (O_rows, O2_cols)) # Use resize as a fallback

    # Step 3: Construct the left part O1 based on the parity of I_cols
    if I_cols % 2 == 0: # Condition: I_cols is even
        # 3a (Even): Extract the source subgrid S
        s_row_start = I_rows - O_rows
        s_row_end = I_rows
        s_col_start = 1
        s_col_end = I_cols # NumPy slicing is exclusive at the end index

        # Validate indices before slicing to prevent errors
        if s_row_start < 0 or s_col_start < 0 or s_row_end > I_rows or s_col_end > I_cols or s_row_start >= s_row_end or s_col_start >= s_col_end:
             raise ValueError(f"Calculated subgrid indices for S are invalid or out of bounds: rows {s_row_start}:{s_row_end}, cols {s_col_start}:{s_col_end}")

        S = I[s_row_start:s_row_end, s_col_start:s_col_end]

        # Validate extracted S shape
        if S.shape != (O_rows, O1_cols):
             raise ValueError(f"Extracted subgrid S shape mismatch. Expected ({O_rows},{O1_cols}), Got {S.shape}")

        # 3b (Even): Flip the subgrid S vertically
        Temp = np.flipud(S)

        # 3c (Even): If Temp has 3 or more columns, swap its second and third columns
        O1 = Temp.copy() # Create a copy to modify, leaving Temp unchanged
        if O1_cols >= 3:
            # Perform the swap on the copy O1. Ensure columns are copied before swapping.
            col1 = O1[:, 1].copy() # Copy of the second column (index 1)
            col2 = O1[:, 2].copy() # Copy of the third column (index 2)
            O1[:, 1] = col2       # Assign the third column's data to the second column
            O1[:, 2] = col1       # Assign the second column's data to the third column
        # If O1_cols < 3, O1 remains just the vertically flipped S

    else: # Condition: I_cols is odd
        # The rule is undetermined. Use a placeholder: create an array of zeros.
        print(f"Warning: Rule for O1 construction with odd I_cols ({I_cols}) is undetermined. Returning zeros for O1 part.")
        O1 = np.zeros((O_rows, O1_cols), dtype=int)


    # Step 4: Combine the parts O1 and O2
    # Horizontally concatenate O1 and O2
    output_grid_np = np.hstack((O1, O2))

    # Step 5: Return the final output grid
    # Convert the final NumPy array back to a list of lists format
    output_grid = output_grid_np.tolist()

    return output_grid