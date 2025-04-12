```python
import numpy as np
from scipy.ndimage import label

"""
Reorganizes an input grid based on the configuration of separator lines ('6')
and the resulting partitioning or quadrant structure. Uses '7' as background.
Operates in one of three modes: Split Vertical, Split Horizontal, or Extract Quadrant.

1.  **Analyze Grid Structure:**
    *   Find horizontal ('6' rows) and vertical ('6' columns) separators.
    *   Count distinct pattern regions (connected components != 6 and != 7).
2.  **Determine Transformation Mode:**
    *   **Split Vertical:** If ONLY vertical separators exist AND they perfectly partition the grid width (cols = num_patterns * 5 + num_v_sep).
    *   **Split Horizontal:** If ONLY horizontal separators exist, len(h_sep) > 1, AND they perfectly partition the grid height (rows = num_patterns * 5 + num_h_sep).
    *   **Extract Quadrant:** If exactly one H and one V separator exist, num_patterns is a perfect square (e.g., 4), AND grid dimensions fit (rows = cols = sqrt(num_patterns) * 5 + 1).
3.  **Execute Transformation:**
    *   **Split Vertical:** Extract subgrids (L-to-R), stack vertically with H-separators.
    *   **Split Horizontal:** Extract subgrids, reverse order (B-to-T), concatenate horizontally with V-separators.
    *   **Extract Quadrant:** Extract 5x5 quadrants (TL, TR, BL, BR), stack vertically in TL, BR, TR, BL order with H-separators.
4.  **Output:** Return the transformed grid as a list of lists, or empty list if no mode applies.
"""

# --- Helper Functions ---

def find_horizontal_separators(grid_np: np.ndarray) -> list[int]:
    """Finds indices of rows composed entirely of 6."""
    separator_digit = 6
    rows, _ = grid_np.shape
    return [r for r in range(rows) if np.all(grid_np[r, :] == separator_digit)]

def find_vertical_separators(grid_np: np.ndarray) -> list[int]:
    """Finds indices of columns composed entirely of 6."""
    separator_digit = 6
    _, cols = grid_np.shape
    return [c for c in range(cols) if np.all(grid_np[:, c] == separator_digit)]

def count_patterns(grid_np: np.ndarray) -> int:
    """Counts distinct connected regions of non-background (7) and non-separator (6) digits."""
    background_digit = 7
    separator_digit = 6
    mask = (grid_np != background_digit) & (grid_np != separator_digit)
    _, num_features = label(mask)
    return num_features

def check_partitioning(grid_shape: tuple[int, int], separator_indices: list[int], num_patterns: int, axis: int) -> bool:
    """Checks if separators perfectly partition the grid along the given axis (0 for H, 1 for V), assuming 5x5 patterns."""
    if num_patterns == 0: return False # Cannot partition if no patterns
    rows, cols = grid_shape
    pattern_dim_size = 5
    num_separators = len(separator_indices)
    if axis == 0: # Horizontal separators, check rows
        expected_rows = num_patterns * pattern_dim_size + num_separators
        return rows == expected_rows
    else: # Vertical separators, check columns
        expected_cols = num_patterns * pattern_dim_size + num_separators
        return cols == expected_cols

def check_quadrant_conditions(grid_shape: tuple[int, int], h_sep: list[int], v_sep: list[int], num_patterns: int) -> bool:
    """Checks conditions for Extract Quadrant mode."""
    rows, cols = grid_shape
    pattern_dim_size = 5
    # Expect exactly 1 H sep and 1 V sep
    if len(h_sep) != 1 or len(v_sep) != 1:
        return False
    # Expect num_patterns to be a non-zero perfect square (e.g., 4)
    if num_patterns == 0: return False
    num_patterns_sqrt = np.sqrt(num_patterns)
    if num_patterns_sqrt != int(num_patterns_sqrt):
        return False
    # Check grid dimensions match expectation: sqrt(patterns)*5 + 1
    expected_dim = int(num_patterns_sqrt) * pattern_dim_size + 1
    return rows == expected_dim and cols == expected_dim

def get_subgrids(grid_np: np.ndarray, separator_indices: list[int], axis: int) -> list[np.ndarray]:
    """Extracts subgrids based on separator indices along a given axis."""
    subgrids = []
    start = 0
    for idx in separator_indices:
        if axis == 0: # Horizontal separators -> split rows
            subgrid = grid_np[start:idx, :]
        else: # Vertical separators -> split columns
            subgrid = grid_np[:, start:idx]
        if subgrid.size > 0: # Avoid empty subgrids
            subgrids.append(subgrid)
        start = idx + 1
    # Add the last subgrid
    if axis == 0:
        subgrid = grid_np[start:, :]
    else:
        subgrid = grid_np[:, start:]
    if subgrid.size > 0:
        subgrids.append(subgrid)
    return subgrids

# --- Main Transformation Function ---

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    # Handle empty input
    if not input_grid or not input_grid[0]:
        return []

    # Convert to numpy array
    grid_np = np.array(input_grid, dtype=int)
    rows, cols = grid_np.shape
    separator_digit = 6
    pattern_dim_size = 5 # Assumed size for patterns/quadrants

    # --- 1. Analyze Grid Structure ---
    h_separators = find_horizontal_separators(grid_np)
    v_separators = find_vertical_separators(grid_np)
    num_patterns = count_patterns(grid_np)

    # --- 2. Determine Transformation Mode ---
    mode = 'unknown'
    partitions_h = check_partitioning(grid_np.shape, h_separators, num_patterns, axis=0)
    partitions_v = check_partitioning(grid_np.shape, v_separators, num_patterns, axis=1)
    quadrant_conditions = check_quadrant_conditions(grid_np.shape, h_separators, v_separators, num_patterns)

    if v_separators and not h_separators and partitions_v:
        mode = 'split_vertical'
    elif h_separators and not v_separators and len(h_separators) > 1 and partitions_h:
        # Original logic required > 1 H separator for this mode based on examples
        mode = 'split_horizontal'
    elif quadrant_conditions:
        mode = 'extract_quadrant'

    # --- 3. Execute Transformation ---
    output_grid_np = None

    # ** Mode 1: Split Vertical **
    if mode == 'split_vertical':
        subgrids = get_subgrids(grid_np, v_separators, axis=1)
        if subgrids:
            output_parts = []
            separator_row = np.full((1, subgrids[0].shape[1]), separator_digit, dtype=int)
            for i, subgrid in enumerate(subgrids):
                output_parts.append(subgrid)
                if i < len(subgrids) - 1:
                    output_parts.append(separator_row)
            if output_parts:
                output_grid_np = np.vstack(output_parts)

    # ** Mode 2: Split Horizontal **
    elif mode == 'split_horizontal':
        subgrids = get_subgrids(grid_np, h_separators, axis=0)
        subgrids.reverse() # Order bottom-to-top
        if subgrids:
            output_parts = []
            separator_col = np.full((subgrids[0].shape[0], 1), separator_digit, dtype=int)
            for i, subgrid in enumerate(subgrids):
                output_parts.append(subgrid)
                if i < len(subgrids) - 1:
                    output_parts.append(separator_col)
            if output_parts:
                output_grid_np = np.hstack(output_parts)

    # ** Mode 3: Extract Quadrant **
    elif mode == 'extract_quadrant':
        h_idx = h_separators[0]
        v_idx = v_separators[0]

        # Extract the four quadrants (assuming 5x5 based on conditions check)
        quad_tl = grid_np[0:h_idx, 0:v_idx]
        quad_tr = grid_np[0:h_idx, v_idx+1:cols]
        quad_bl = grid_np[h_idx+1:rows, 0:v_idx]
        quad_br = grid_np[h_idx+1:rows, v_idx+1:cols]

        # Define the separator row (width should match quadrant width)
        separator_row = np.full((1, pattern_dim_size), separator_digit, dtype=int)

        # Stack in TL, BR, TR, BL order
        output_parts = [quad_tl, separator_row, quad_br, separator_row, quad_tr, separator_row, quad_bl]
        output_grid_np = np.vstack(output_parts)

    # --- 4. Final Output ---
    if output_grid_np is None:
        return [] # Return empty list if mode was 'unknown' or execution failed
    else:
        return output_grid_np.tolist()
```