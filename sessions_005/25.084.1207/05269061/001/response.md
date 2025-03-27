```python
import numpy as np

"""
1.  Initialize an empty list `input_sequence` and an empty set `seen_colors`.
2.  Iterate through the `input_grid` row by row (from top to bottom), and within each row, column by column (from left to right).
3.  For each pixel value `color` at coordinates `(r, c)`:
    *   If `color` is not white (0) and `color` has not been seen before (is not in `seen_colors`):
        *   Add `color` to `seen_colors`.
        *   Append `color` to the `input_sequence`.
4.  Determine the number of unique non-white colors, `N = length(input_sequence)`.
5.  Find the minimum color value in the `input_sequence`, `min_color`.
6.  Calculate the left cyclic shift amount: `shift = (2 - min_color) % N`.
7.  Create the `output_pattern` by cyclically shifting the `input_sequence` to the left by `shift` positions.
8.  Get the dimensions (height `H` and width `W`) of the `input_grid`.
9.  Create a new `output_grid` with dimensions `H x W`.
10. Iterate through each cell `(r, c)` of the `output_grid` (from `r = 0` to `H-1`, `c = 0` to `W-1`).
11. Calculate the pattern index: `index = (r + c) % N`.
12. Set the value of the `output_grid` at `(r, c)` to the color found at `output_pattern[index]`.
13. Return the `output_grid`.
"""

def transform(input_grid):
    """
    Fills an output grid with a repeating color pattern derived from the unique non-white
    colors found in the input grid, ordered by their first appearance and cyclically shifted.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    H, W = input_grid_np.shape

    # 1. Initialize sequence and seen set
    input_sequence = []
    seen_colors = set()

    # 2. & 3. Iterate through input grid to find unique non-white colors in order
    for r in range(H):
        for c in range(W):
            color = input_grid_np[r, c]
            if color != 0 and color not in seen_colors:
                seen_colors.add(color)
                input_sequence.append(color)

    # 4. Determine the number of unique non-white colors (N)
    N = len(input_sequence)

    # Handle edge case: no non-white colors found
    if N == 0:
        # Return a grid of the same size filled with white (or handle as error if preferred)
        return np.zeros((H, W), dtype=int).tolist() 

    # 5. Find the minimum color value
    min_color = min(input_sequence)

    # 6. Calculate the left cyclic shift amount
    # Ensure the shift calculation handles negative results correctly with modulo N
    shift = (2 - min_color) % N 

    # 7. Create the output pattern by shifting the input sequence
    # Perform a left cyclic shift
    output_pattern = input_sequence[shift:] + input_sequence[:shift]

    # 8. Get input dimensions (already done H, W)
    
    # 9. Create a new output grid
    output_grid = np.zeros((H, W), dtype=int)

    # 10., 11., 12. Iterate through output grid cells and fill with pattern
    for r in range(H):
        for c in range(W):
            # Calculate the pattern index based on row and column sum
            index = (r + c) % N
            # Set the output grid cell value
            output_grid[r, c] = output_pattern[index]

    # 13. Return the output grid as a list of lists
    return output_grid.tolist()

```