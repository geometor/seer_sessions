```python
import numpy as np
import collections

"""
Extracts a subgrid from the input grid based on boundary columns and rows.

1.  **Identify Boundary Columns:** Finds the leftmost (col1) and rightmost (col2) 
    columns where all non-zero elements consist of a single, repeating digit.
2.  **Identify Boundary Rows:** Finds the topmost (row1) and bottommost (row2) 
    rows where all elements between col1 and col2 (inclusive) are non-zero.
3.  **Extract Subgrid:** Returns the portion of the input grid defined by the 
    rectangle from (row1, col1) to (row2, col2).
"""

def _find_boundary_columns(grid: np.ndarray) -> tuple[int, int]:
    """
    Finds the indices of the leftmost and rightmost boundary columns.
    A boundary column is defined as a column where all non-zero elements
    are the same single digit.
    """
    num_rows, num_cols = grid.shape
    boundary_col_indices = []

    for j in range(num_cols):
        col = grid[:, j]
        non_zeros = col[col != 0]
        if len(non_zeros) > 1: # Need at least two non-zeros to establish pattern
             unique_non_zeros = np.unique(non_zeros)
             if len(unique_non_zeros) == 1:
                 # Check if all non-zero elements are this single unique value
                 if np.all(non_zeros == unique_non_zeros[0]):
                     boundary_col_indices.append(j)

    if len(boundary_col_indices) < 2:
        # Fallback or error handling needed if less than 2 boundaries found
        # For now, let's assume based on examples, at least 2 will be found.
        # A simpler heuristic might be needed if this fails.
        # Maybe find columns with the *most* instances of a single non-zero number?
         potential_cols = {}
         for j in range(num_cols):
            col = grid[:, j]
            non_zeros = col[col != 0]
            if len(non_zeros) > 0:
                counts = collections.Counter(non_zeros)
                most_common_val, most_common_count = counts.most_common(1)[0]
                # Store column index and the count/value as potential boundary markers
                potential_cols[j] = {'count': most_common_count, 'value': most_common_val}

         # Sort potential columns by count (desc) and pick first/last as a guess
         if len(potential_cols) >= 2:
             sorted_indices = sorted(potential_cols.keys())
             col1 = sorted_indices[0]
             col2 = sorted_indices[-1]
             # Refine: maybe select based on counts rather than just first/last index?
             # For the given examples, the strict definition works, let's stick to it for now.
             # If the strict check fails, this part needs improvement.
             raise ValueError("Could not reliably identify exactly two boundary columns with the strict definition.")
         elif len(potential_cols) == 1:
              # Handle cases with only one potential boundary? Unlikely based on examples.
              raise ValueError("Only one potential boundary column identified.")
         else:
             raise ValueError("No potential boundary columns identified.")


    col1 = min(boundary_col_indices)
    col2 = max(boundary_col_indices)
    return col1, col2


def _find_boundary_rows(grid: np.ndarray, col1: int, col2: int) -> tuple[int, int]:
    """
    Finds the indices of the first and last rows where all elements
    between col1 and col2 (inclusive) are non-zero.
    """
    num_rows = grid.shape[0]
    boundary_row_indices = []

    for i in range(num_rows):
        sub_row = grid[i, col1 : col2 + 1]
        if np.all(sub_row != 0):
            boundary_row_indices.append(i)

    if not boundary_row_indices:
         raise ValueError("Could not find any rows where all elements between boundary columns are non-zero.")

    row1 = min(boundary_row_indices)
    row2 = max(boundary_row_indices)
    return row1, row2


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by extracting a subgrid based on identified boundaries.
    """
    # Convert input to numpy array for easier manipulation
    grid_np = np.array(input_grid, dtype=int)

    if grid_np.size == 0:
        return []
    if grid_np.ndim != 2 or grid_np.shape[0] == 0 or grid_np.shape[1] == 0:
         # Handle empty or non-2D grids if necessary
         return [] # Or raise error


    # Find the boundary columns (leftmost and rightmost)
    col1, col2 = _find_boundary_columns(grid_np)

    # Find the boundary rows (topmost and bottommost) based on the columns
    row1, row2 = _find_boundary_rows(grid_np, col1, col2)

    # Extract the subgrid defined by these boundaries
    output_grid_np = grid_np[row1 : row2 + 1, col1 : col2 + 1]

    # Convert the resulting numpy array back to a list of lists
    output_grid = output_grid_np.tolist()

    return output_grid
```