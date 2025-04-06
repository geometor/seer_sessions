import numpy as np
from typing import List, Optional, Tuple

"""
Transforms an input grid based on the presence and location of axes marked by the number 4.

The transformation rule depends on the number of axes found:

1.  **Identify Axes:** Locate a horizontal axis (row `h` where all elements are 4) and/or a vertical axis (column `v` where all elements are 4).

2.  **Transformation Logic:**
    *   **No Axes Found:** The output grid is identical to the input grid.
    *   **Only Horizontal Axis `h` Found:** The content from the upper region (rows < h) of the input is moved to the lower region (rows > h) of the output. The axis row `h` is copied. All other cells in the output are 0.
    *   **Only Vertical Axis `v` Found:** The content from the left region (cols < v) of the input is moved to the right region (cols > v) of the output. The axis column `v` is copied. All other cells in the output are 0. (This case is inferred by symmetry but not explicitly shown in examples).
    *   **Both Horizontal Axis `h` and Vertical Axis `v` Found:** The grid is divided into four quadrants. The transformation swaps diagonally opposite quadrants: Top-Left swaps with Bottom-Right, and Top-Right swaps with Bottom-Left. The axis row `h` and axis column `v` are copied.

3.  **Output:** Return the transformed grid.
"""

def find_horizontal_axis(grid: np.ndarray) -> Optional[int]:
    """Finds the row index of a horizontal axis (all 4s)."""
    rows, _ = grid.shape
    for r in range(rows):
        if np.all(grid[r, :] == 4):
            return r
    return None

def find_vertical_axis(grid: np.ndarray) -> Optional[int]:
    """Finds the column index of a vertical axis (all 4s)."""
    _, cols = grid.shape
    for c in range(cols):
        if np.all(grid[:, c] == 4):
            return c
    return None

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule based on identified axes of 4s.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape

    # Find axes
    h_axis_idx = find_horizontal_axis(input_np)
    v_axis_idx = find_vertical_axis(input_np)

    # Case 4: No axes found - return input unchanged
    if h_axis_idx is None and v_axis_idx is None:
        return input_grid

    # Initialize output grid with zeros for transformation cases
    output_np = np.zeros_like(input_np)

    # Case 1: Both horizontal and vertical axes found (Swap Quadrants)
    if h_axis_idx is not None and v_axis_idx is not None:
        h = h_axis_idx
        v = v_axis_idx

        # Copy axes to the output
        output_np[h, :] = input_np[h, :]
        output_np[:, v] = input_np[:, v] # Note: Intersection point input_np[h,v] is copied twice, which is fine as it's 4.

        # Swap quadrants (copying from input to output's swapped location)
        # Input Top-Left -> Output Bottom-Right
        if h > 0 and v > 0 and h + 1 < rows and v + 1 < cols:
             output_np[h+1:, v+1:] = input_np[:h, :v]
        # Input Top-Right -> Output Bottom-Left
        if h > 0 and v + 1 < cols and h + 1 < rows and v > 0:
            output_np[h+1:, :v] = input_np[:h, v+1:]
        # Input Bottom-Left -> Output Top-Right
        if h + 1 < rows and v > 0 and h > 0 and v + 1 < cols:
            output_np[:h, v+1:] = input_np[h+1:, :v]
        # Input Bottom-Right -> Output Top-Left
        if h + 1 < rows and v + 1 < cols and h > 0 and v > 0:
             output_np[:h, :v] = input_np[h+1:, v+1:]

    # Case 2: Only horizontal axis found (Move Upper to Lower)
    elif h_axis_idx is not None:
        h = h_axis_idx

        # Copy the axis
        output_np[h, :] = input_np[h, :]

        # Move upper region to lower region
        # Input Upper -> Output Lower
        if h > 0 and h + 1 < rows:
             output_np[h+1:, :] = input_np[:h, :]
        # The original upper region and non-axis parts of lower region remain 0

    # Case 3: Only vertical axis found (Move Left to Right)
    elif v_axis_idx is not None:
        v = v_axis_idx

        # Copy the axis
        output_np[:, v] = input_np[:, v]

        # Move left region to right region
        # Input Left -> Output Right
        if v > 0 and v + 1 < cols:
            output_np[:, v+1:] = input_np[:, :v]
        # The original left region and non-axis parts of right region remain 0

    # Convert final numpy array back to list of lists
    return output_np.tolist()