
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 1 1 2 0 0 2 1 1 0
0 1 1 2 0 0 2 1 1 0
0 2 2 0 0 0 0 2 2 0
0 1 1 0 0 0 0 1 1 0
0 1 1 0 0 0 0 1 1 0
0 2 2 0 0 0 0 2 2 0
0 1 1 2 1 1 2 1 1 0
0 1 1 2 1 1 2 1 1 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 1 1 2 1 1 2 1 1 0
0 1 1 2 1 1 2 1 1 0
0 2 2 0 0 0 0 2 2 0
0 1 1 0 0 0 0 1 1 0
0 1 1 0 0 0 0 1 1 0
0 2 2 0 0 0 0 2 2 0
0 1 1 2 1 1 2 1 1 0
0 1 1 2 1 1 2 1 1 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 2 6 6 6 6 2 0
0 6 0 0 0 0 6 0
0 6 0 0 0 0 6 0
0 6 0 0 0 0 6 0
0 6 0 0 0 0 6 0
0 2 6 6 0 0 2 0
```


**output:**
```
0 2 6 6 6 6 2 0
0 6 0 0 0 0 6 0
0 6 0 0 0 0 6 0
0 6 0 0 0 0 6 0
0 6 0 0 0 0 6 0
0 2 6 6 6 6 2 0
```

*   **Perception of Elements:**
    *   The inputs are grids containing a background color (white - 0) and several objects or patterns composed of other colors (blue - 1, red - 2, magenta - 6).
    *   The core feature seems to be pairs of adjacent white pixels (`0 0`) occurring horizontally within rows.
    *   The transformation specifically targets these `0 0` pairs based on their horizontal context (neighboring pixels).
    *   Two distinct transformation rules seem to apply depending on the symmetry of the pattern surrounding the `0 0` pair.

*   **YAML Facts:**
    
```yaml
    task_type: pattern_completion
    focus: local_horizontal_patterns
    elements:
      - element: pixel_pair
        property: horizontal_adjacency
        value: white (0)
        notation: '0 0'
      - element: context
        property: flanking_pixels
        description: Pixels immediately to the left (C) and right (D) of the '0 0' pair.
        notation: 'C 0 0 D'
      - element: context
        property: extended_context
        description: Pixels further left (X, Y) and right (Z, W) of the C and D pixels.
        notation: 'X Y C 0 0 D Z W'
      - element: symmetry
        property: pattern_reflection
        description: Checks if the pattern reflects around the central '0 0' pair (C==D, Y==Z, X==W).
      - element: fill_color
        property: determined_by_context
        description: The color used to replace the '0 0' pair depends on symmetry and flanking/context pixels.
    actions:
      - action: find_pattern
        target: horizontal sequence 'C 0 0 D' where C and D are any color, and the middle pixels are white (0).
      - action: evaluate_symmetry
        target: the pattern 'X Y C 0 0 D Z W' surrounding the '0 0' pair.
      - action: replace_pixels
        target: the '0 0' pair.
        condition: based on symmetry evaluation.
        details:
          - if symmetric ('X Y C 0 0 C Y X', C>0, Y>0): replace '0 0' with 'Y Y'.
          - if asymmetric or bounds/color conditions fail: replace '0 0' with 'C C' (if C>0).
    ```


*   **Natural Language Program:**
    1.  Create a copy of the input grid to serve as the output grid.
    2.  Iterate through each row (`r`) of the input grid.
    3.  Within each row, iterate through each possible starting column index `c` such that the pattern `C 0 0 D` can be evaluated (i.e., from index 0 up to `width - 4`).
    4.  Check if the pixels at `(r, c+1)` and `(r, c+2)` are both white (0).
    5.  If they are, identify the left flanking pixel `C = input_grid[r, c]` and the right flanking pixel `D = input_grid[r, c+3]`.
    6.  Attempt to identify the extended context pixels: `Y = input_grid[r, c-1]`, `X = input_grid[r, c-2]`, `Z = input_grid[r, c+4]`, `W = input_grid[r, c+5]`, handling out-of-bounds errors (treat out-of-bounds as non-matching for symmetry).
    7.  Evaluate the symmetric condition: Check if `C > 0`, `Y > 0`, `C == D`, `Y == Z`, and `X == W` (considering bounds).
    8.  If the symmetric condition is true: Modify the output grid by setting the pixels at `(r, c+1)` and `(r, c+2)` to the color `Y`.
    9.  If the symmetric condition is false: Check if the left flanking pixel `C` is non-white (`C > 0`). If it is, modify the output grid by setting the pixels at `(r, c+1)` and `(r, c+2)` to the color `C`.
    10. After checking all possible positions in all rows, return the modified output grid. (Note: Modifications should be based on the original input grid's context to avoid cascading effects within a single pass).
```python
import numpy as np

"""
The transformation identifies horizontally adjacent pairs of white pixels ('0 0') within each row of the input grid. 
For each '0 0' pair found at position (r, c+1) and (r, c+2), it examines the surrounding horizontal context.

1.  Symmetric Case: It checks for a symmetric pattern of the form 'X Y C 0 0 C Y X', where C and Y must be non-white colors. 
    - C is the pixel immediately to the left of the '0 0' pair (input_grid[r, c]).
    - Y is the pixel two positions to the left (input_grid[r, c-1]).
    - X is the pixel three positions to the left (input_grid[r, c-2]).
    - The symmetry requires the pixels to the right of '0 0' to mirror this: D=C (input_grid[r, c+3]), Z=Y (input_grid[r, c+4]), W=X (input_grid[r, c+5]).
    - Boundary conditions are considered: if any required context pixel (X, Y, Z, W) is out of bounds, it's not considered symmetric.
    - If the symmetric condition holds (C>0, Y>0, C==D, Y==Z, X==W), the '0 0' pair in the output grid is replaced with 'Y Y'.

2.  Asymmetric/Default Case: If the symmetric condition is not met, it checks if the pixel immediately to the left of the '0 0' pair (C = input_grid[r, c]) is non-white (C > 0).
    - If C > 0, the '0 0' pair in the output grid is replaced with 'C C'.

3.  No Change: If neither the symmetric condition is met nor the left flanking pixel C is non-white, the '0 0' pair remains unchanged.

The process iterates through all possible '0 0' pair locations in each row, applying the changes to a copy of the input grid based on the original input's context.
"""

def transform(input_grid):
    """
    Applies the described transformation rule to the input grid.
    """
    # Convert input list of lists to numpy array for easier slicing
    input_arr = np.array(input_grid, dtype=int)
    # Initialize the output grid as a copy of the input
    output_arr = np.copy(input_arr)
    height, width = input_arr.shape

    # Iterate through each row
    for r in range(height):
        # Iterate through columns, stopping early enough to check for the pattern 'C 0 0 D'
        # We need at least index c+3, so loop up to width - 4
        for c in range(width - 3):
            # Check for the '0 0' pattern
            if input_arr[r, c+1] == 0 and input_arr[r, c+2] == 0:
                # Identify immediate context C and D
                pixel_c = input_arr[r, c]
                pixel_d = input_arr[r, c+3]

                # Default fill values in case of asymmetry or failed conditions
                fill_val_1 = -1 # Use -1 to indicate no change initially
                fill_val_2 = -1

                # Attempt to identify extended context X, Y, Z, W, handling boundary checks
                pixel_y = input_arr[r, c-1] if c > 0 else None
                pixel_x = input_arr[r, c-2] if c > 1 else None
                pixel_z = input_arr[r, c+4] if c+4 < width else None
                pixel_w = input_arr[r, c+5] if c+5 < width else None

                # Check symmetric condition: X Y C 0 0 C Y X
                # Ensure all required context pixels exist (are not None) and C, Y are non-white
                is_symmetric = (
                    pixel_x is not None and
                    pixel_y is not None and
                    pixel_z is not None and
                    pixel_w is not None and
                    pixel_c > 0 and           # C must be non-white
                    pixel_y > 0 and           # Y must be non-white
                    pixel_c == pixel_d and    # C == D
                    pixel_y == pixel_z and    # Y == Z
                    pixel_x == pixel_w        # X == W
                )

                if is_symmetric:
                    # Symmetric case: fill with Y Y
                    fill_val_1 = pixel_y
                    fill_val_2 = pixel_y
                else:
                    # Asymmetric/Default case: check if C is non-white
                    if pixel_c > 0:
                        # Fill with C C
                        fill_val_1 = pixel_c
                        fill_val_2 = pixel_c

                # Apply the determined fill values if a change was decided (fill_val > -1)
                if fill_val_1 != -1:
                    output_arr[r, c+1] = fill_val_1
                if fill_val_2 != -1:
                     output_arr[r, c+2] = fill_val_2

    # Convert the result back to a list of lists
    return output_arr.tolist()

```
