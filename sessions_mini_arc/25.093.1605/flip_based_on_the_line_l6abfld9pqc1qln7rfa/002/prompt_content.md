
Previous Code:
```python
import numpy as np
import copy

"""
Transformation Rule:

The transformation depends on whether the non-zero pattern in the input grid touches the bottom edge.

1. Find all non-zero cells and determine the grid dimensions (H, W).
2. Find the maximum row index (`max_r_nz`) occupied by any non-zero cell.

3. **Case 1: Pattern does NOT touch the bottom edge (`max_r_nz < H - 1`)**
   - Shift the entire non-zero pattern down by one row.
   - Create an output grid of the same dimensions, initialized with zeros.
   - For each non-zero cell `input[r][c]`, set `output[r+1][c]` to the value of `input[r][c]`.

4. **Case 2: Pattern DOES touch the bottom edge (`max_r_nz == H - 1`)**
   - Find the minimum row index (`min_r_nz`), minimum column index (`min_c_nz`), and maximum column index (`max_c_nz`) occupied by non-zero cells.
   - **Subcase 2a: Reflection condition**
     - If the pattern touches the top edge (`min_r_nz == 0`), touches the left edge (`min_c_nz == 0`), AND does NOT touch the right edge (`max_c_nz < W - 1`):
       - Perform a horizontal reflection of the pattern across the vertical center line.
       - Create an output grid of the same dimensions, initialized with zeros.
       - For each non-zero cell `input[r][c]`, set `output[r][W - 1 - c]` to the value of `input[r][c]`.
   - **Subcase 2b: Pixel removal condition (Otherwise)**
     - Find the row index (`target_r`) that contains the maximum number of non-zero elements. If there are multiple such rows, choose the one with the smallest row index.
     - Find the maximum column index (`target_c`) within that `target_r` such that `input[target_r][target_c]` is non-zero.
     - Create the output grid as a copy of the input grid.
     - Set the value of the cell `output[target_r][target_c]` to 0.

5. Return the resulting output grid.
"""

def find_non_zero_cells(grid):
    """Finds coordinates and values of non-zero cells."""
    non_zero = []
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if val != 0:
                non_zero.append({'r': r, 'c': c, 'val': val})
    return non_zero

def get_grid_dims(grid):
    """Gets the dimensions (height, width) of the grid."""
    if not grid:
        return 0, 0
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    return height, width

def transform(input_grid):
    """
    Applies the transformation rule based on pattern position and characteristics.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Find non-zero cells
    non_zero_cells = []
    for r in range(height):
        for c in range(width):
            if input_np[r, c] != 0:
                non_zero_cells.append((r, c, input_np[r, c]))

    # Handle empty grid or grid with only zeros
    if not non_zero_cells:
        return input_np.tolist()

    # Determine bounding box and edge touching properties
    min_r_nz = min(r for r, c, v in non_zero_cells)
    max_r_nz = max(r for r, c, v in non_zero_cells)
    min_c_nz = min(c for r, c, v in non_zero_cells)
    max_c_nz = max(c for r, c, v in non_zero_cells)

    # Initialize output grid
    output_np = np.zeros_like(input_np)

    # Case 1: Pattern does NOT touch the bottom edge
    if max_r_nz < height - 1:
        # Shift down by one row
        for r, c, val in non_zero_cells:
            if r + 1 < height: # Ensure shift stays within bounds
                output_np[r + 1, c] = val
        return output_np.tolist()

    # Case 2: Pattern DOES touch the bottom edge
    else:
        # Subcase 2a: Reflection condition
        touches_top = (min_r_nz == 0)
        touches_left = (min_c_nz == 0)
        touches_right = (max_c_nz == width - 1)

        if touches_top and touches_left and not touches_right:
            # Perform horizontal reflection
            for r, c, val in non_zero_cells:
                output_np[r, width - 1 - c] = val
            return output_np.tolist()

        # Subcase 2b: Pixel removal condition
        else:
            # Find the row with the maximum number of non-zero elements
            max_non_zeros_in_row = -1
            target_r = -1
            for r in range(height):
                count = np.count_nonzero(input_np[r, :])
                if count > max_non_zeros_in_row:
                    max_non_zeros_in_row = count
                    target_r = r
                # Tie-breaking: choose the lowest row index (handled implicitly by loop order)

            if target_r == -1: # Should not happen if there are non-zero cells, but safety check
                 return input_np.tolist()

            # Find the rightmost non-zero column in that target row
            target_c = -1
            for c in range(width - 1, -1, -1): # Iterate from right to left
                if input_np[target_r, c] != 0:
                    target_c = c
                    break
            
            # Copy input and modify the target cell
            output_np = np.copy(input_np)
            if target_r != -1 and target_c != -1:
                 output_np[target_r, target_c] = 0
            
            return output_np.tolist()

```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
3 0 3 0 0
3 3 3 0 0
0 3 3 0 0
3 3 3 0 0
3 0 3 0 0
```
Expected Output:
```
0 0 3 0 3
0 0 3 3 3
0 0 3 3 0
0 0 3 3 3
0 0 3 0 3
```
Transformed Output:
```
0 0 3 0 3
0 0 3 3 3
0 0 3 3 0
0 0 3 3 3
0 0 3 0 3
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0.0

## Example 2:
Input:
```
6 0 6 0 6
6 6 6 6 6
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0
6 6 6 6 6
6 0 6 0 6
0 0 0 0 0
0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0
6 0 6 0 6
6 6 6 6 6
0 0 0 0 0
0 0 0 0 0
```
Match: False
Pixels Off: 4
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 16.0

## Example 3:
Input:
```
0 0 0 0 0
0 1 0 1 0
1 1 1 1 1
0 0 0 0 0
0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0
0 0 0 0 0
1 1 1 1 1
0 1 0 1 0
0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0
0 0 0 0 0
0 1 0 1 0
1 1 1 1 1
0 0 0 0 0
```
Match: False
Pixels Off: 6
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 24.0

## Example 4:
Input:
```
0 9 0 0 0
0 9 0 0 0
9 9 9 9 0
0 9 0 0 0
0 9 0 0 0
```
Expected Output:
```
0 9 0 0 0
0 9 0 0 0
9 9 9 0 0
0 9 0 0 0
0 9 0 0 0
```
Transformed Output:
```
0 0 0 9 0
0 0 0 9 0
0 9 9 9 9
0 0 0 9 0
0 0 0 9 0
```
Match: False
Pixels Off: 11
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 87.99999999999999

Test Set Results:

## Example 1:
Input:
```
0 0 8 0 0
0 8 8 0 0
8 8 8 8 8
0 0 0 0 0
0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0
0 0 0 0 0
8 8 8 8 8
0 8 8 0 0
0 0 8 0 0
```
Transformed Output:
```
0 0 0 0 0
0 0 8 0 0
0 8 8 0 0
8 8 8 8 8
0 0 0 0 0
```
Match: False
Pixels Off: 8
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 32.0
