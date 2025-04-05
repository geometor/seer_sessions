```python
import numpy as np

"""
Transformation Rule:
1. Find the index (`idx_2`) of the digit '2' (boundary_marker) in the input sequence (1D NumPy array).
2. If '2' is not found, return the original sequence.
3. Process the left side:
    a. Check if an element exists immediately to the left (`idx_2 > 0`) and if this element is '0' (fillable_space).
    b. If both conditions are true, scan leftwards from `idx_2 - 2` to find the index (`idx_left`) and value (`X_left`) of the first non-zero digit.
    c. If such a digit `X_left` is found and its value is not '2', replace all elements in the range `[idx_left + 1, idx_2 - 1]` (inclusive) with `X_left`.
4. Process the right side:
    a. Check if an element exists immediately to the right (`idx_2 < length - 1`) and if this element is '0'.
    b. If both conditions are true, scan rightwards from `idx_2 + 2` to find the index (`idx_right`) and value (`X_right`) of the first non-zero digit.
    c. If such a digit `X_right` is found and its value is not '2', replace all elements in the range `[idx_2 + 1, idx_right - 1]` (inclusive) with `X_right`.
5. Return the modified sequence. The left and right side processing are independent.
"""

BOUNDARY_MARKER = 2
FILLABLE_SPACE = 0

def _find_marker_index(grid: np.ndarray, marker: int) -> int:
    """Finds the index of the first occurrence of the marker in the grid."""
    indices = np.where(grid == marker)[0]
    return indices[0] if len(indices) > 0 else -1

def _scan_left_for_source(grid: np.ndarray, start_scan_idx: int) -> tuple[int, int]:
    """
    Scans leftwards from start_scan_idx to find the index and value
    of the first non-zero digit encountered.
    Returns (-1, -1) if no non-zero digit is found or scan goes out of bounds.
    """
    for i in range(start_scan_idx, -1, -1):
        if grid[i] != FILLABLE_SPACE:
            return i, grid[i] # index, value
    return -1, -1 # index, value

def _scan_right_for_source(grid: np.ndarray, start_scan_idx: int) -> tuple[int, int]:
    """
    Scans rightwards from start_scan_idx to find the index and value
    of the first non-zero digit encountered.
    Returns (-1, -1) if no non-zero digit is found or scan goes out of bounds.
    """
    n = len(grid)
    for i in range(start_scan_idx, n):
        if grid[i] != FILLABLE_SPACE:
            return i, grid[i] # index, value
    return -1, -1 # index, value

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule based on the boundary marker '2'.
    """
    # initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    n = len(output_grid)

    # 1. Find the index of the boundary marker '2'
    idx_marker = _find_marker_index(output_grid, BOUNDARY_MARKER)

    # 2. If '2' is not found, return the original sequence
    if idx_marker == -1:
        return output_grid

    # 3. Process Left Side
    # 3a. Check if adjacent left element exists and is fillable space
    if idx_marker > 0 and output_grid[idx_marker - 1] == FILLABLE_SPACE:
        # 3b. Scan left for the first non-zero digit (potential source)
        left_source_idx, left_source_value = _scan_left_for_source(output_grid, idx_marker - 2)

        # 3c. If a non-zero source is found and it's not the boundary marker itself
        if left_source_idx != -1 and left_source_value != BOUNDARY_MARKER:
            # Fill the region between the source and the boundary marker
            fill_start_left = left_source_idx + 1
            fill_end_left = idx_marker # Slice goes up to, but not including, idx_marker
            if fill_start_left < fill_end_left: # Check if range is valid
                output_grid[fill_start_left:fill_end_left] = left_source_value

    # 4. Process Right Side
    # 4a. Check if adjacent right element exists and is fillable space
    if idx_marker < n - 1 and output_grid[idx_marker + 1] == FILLABLE_SPACE:
        # 4b. Scan right for the first non-zero digit (potential source)
        right_source_idx, right_source_value = _scan_right_for_source(output_grid, idx_marker + 2)

        # 4c. If a non-zero source is found and it's not the boundary marker itself
        if right_source_idx != -1 and right_source_value != BOUNDARY_MARKER:
            # Fill the region between the boundary marker and the source
            fill_start_right = idx_marker + 1
            fill_end_right = right_source_idx # Slice goes up to, but not including, idx_right
            if fill_start_right < fill_end_right: # Check if range is valid
                output_grid[fill_start_right:fill_end_right] = right_source_value

    # 5. Return the modified grid
    return output_grid
```