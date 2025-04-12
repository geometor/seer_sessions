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
Finally, it constructs the output grid by vertically stacking these three 
selected sub-grids in that specific order.
"""

def _find_separator_lines(grid: np.ndarray, sep_value: int) -> Tuple[List[int], List[int]]:
    """Finds the indices of rows and columns that act as separators."""
    height, width = grid.shape
    sep_rows = [i for i in range(height) if np.all(grid[i, :] == sep_value)]
    sep_cols = [j for j in range(width) if np.all(grid[:, j] == sep_value)]
    return sep_rows, sep_cols

def _extract_subgrid(grid: np.ndarray, sep_rows: List[int], sep_cols: List[int], r_idx: int, c_idx: int) -> np.ndarray:
    """Extracts a single sub-grid based on its block index."""
    start_row = sep_rows[r_idx]
    # Slicing needs the index *after* the end of the block. The next separator line index marks this.
    # However, numpy slicing is exclusive of the end index, so we need sep_rows[r_idx+1]
    # But wait, the original analysis showed the block *includes* the final separator line.
    # Let's rethink the slice: sep_rows[r] is the top border. sep_rows[r+1] is the *next* border.
    # So the rows *for* block r are from sep_rows[r] up to *and including* sep_rows[r+1].
    # Numpy slice: [start : end], where end is exclusive.
    # So we need [sep_rows[r] : sep_rows[r+1] + 1]
    end_row = sep_rows[r_idx+1] + 1 # +1 because slicing is exclusive and we want to include the separator row/col
    start_col = sep_cols[c_idx]
    end_col = sep_cols[c_idx+1] + 1

    # Ensure the calculated end indices do not exceed grid dimensions
    # This check might be redundant if index validation happens earlier, but good for safety.
    grid_height, grid_width = grid.shape
    end_row = min(end_row, grid_height)
    end_col = min(end_col, grid_width)

    return grid[start_row:end_row, start_col:end_col]


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Selects three specific sub-grids from the input grid based on their
    position and stacks them vertically.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the output grid, formed by stacking
        the selected sub-grids. Returns empty list if structure is invalid.
    """
    # Convert input to a NumPy array for easier manipulation
    if not input_grid or not input_grid[0]:
        return [] # Handle empty input
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape

    # Identify the separator value (assumed to be the value in the top-left corner)
    sep_value = input_array[0, 0]

    # Find the indices of separator rows and columns
    sep_rows, sep_cols = _find_separator_lines(input_array, sep_value)

    # Check if enough separators exist to form at least one block
    if len(sep_rows) < 2 or len(sep_cols) < 2:
        # Cannot determine block structure
        return []

    # Determine the number of block rows (M) and columns (N)
    num_block_rows = len(sep_rows) - 1
    num_block_cols = len(sep_cols) - 1

    # We need at least 3 rows of blocks (M>=3) and enough columns for the indices.
    if num_block_rows < 3:
         print(f"Warning: Input grid requires at least 3 block rows, found {num_block_rows}. Returning empty.")
         return []

    # Determine the column index for the third block based on N
    if num_block_cols % 2 == 0:  # N is even
        c3 = num_block_cols - 1
    else:  # N is odd
        c3 = num_block_cols - 2

    # Define the target block indices (row_index, col_index)
    block_indices = [(0, 2), (1, 0), (2, c3)]
    r1, c1 = block_indices[0]
    r2, c2 = block_indices[1]
    r3, c3 = block_indices[2] # Use the calculated c3

    # Validate indices: check if column indices are within the bounds [0, N-1]
    if not (0 <= c1 < num_block_cols and \
            0 <= c2 < num_block_cols and \
            0 <= c3 < num_block_cols):
        print(f"Warning: Required column index out of bounds (N={num_block_cols}, required c1={c1}, c2={c2}, c3={c3}). Returning empty.")
        return []
        
    # Check if row indices are valid (redundant due to M check, but safe)
    if not (0 <= r1 < num_block_rows and \
            0 <= r2 < num_block_rows and \
            0 <= r3 < num_block_rows):
         print(f"Warning: Required row index out of bounds (M={num_block_rows}, required r1={r1}, r2={r2}, r3={r3}). Returning empty.")
         return []


    # Extract the selected sub-grids using the helper function
    try:
        block1 = _extract_subgrid(input_array, sep_rows, sep_cols, r1, c1)
        block2 = _extract_subgrid(input_array, sep_rows, sep_cols, r2, c2)
        block3 = _extract_subgrid(input_array, sep_rows, sep_cols, r3, c3)
    except IndexError:
        # This might happen if sep_rows/sep_cols don't have enough elements for r+1/c+1 access
        print(f"Error: Index out of bounds during subgrid extraction. Check separator line detection.")
        return []


    # Check if block extraction was successful and shapes match
    if block1.size == 0 or block2.size == 0 or block3.size == 0:
         print(f"Warning: One or more blocks extracted were empty.")
         return []
    if not (block1.shape == block2.shape == block3.shape):
        print(f"Warning: Extracted blocks have inconsistent shapes: {block1.shape}, {block2.shape}, {block3.shape}. Returning empty.")
        return []

    # Vertically stack the selected blocks
    output_array = np.vstack((block1, block2, block3))

    # Convert the final NumPy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid