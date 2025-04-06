
## train_1

**input:**
```
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 6 6 6 0
6 1 1 1 6
```


**output:**
```
0 0 0 0 0
0 0 0 0 0
1 0 0 0 1
0 6 6 6 0
6 1 1 1 6
```


## train_2

**input:**
```
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 8 0 0
8 8 3 8 8
```


**output:**
```
0 0 0 0 0
3 0 0 0 3
0 3 0 3 0
0 0 8 0 0
8 8 3 8 8
```


## train_3

**input:**
```
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 2 2 2 0 0
2 2 4 4 4 2 2
```


**output:**
```
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
4 0 0 0 0 0 4
0 4 0 0 0 4 0
0 0 2 2 2 0 0
2 2 4 4 4 2 2
```


## train_4

**input:**
```
0 0 0
0 2 0
2 4 2
```


**output:**
```
4 0 4
0 2 0
2 4 2
```

Okay, analyzing the provided examples to understand the transformation.

**Perception of Elements:**

1.  **Grids:** The inputs and outputs are 2D grids containing single digits. The digit '0' acts as a background color.
2.  **Objects:** The non-zero digits form structures within the grid. A key structure appears consistently in the lower part of the input grid: a horizontal segment composed of one color (central color, C) flanked on both sides by another color (boundary color, B). Examples: `6 1 1 1 6`, `8 8 3 8 8`, `2 2 4 4 4 2 2`, `2 4 2`.
3.  **Transformation:** The transformation involves identifying this specific `B... C... B...` structure in the lowest part of the input grid and then adding new pixels of the central color (C) to the grid at locations *above* the identified structure. The original input structure remains in the output.
4.  **Propagation:** The placement of the new C-colored pixels follows specific rules based on the properties (colors B and C, and the number N of central C pixels) of the identified structure. There are two types of propagation:
    *   Diagonal: New C pixels appear vertically above the boundary B pixels. The vertical distance depends on B and N.
    *   Central: Sometimes, a new C pixel appears vertically above the center of the C segment. This also depends on B and N, and the vertical distance is consistently 2 rows up.

**YAML Facts:**


```yaml
task: grid_transformation
input_type: 2D grid of digits
output_type: 2D grid of digits (same dimensions as input)
background_color: 0
objects:
  - id: pattern
    description: A horizontal structure found near the bottom of the input grid.
    properties:
      - central_color (C): The color of the central segment (non-zero, different from boundary_color).
      - boundary_color (B): The color flanking the central segment (non-zero, different from central_color).
      - central_segment_length (N): The number of contiguous pixels of the central_color.
      - row_index (r_orig): The row where the pattern is located.
      - boundary_left_col (c_left): The column index of the leftmost boundary pixel B relevant to the pattern.
      - boundary_right_col (c_right): The column index of the rightmost boundary pixel B relevant to the pattern.
      - central_mid_col (c_mid): The column index of the middle pixel of the central segment C (relevant if N is odd).
actions:
  - id: identify_pattern
    description: Scan the input grid from bottom to top to find the first occurrence of the 'pattern' object.
    input: input grid
    output: pattern object properties (C, B, N, r_orig, c_left, c_right, c_mid)
  - id: calculate_shifts
    description: Determine the vertical shifts for propagation based on pattern properties.
    input: pattern object properties (B, N)
    output:
      - diagonal_vertical_shift (V_diag)
      - perform_central_propagation (boolean flag)
    logic:
      - V_diag = 3 if (B == 8) or (B == 2 and N > 1) else 2
      - perform_central_propagation = true if (N == 1 and B == 8) or (N > 1 and B == 2) else false
  - id: apply_propagation
    description: Add new pixels to the output grid based on calculated shifts and pattern properties.
    input: input grid, pattern object properties, shifts
    output: modified output grid
    steps:
      - Copy input grid to output grid.
      - Place C at (r_orig - V_diag, c_left) if within bounds.
      - Place C at (r_orig - V_diag, c_right) if within bounds.
      - If perform_central_propagation is true, place C at (r_orig - 2, c_mid) if within bounds.
relationships:
  - The output grid is derived from the input grid by adding pixels.
  - The added pixels' color matches the central_color (C) of the identified pattern.
  - The locations of added pixels depend on the row (r_orig), boundary columns (c_left, c_right), middle column (c_mid), boundary color (B), and central segment length (N) of the identified pattern.
```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid.
2.  Scan the input grid rows from bottom to top.
3.  Identify the first row (`r_orig`) that contains a horizontal pattern consisting of a contiguous block of one non-zero color (`C`) of length `N`, flanked on both the left and right sides by at least one pixel of a different non-zero color (`B`) within the same row. Record the color `C`, color `B`, length `N`, row index `r_orig`, the column index of the leftmost flanking pixel `B` (`c_left`), the column index of the rightmost flanking pixel `B` (`c_right`), and the column index of the middle pixel of the `C` block (`c_mid` - relevant if `N` is odd).
4.  Once the first such pattern is found, stop scanning.
5.  Determine the vertical shift (`V_diag`) for diagonal propagation: if the boundary color `B` is 8, OR if `B` is 2 AND the central length `N` is greater than 1, set `V_diag` to 3; otherwise, set `V_diag` to 2.
6.  Determine if central propagation should occur: central propagation occurs if (the central length `N` is 1 AND the boundary color `B` is 8) OR if (`N` is greater than 1 AND `B` is 2).
7.  Add new pixels to the output grid:
    a.  Place a pixel of color `C` at coordinates (`r_orig - V_diag`, `c_left`), if these coordinates are within the grid boundaries.
    b.  Place a pixel of color `C` at coordinates (`r_orig - V_diag`, `c_right`), if these coordinates are within the grid boundaries.
    c.  If central propagation is determined to occur (from step 6), place a pixel of color `C` at coordinates (`r_orig - 2`, `c_mid`), if these coordinates are within the grid boundaries.
8.  Return the modified output grid.
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
