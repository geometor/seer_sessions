import numpy as np
from typing import List, Tuple, Optional, Union

"""
Transforms an input grid based on the location and pattern of the number '1'.

The transformation follows one of three primary rules determined by the pattern of '1's:

1.  **Vertical Expansion ('Vertical' pattern):** Triggered if all '1's are in column 0 AND form a contiguous block of rows.
    a.  Partitions the grid into `Subgrid_A` (rows above the marker block).
    b.  Creates `Row_0` (a row of zeros).
    c.  Forms `Block_V`: `[Subgrid_A / Row_0]` or just `Row_0`.
    d.  Repeats `Block_V` vertically `N` times (where `N` is the marker block height).
    e.  Appends a final `Subgrid_A` if it exists.

2.  **Horizontal Expansion ('Horizontal_Column' pattern):** Triggered if all '1's are in a single column (but not satisfying the 'Vertical' pattern).
    a.  Partitions the grid into `Matrix_A` (left), `Column_B` (marker), `Matrix_C` (right).
    b.  Creates `Column_0` (marker column with '1's -> '0's).
    c.  Forms `Block_H`: `[Matrix_A | Column_0]` or just `Column_0`.
    d.  Repeats `Block_H` horizontally `N` times (where `N` = cols in `Matrix_C` + 1).
    e.  Appends a final `Matrix_A` if it exists.

3.  **Horizontal Expansion ('Horizontal_Row' pattern):** Triggered if all '1's are in a single row, spanning multiple columns.
    a.  Determines the marker column as the *leftmost* column containing a '1'.
    b.  Applies the exact same logic as the 'Horizontal_Column' pattern (steps 2a-e).

If the '1' pattern doesn't match these cases, or if no '1' is found, the original input grid is returned.
"""

# --- Helper Functions ---

def find_marker_positions(grid: np.ndarray, marker: int = 1) -> List[Tuple[int, int]]:
    """Finds all (row, col) occurrences of the marker value in the grid."""
    rows, cols = np.where(grid == marker)
    # Convert numpy indices to standard ints for consistency
    return list(zip(rows.tolist(), cols.tolist()))

def determine_pattern(marker_positions: List[Tuple[int, int]], grid_shape: Tuple[int, int]) -> Tuple[str, Optional[Union[int, Tuple[int, int]]]]:
    """
    Determines the pattern ('Vertical', 'Horizontal_Column', 'Horizontal_Row', 'Unknown')
    based on the refined logic derived from examples.

    Returns:
        A tuple: (pattern_type, relevant_indices)
    """
    if not marker_positions:
        return 'Unknown', None # No marker found

    rows, cols = zip(*marker_positions)
    unique_rows = set(rows)
    unique_cols = set(cols)
    num_unique_rows = len(unique_rows)
    num_unique_cols = len(unique_cols)
    min_row, max_row = min(unique_rows), max(unique_rows)
    min_col, max_col = min(unique_cols), max(unique_cols)

    # Calculate derived properties for pattern matching
    is_col_zero = unique_cols == {0}
    is_contiguous_rows = num_unique_rows == (max_row - min_row + 1)
    is_single_col = num_unique_cols == 1
    is_single_row = num_unique_rows == 1

    # Determine pattern based on refined rules with precedence
    if is_col_zero and is_contiguous_rows:
        # Rule 1: Vertical Expansion Pattern
        return 'Vertical', (min_row, max_row)
    elif is_single_col:
        # Rule 2: Horizontal Column Pattern (catches cases not covered by Rule 1)
        # The single column index is min_col (or max_col, they are the same)
        return 'Horizontal_Column', min_col
    elif is_single_row and num_unique_cols > 1:
        # Rule 3: Horizontal Row Pattern
        # Use the leftmost column containing '1' as the marker column index
        return 'Horizontal_Row', min_col
    else:
        # Rule 4: Unknown Pattern
        return 'Unknown', None


# --- Main Transformation Function ---

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule to the input grid based on '1' marker patterns.
    """
    # Handle empty input grid
    if not input_grid or not input_grid[0]:
        return []

    # Convert input to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    grid_shape = grid.shape
    num_rows, num_cols = grid_shape

    # --- Workflow Step 1: Locate Markers ---
    marker_positions = find_marker_positions(grid, 1)

    # Handle case: No markers found
    if not marker_positions:
        return input_grid # Return original grid

    # --- Workflow Step 2: Determine Pattern ---
    pattern_type, indices = determine_pattern(marker_positions, grid_shape)

    # Initialize output grid variable
    output_grid_np = None

    # --- Workflow Step 3: Process by Pattern ---
    if pattern_type == 'Vertical':
        # Vertical Expansion Logic
        start_row, end_row = indices

        # 3a. Partition Grid: Identify Subgrid_A
        subgrid_a = grid[:start_row, :]
        subgrid_a_exists = subgrid_a.size > 0

        # 3b. Create Zero Region: Row_0
        row_0 = np.zeros((1, num_cols), dtype=int)

        # 3c. Calculate Repetitions: Based on marker block height
        repetitions = end_row - start_row + 1

        # 3d. Assemble Repeating Block (Block_V)
        if subgrid_a_exists:
            block_v = np.vstack((subgrid_a, row_0))
        else: # Marker rows started at the first row
            block_v = row_0

        # 3e. Assemble Output Grid: Stack Block_V repeatedly, add final Subgrid_A
        output_parts = []
        for _ in range(repetitions):
            output_parts.append(block_v)
        if subgrid_a_exists:
            output_parts.append(subgrid_a)

        # Perform the vertical stack if parts exist
        if output_parts:
            output_grid_np = np.vstack(output_parts)
        else: # Should not happen if repetitions > 0
             output_grid_np = np.array([[]]) # Empty grid

    elif pattern_type in ['Horizontal_Column', 'Horizontal_Row']:
        # Horizontal Expansion Logic (shared by both patterns)
        marker_col = indices # Already determined correctly in determine_pattern

        # 3a. Partition Grid: Slice into Matrix_A, Column_B, Matrix_C
        matrix_a = grid[:, :marker_col]
        column_b = grid[:, marker_col:marker_col+1] # Keep as 2D column
        matrix_c = grid[:, marker_col+1:]
        matrix_a_exists = matrix_a.size > 0
        matrix_c_exists = matrix_c.size > 0

        # 3b. Create Zero Region: Column_0 (replacing 1s in Column_B)
        column_0 = np.where(column_b == 1, 0, column_b)

        # 3c. Calculate Repetitions: Based on Matrix_C's width
        repetitions = (matrix_c.shape[1] if matrix_c_exists else 0) + 1

        # 3d. Assemble Repeating Block (Block_H)
        if matrix_a_exists:
            block_h = np.hstack((matrix_a, column_0))
        else: # Marker was in the first column
            block_h = column_0

        # 3e. Assemble Output Grid: Concatenate Block_H repeatedly, add final Matrix_A
        output_parts = []
        for _ in range(repetitions):
            output_parts.append(block_h)
        if matrix_a_exists:
            output_parts.append(matrix_a)

        # Perform the horizontal concatenation if parts exist
        if output_parts:
            # Check if block_h itself might be empty column (num_rows x 0)
            # This happens if matrix_a is empty and column_0 is empty (0 rows input?)
            # Unlikely given problem constraints, but hstack needs non-empty arrays
            # Ensure block_h has columns before attempting hstack
             if block_h.shape[1] > 0:
                output_grid_np = np.hstack(output_parts)
             elif matrix_a_exists and matrix_a.shape[1] > 0: # Case: Only final matrix_a exists
                 output_grid_np = matrix_a
             else: # Case: Everything became empty
                 output_grid_np = np.array([[]] * num_rows)
        else: # Should not happen with valid inputs where marker exists
             output_grid_np = np.array([[]] * num_rows) # Empty grid with correct rows

    else: # pattern_type == 'Unknown'
        # --- Workflow Step 4: Handle Unknown Pattern ---
        return input_grid # Return the original input grid

    # --- Workflow Step 5: Final Output Conversion ---
    # Convert the final NumPy array back to a list of lists
    if output_grid_np is not None and output_grid_np.size > 0:
        return output_grid_np.tolist()
    elif output_grid_np is not None and output_grid_np.shape[0] > 0 and output_grid_np.shape[1] == 0:
         # Handle case of empty columns but multiple rows (e.g., hstack result was empty)
         return [[] for _ in range(output_grid_np.shape[0])]
    elif output_grid_np is not None: # Handles empty grid np.array([[]]) from vstack or hstack
        return []
    else: # Should only be reached if pattern was unknown (already handled)
        return input_grid # Failsafe