
Previous Code:
```python
import copy
import math

"""
Transformation rule:
1. Identify a specific horizontal pattern in the lower part of the input grid. The pattern consists of a central segment of color 'C' (length N) flanked immediately on both sides by a different non-zero color 'B'.
2. Determine vertical propagation shifts based on the properties (B, N) of the identified pattern.
3. Add new pixels of color 'C' to the grid at positions determined by these shifts relative to the original pattern's location. The original pattern remains unchanged.

Specifically:
- Scan rows from bottom to top to find the first occurrence of the pattern 'B... C... B...' where B and C are distinct non-zero colors.
- Record the row index (r_orig), the central color (C), the boundary color (B), the length of the central segment (N), the column index of the leftmost boundary pixel (c_left), the column index of the rightmost boundary pixel (c_right), and the column index of the middle pixel of the central segment (c_mid).
- Calculate the diagonal vertical shift (V_diag): V_diag is 3 if (B == 8) or (B == 2 and N > 1), otherwise V_diag is 2.
- Determine if central propagation should occur: True if (N == 1 and B == 8) or (N > 1 and B == 2).
- Place new pixels of color C at:
    - (r_orig - V_diag, c_left)
    - (r_orig - V_diag, c_right)
    - (r_orig - 2, c_mid) (only if central propagation is determined to occur)
- Ensure added pixels are within grid boundaries.
"""

def find_pattern(grid: list[list[int]]) -> dict | None:
    """
    Finds the first occurrence (from bottom) of the B-C-B pattern.

    Args:
        grid: The input grid.

    Returns:
        A dictionary containing pattern details (C, B, N, r_orig, c_left, c_right, c_mid)
        or None if no pattern is found.
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    for r_orig in range(rows - 1, -1, -1): # Scan rows from bottom up
        row = grid[r_orig]
        c = 0
        while c < cols:
            if row[c] != 0:
                central_color_C = row[c]
                # Find the extent of the central segment
                start_c = c
                while c + 1 < cols and row[c + 1] == central_color_C:
                    c += 1
                end_c = c
                central_segment_length_N = end_c - start_c + 1

                # Check for left boundary pixel B
                c_left = start_c - 1
                if c_left >= 0:
                    boundary_color_B = row[c_left]
                    if boundary_color_B != 0 and boundary_color_B != central_color_C:
                        # Check for right boundary pixel B (must be the *same* B)
                        c_right = end_c + 1
                        if c_right < cols and row[c_right] == boundary_color_B:
                            # Pattern found!
                            # Calculate middle column (integer division for even N)
                            c_mid = start_c + (central_segment_length_N - 1) // 2
                            return {
                                "C": central_color_C,
                                "B": boundary_color_B,
                                "N": central_segment_length_N,
                                "r_orig": r_orig,
                                "c_left": c_left,
                                "c_right": c_right,
                                "c_mid": c_mid,
                            }
                # Move to the next potential segment start
                c = end_c + 1
            else:
                c += 1 # Move past zero
    return None # No pattern found

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: The 2D list representing the input grid.

    Returns:
        The transformed 2D list representing the output grid.
    """
    # Initialize output_grid as a deep copy of the input grid
    output_grid = copy.deepcopy(input_grid)
    rows = len(output_grid)
    cols = len(output_grid[0]) if rows > 0 else 0

    # 1. Find the B-C-B pattern
    pattern_info = find_pattern(input_grid)

    if pattern_info:
        # Extract pattern details
        C = pattern_info["C"]
        B = pattern_info["B"]
        N = pattern_info["N"]
        r_orig = pattern_info["r_orig"]
        c_left = pattern_info["c_left"]
        c_right = pattern_info["c_right"]
        c_mid = pattern_info["c_mid"]

        # 2. Calculate shifts and propagation flags
        V_diag = 3 if (B == 8) or (B == 2 and N > 1) else 2
        perform_central_propagation = (N == 1 and B == 8) or (N > 1 and B == 2)

        # 3. Apply propagation - add new pixels to the output grid
        # Diagonal propagation
        prop_r_diag = r_orig - V_diag
        if 0 <= prop_r_diag < rows:
            if 0 <= c_left < cols:
                output_grid[prop_r_diag][c_left] = C
            if 0 <= c_right < cols:
                output_grid[prop_r_diag][c_right] = C

        # Central propagation
        if perform_central_propagation:
            prop_r_central = r_orig - 2
            if 0 <= prop_r_central < rows and 0 <= c_mid < cols:
                 output_grid[prop_r_central][c_mid] = C

    # Return the potentially modified grid
    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 6 6 6 0
6 1 1 1 6
```
Expected Output:
```
0 0 0 0 0
0 0 0 0 0
1 0 0 0 1
0 6 6 6 0
6 1 1 1 6
```
Transformed Output:
```
0 0 0 0 0
0 0 0 0 0
1 0 0 0 1
0 6 6 6 0
6 1 1 1 6
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
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 8 0 0
8 8 3 8 8
```
Expected Output:
```
0 0 0 0 0
3 0 0 0 3
0 3 0 3 0
0 0 8 0 0
8 8 3 8 8
```
Transformed Output:
```
0 0 0 0 0
0 3 0 3 0
0 0 3 0 0
0 0 8 0 0
8 8 3 8 8
```
Match: False
Pixels Off: 7
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 56.0

## Example 3:
Input:
```
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 2 2 2 0 0
2 2 4 4 4 2 2
```
Expected Output:
```
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
4 0 0 0 0 0 4
0 4 0 0 0 4 0
0 0 2 2 2 0 0
2 2 4 4 4 2 2
```
Transformed Output:
```
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 4 0 0 0 4 0
0 0 0 4 0 0 0
0 0 2 2 2 0 0
2 2 4 4 4 2 2
```
Match: False
Pixels Off: 7
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 28.571428571428584

## Example 4:
Input:
```
0 0 0
0 2 0
2 4 2
```
Expected Output:
```
4 0 4
0 2 0
2 4 2
```
Transformed Output:
```
4 0 4
0 2 0
2 4 2
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0.0
