```python
import numpy as np
from typing import List, Tuple

"""
This transformation identifies sub-grids within a larger input grid based on 
separator lines (rows/columns filled with a single value, typically the value
at [0,0]). It then selects three specific sub-grids based on their row and 
column index within the M x N arrangement of sub-grids. 
The selected sub-grids are:
1. The sub-grid at index (row=0, col=2).
2. The sub-grid at index (row=1, col=0).
3. The sub-grid at index (row=2, col=C3), where C3 is determined by the 
   total number of sub-grid columns (N). If N is even, C3 = N - 1. 
   If N is odd, C3 = N - 2.
Finally, it constructs the output grid by vertically stacking the first 
selected sub-grid, followed by the second sub-grid excluding its first row, 
and finally the third sub-grid excluding its first row. This creates an 
overlapping effect using the separator lines.
"""

def _find_separator_lines(grid: np.ndarray, sep_value: int) -> Tuple[List[int], List[int]]:
    """Finds the indices of rows and columns that act as separators."""
    height, width = grid.shape
    sep_rows = [i for i in range(height) if np.all(grid[i, :] == sep_value)]
    sep_cols = [j for j in range(width) if np.all(grid[:, j] == sep_value)]
    return sep_rows, sep_cols

def _extract_subgrid(grid: np.ndarray, sep_rows: List[int], sep_cols: List[int], r_idx: int, c_idx: int) -> np.ndarray:
    """
    Extracts a single sub-grid based on its block index (r_idx, c_idx),
    including its surrounding separator lines.
    """
    # Get the start row/col index (top/left separator line)
    start_row = sep_rows[r_idx]
    start_col = sep_cols[c_idx]
    
    # Get the end row/col index (the index *after* the bottom/right separator line)
    # The sub-grid includes the separator line at sep_rows[r_idx+1] / sep_cols[c_idx+1]
    # Numpy slicing is exclusive, so end index needs to be sep_...[idx+1] + 1
    end_row = sep_rows[r_idx+1] + 1 
    end_col = sep_cols[c_idx+1] + 1

    # Ensure the calculated end indices do not exceed grid dimensions
    grid_height, grid_width = grid.shape
    end_row = min(end_row, grid_height)
    end_col = min(end_col, grid_width)

    return grid[start_row:end_row, start_col:end_col]


def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    """
    Selects three specific sub-grids from the input grid based on their
    position and stacks them with overlap to produce the output grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the output grid, formed by stacking
        the selected sub-grids with overlap. Returns empty list if the
        input structure is invalid or incompatible with the transformation.
    """
    # Handle empty input grid
    if not input_grid or not input_grid[0]:
        return [] 

    # Convert input to a NumPy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape

    # Identify the separator value (assumed to be the value in the top-left corner)
    sep_value = input_array[0, 0]

    # Find the indices of separator rows and columns
    sep_rows, sep_cols = _find_separator_lines(input_array, sep_value)

    # Validate structure: Need at least 4 separator rows (M>=3) and 3 separator columns (N>=2)
    # M = len(sep_rows) - 1, N = len(sep_cols) - 1
    if len(sep_rows) < 4 or len(sep_cols) < 3:
        # Cannot determine required block structure or access required indices
        # print(f"Warning: Invalid structure. Need M>=3 (found {len(sep_rows)-1}) and N>=2 (found {len(sep_cols)-1}).")
        return []

    # Determine the number of block columns (N)
    num_block_cols = len(sep_cols) - 1
    N = num_block_cols

    # Determine the column index for the third block (C3) based on N's parity
    if N % 2 == 0:  # N is even
        c3_idx = N - 1
    else:  # N is odd
        c3_idx = N - 2

    # Define the target block indices (row_index, col_index)
    # Indices are fixed based on the task description
    idx1 = (0, 2)
    idx2 = (1, 0)
    idx3 = (2, c3_idx) 
    
    r1, c1 = idx1
    r2, c2 = idx2
    r3, c3 = idx3 

    # Validate column indices: Check if required columns (0, 2, C3) exist within N blocks
    if not (0 <= c1 < N and 0 <= c2 < N and 0 <= c3 < N):
        # print(f"Warning: Required column index out of bounds (N={N}, required c1={c1}, c2={c2}, c3={c3}).")
        return []
        
    # Note: Row index validation (0, 1, 2) is implicitly covered by checking len(sep_rows) >= 4 earlier.

    # Extract the selected sub-grids using the helper function
    try:
        block1 = _extract_subgrid(input_array, sep_rows, sep_cols, r1, c1)
        block2 = _extract_subgrid(input_array, sep_rows, sep_cols, r2, c2)
        block3 = _extract_subgrid(input_array, sep_rows, sep_cols, r3, c3)
    except IndexError:
        # This might happen if sep_rows/sep_cols calculation was faulty or grid is irregular
        # print(f"Error: Index out of bounds during subgrid extraction. Check separator line detection or grid regularity.")
        return []

    # Validate extracted blocks - ensure they are not empty and have height > 1 for overlap logic
    if block1.size == 0 or block2.size == 0 or block3.size == 0:
        # print(f"Warning: One or more extracted blocks were empty.")
        return []
    if block1.shape[0] <= 1 or block2.shape[0] <= 1 or block3.shape[0] <= 1:
        # print(f"Warning: Extracted block height ({block1.shape[0]}) is too small for overlap logic.")
        return []
    # Basic shape check (more robust check might compare all shapes)
    if block1.shape[1] != block2.shape[1] or block1.shape[1] != block3.shape[1]:
         # print(f"Warning: Extracted blocks have inconsistent widths: {block1.shape[1]}, {block2.shape[1]}, {block3.shape[1]}.")
         return []


    # Construct the output grid by vertically stacking with overlap
    # Stack: Block1 (full), Block2 (rows 1 onwards), Block3 (rows 1 onwards)
    output_array = np.vstack((block1, block2[1:, :], block3[1:, :]))

    # Convert the final NumPy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid
```