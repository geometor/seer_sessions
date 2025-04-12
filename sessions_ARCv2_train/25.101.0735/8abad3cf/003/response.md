```python
import numpy as np
import math

"""
Transforms a 2D input grid into a 2D output grid with different dimensions.

The transformation involves:
1. Determining output dimensions based on input columns:
   - O_rows = floor(I_cols / 2) + 1
   - O2_cols = O_rows
   - O1_cols = I_cols - 1
   - O_cols = O1_cols + O2_cols
2. Constructing the right part (O2) by vertically tiling the first O_rows elements of the input's first row.
3. Constructing the left part (O1) by:
   a. Extracting a subgrid S from the bottom-right portion of the input (excluding the first column): S = I[(I_rows - O_rows):I_rows, 1:I_cols].
   b. Flipping S vertically (upside-down).
   c. If the flipped grid has 3 or more columns, swapping its second (index 1) and third (index 2) columns.
   d. The resulting grid is O1.
4. Horizontally concatenating O1 and O2 to form the final output grid.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation described above to the input grid.
    """
    # Convert input to numpy array for easier manipulation
    I = np.array(input_grid, dtype=int)
    I_rows, I_cols = I.shape

    # --- Step 2: Determine dimensions ---
    O_rows = math.floor(I_cols / 2) + 1
    O2_cols = O_rows
    O1_cols = I_cols - 1
    # O_cols = O1_cols + O2_cols # Total output columns

    # --- Step 3: Construct O2 (Right Part) ---
    # Select the slice from the first row
    slice_O2 = I[0, 0:O_rows]
    # Tile the slice vertically
    # Ensure slice_O2 is 2D for tiling (1, O_rows)
    if slice_O2.ndim == 1:
        slice_O2 = slice_O2.reshape(1, -1)
    # Use np.tile to repeat the row O_rows times vertically
    O2 = np.tile(slice_O2, (O_rows, 1))
    # Ensure O2 has the correct shape (O_rows, O2_cols)
    if O2.shape != (O_rows, O2_cols):
         # Defensive check - should not happen based on logic O2_cols = O_rows = slice length
         print(f"Warning: O2 shape mismatch. Expected ({O_rows},{O2_cols}), Got {O2.shape}")
         O2 = np.resize(O2, (O_rows, O2_cols))

    # --- Step 4: Construct O1 (Left Part) ---
    # 4a: Extract the source subgrid S
    s_row_start = I_rows - O_rows
    s_row_end = I_rows
    s_col_start = 1
    s_col_end = I_cols # Slices up to, but not including I_cols

    # Validate indices before slicing
    if s_row_start < 0 or s_col_start < 0 or s_row_end > I_rows or s_col_end > I_cols or s_row_start >= s_row_end or s_col_start >= s_col_end:
         raise ValueError(f"Calculated subgrid indices for S are invalid or out of bounds: rows {s_row_start}:{s_row_end}, cols {s_col_start}:{s_col_end}")

    S = I[s_row_start:s_row_end, s_col_start:s_col_end]

    # Validate extracted S shape
    if S.shape != (O_rows, O1_cols):
         raise ValueError(f"Extracted subgrid S shape mismatch. Expected ({O_rows},{O1_cols}), Got {S.shape}")

    # 4b: Flip S vertically
    Temp = np.flipud(S)

    # 4c: Swap columns 1 and 2 if O1_cols >= 3
    O1 = Temp.copy() # Start with the flipped version, copy to allow modification
    if O1_cols >= 3:
        # Perform the swap on the copy O1
        col1 = O1[:, 1].copy() # Make copies to avoid view issues during swap
        col2 = O1[:, 2].copy()
        O1[:, 1] = col2
        O1[:, 2] = col1
    # If O1_cols < 3, O1 remains just the vertically flipped S

    # --- Step 5: Combine O1 and O2 ---
    # Horizontally concatenate O1 and O2
    output_grid_np = np.hstack((O1, O2))

    # --- Step 6: Return result ---
    # Convert final numpy array back to list of lists
    output_grid = output_grid_np.tolist()

    return output_grid
```