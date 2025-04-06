
Previous Code:
```python
import numpy as np
from typing import List, Optional, Tuple

"""
Transforms an input grid based on the presence and location of axes marked by the number 4.

1.  Identifies horizontal and/or vertical axes (rows/columns filled entirely with 4s).
2.  If both a horizontal (at row `h`) and vertical (at column `v`) axis exist:
    - The grid is divided into four quadrants by these axes.
    - The transformation swaps diagonally opposite quadrants:
        - Top-Left swaps with Bottom-Right.
        - Top-Right swaps with Bottom-Left.
    - The axes themselves remain unchanged.
3.  If only a horizontal axis (at row `h`) exists:
    - The transformation swaps the region above the axis with the region below the axis.
    - The axis itself remains unchanged.
4.  If only a vertical axis (at column `v`) exists:
    - The transformation swaps the region to the left of the axis with the region to the right of the axis.
    - The axis itself remains unchanged.
5.  If no axis is found, the grid remains unchanged.
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

    # Initialize output grid as a copy first (handles cases with no axes)
    output_np = np.copy(input_np)

    # Find axes
    h_axis_idx = find_horizontal_axis(input_np)
    v_axis_idx = find_vertical_axis(input_np)

    # Scenario 1: Both horizontal and vertical axes found
    if h_axis_idx is not None and v_axis_idx is not None:
        h = h_axis_idx
        v = v_axis_idx
        # Create a zero-initialized grid to place swapped quadrants
        # This avoids overwriting parts needed for later swaps if done in-place on a copy
        temp_output_np = np.zeros_like(input_np)

        # Copy axes to the temp output
        temp_output_np[h, :] = input_np[h, :]
        temp_output_np[:, v] = input_np[:, v]

        # Swap quadrants
        # Input Top-Left -> Output Bottom-Right
        if h > 0 and v > 0 and h + 1 < rows and v + 1 < cols:
             temp_output_np[h+1:, v+1:] = input_np[:h, :v]
        # Input Top-Right -> Output Bottom-Left
        if h > 0 and v + 1 < cols and h + 1 < rows and v > 0:
            temp_output_np[h+1:, :v] = input_np[:h, v+1:]
        # Input Bottom-Left -> Output Top-Right
        if h + 1 < rows and v > 0 and h > 0 and v + 1 < cols:
            temp_output_np[:h, v+1:] = input_np[h+1:, :v]
        # Input Bottom-Right -> Output Top-Left
        if h + 1 < rows and v + 1 < cols and h > 0 and v > 0:
             temp_output_np[:h, :v] = input_np[h+1:, v+1:]
             
        # Handle edge cases where quadrants might touch the grid boundary directly
        # (e.g., h=0 or v=0 or h=rows-1 or v=cols-1)
        # The slicing logic generally handles these, but explicit checks can clarify
        # Example: If h=0, input[:h, ...] is empty, which is correct.
        # Example: If h=rows-1, input[h+1:, ...] is empty, which is correct.

        output_np = temp_output_np # Assign the result

    # Scenario 2: Only horizontal axis found
    elif h_axis_idx is not None:
        h = h_axis_idx
        # Create a zero-initialized grid
        temp_output_np = np.zeros_like(input_np)
        
        # Copy the axis
        temp_output_np[h, :] = input_np[h, :]

        # Swap upper and lower regions
        # Input Upper -> Output Lower
        if h > 0 and h + 1 < rows:
             temp_output_np[h+1:, :] = input_np[:h, :]
        # Input Lower -> Output Upper
        if h + 1 < rows and h > 0:
            temp_output_np[:h, :] = input_np[h+1:, :]
            
        output_np = temp_output_np

    # Scenario 3: Only vertical axis found
    elif v_axis_idx is not None:
        v = v_axis_idx
        # Create a zero-initialized grid
        temp_output_np = np.zeros_like(input_np)
        
        # Copy the axis
        temp_output_np[:, v] = input_np[:, v]

        # Swap left and right regions
        # Input Left -> Output Right
        if v > 0 and v + 1 < cols:
            temp_output_np[:, v+1:] = input_np[:, :v]
        # Input Right -> Output Left
        if v + 1 < cols and v > 0:
            temp_output_np[:, :v] = input_np[:, v+1:]

        output_np = temp_output_np

    # Scenario 4: No axis found - output_np remains the initial copy of input_np

    # Convert final numpy array back to list of lists
    return output_np.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 0 2 0
0 0 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 1 0 0 0 0
0 0 1 0 0 0 0 0 0
0 0 2 0 0 0 0 2 0
0 2 0 0 0 5 5 0 0
0 0 0 0 0 0 0 0 0
4 4 4 4 4 4 4 4 4
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 0 2 0
0 0 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 1 0 0 0 0
0 0 1 0 0 0 0 0 0
0 0 2 0 0 0 0 2 0
0 2 0 0 0 5 5 0 0
0 0 0 0 0 0 0 0 0
4 4 4 4 4 4 4 4 4
0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 0 2 0
0 0 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 1 0 0 0 0
0 0 1 0 0 0 0 0 0
0 0 2 0 0 0 0 2 0
0 2 0 0 0 5 5 0 0
0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
4 4 4 4 4 4 4 4 4
0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 0 2 0
0 0 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 1 0 0 0 0
0 0 1 0 0 0 0 0 0
0 0 2 0 0 0 0 2 0
0 2 0 0 0 5 5 0 0
0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 10
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 11.69590643274853

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 3 0 0 0 3 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 8 7 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 0 3 0 4 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 4 0 0 0 0 0 7 0 0 0
0 0 0 2 0 0 0 0 0 4 0 0 0 2 0 0 0 0 0
0 0 2 0 0 0 0 0 0 4 0 0 2 0 0 0 0 0 0
0 3 0 0 0 3 0 0 0 4 0 3 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 8 7 0 0 0 0 4 0 0 0 8 7 0 0 0 0
0 0 0 0 8 0 0 3 0 4 0 0 0 0 8 0 0 3 0
0 7 0 0 0 0 0 0 0 4 0 7 0 0 0 0 0 0 0
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 4 0 0 0 0 0 7 0 0 0
0 0 0 2 0 0 0 0 0 4 0 0 0 2 0 0 0 0 0
0 0 2 0 0 0 0 0 0 4 0 0 2 0 0 0 0 0 0
0 3 0 0 0 3 0 0 0 4 0 3 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 8 7 0 0 0 0 4 0 0 0 8 7 0 0 0 0
0 0 0 0 8 0 0 3 0 4 0 0 0 0 8 0 0 3 0
0 7 0 0 0 0 0 0 0 4 0 7 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 3 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0 0 8 7 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0 0 0 8 0 0 3 0
0 0 0 0 0 0 0 0 0 4 0 7 0 0 0 0 0 0 0
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 30
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 16.62049861495845
