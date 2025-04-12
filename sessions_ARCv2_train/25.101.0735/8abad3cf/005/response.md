```python
import numpy as np
import math

"""
Transforms a 2D input grid (I) into a 2D output grid (O) with different dimensions.

The transformation involves:
1. Determining output dimensions based on input columns (I_cols):
   - Output rows: O_rows = floor(I_cols / 2) + 1
   - Right part (O2) columns: O2_cols = O_rows
   - Left part (O1) columns: O1_cols = I_cols - 1
   - Total output columns: O_cols = O1_cols + O2_cols
2. Constructing the right part (O2) by vertically tiling the first O_rows elements of the input's first row.
3. Constructing the left part (O1) using a rule derived from train_2 (known to fail for train_1):
   a. Extracting a source subgrid S from the input: S = I[(I_rows - O_rows):I_rows, 1:I_cols].
   b. Flipping S vertically (upside-down) to create Temp.
   c. If Temp has 3 or more columns (O1_cols >= 3), swapping its second (index 1) and third (index 2) columns.
   d. The resulting grid is O1. (Note: This step is known to be incorrect for train_1).
4. Horizontally concatenating the calculated O1 and O2 to form the final output grid O.
"""


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation described above to the input grid.
    """
    # Convert input list of lists to a NumPy array for efficient manipulation
    I = np.array(input_grid, dtype=int)
    I_rows, I_cols = I.shape

    # Step 2: Determine the dimensions of the output grid O and its parts
    O_rows = math.floor(I_cols / 2) + 1
    O2_cols = O_rows
    O1_cols = I_cols - 1
    # O_cols = O1_cols + O2_cols # Total output columns

    # Step 3: Construct the right part O2
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
         O2 = np.resize(O2, (O_rows, O2_cols))

    # Step 4: Construct the left part O1 (using the best-fit rule derived so far)
    # 4a: Identify and extract the source subgrid S
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

    # 4b: Flip the subgrid S vertically
    Temp = np.flipud(S)

    # 4c: If Temp has 3 or more columns, swap its second and third columns
    O1 = Temp.copy() # Create a copy to modify, leaving Temp unchanged
    if O1_cols >= 3:
        # Perform the swap on the copy O1. Ensure columns are copied before swapping.
        col1 = O1[:, 1].copy() # Copy of the second column (index 1)
        col2 = O1[:, 2].copy() # Copy of the third column (index 2)
        O1[:, 1] = col2       # Assign the third column's data to the second column
        O1[:, 2] = col1       # Assign the second column's data to the third column
    # If O1_cols < 3, O1 remains just the vertically flipped S

    # Step 5: Combine the parts O1 and O2
    # Horizontally concatenate O1 and O2
    output_grid_np = np.hstack((O1, O2))

    # Step 6: Return the final output grid
    # Convert the final NumPy array back to a list of lists format
    output_grid = output_grid_np.tolist()

    return output_grid
```