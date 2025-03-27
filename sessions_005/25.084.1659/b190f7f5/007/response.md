```python
import numpy as np

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Upscales each pixel of the input grid into a larger S x S block in the output grid, 
    where S is the height of the input grid. The pattern applied within each block 
    depends on the original pixel's color.

    Transformation Steps:
    1. Determine the scaling factor S (input grid height).
    2. Calculate output grid dimensions (input_height * S, input_width * S).
    3. Initialize the output grid with white (0).
    4. For each input pixel (r, c) with color inp_color:
        a. Determine the pattern_color: white (0) if inp_color is azure (8), otherwise inp_color.
        b. Calculate the top-left (R, C) of the corresponding S x S block in the output grid.
        c. Calculate the center index center_idx = S // 2.
        d. Draw a horizontal line of pattern_color at row R + center_idx within the block.
        e. Draw a vertical line of pattern_color at column C + center_idx within the block.
        (This forms a plus-sign shape if pattern_color is not white).
    5. Return the resulting output grid.
    """
    # 1. Determine scaling factor S and input dimensions
    input_height, input_width = input_grid.shape
    scaling_factor_S = input_height

    # 2. Calculate output grid dimensions
    output_height = input_height * scaling_factor_S
    output_width = input_width * scaling_factor_S

    # 3. Initialize the output grid with white (0)
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # 4. Iterate through each pixel of the input grid
    center_idx = scaling_factor_S // 2  # Calculate center index once

    for r in range(input_height):
        for c in range(input_width):
            # a. Get input color
            inp_color = input_grid[r, c]

            # b. Determine pattern_color
            if inp_color == 8: # Azure
                pattern_color = 0 # White
            else:
                pattern_color = inp_color

            # Skip drawing if pattern color is white (already initialized)
            if pattern_color == 0:
                continue

            # c. Calculate top-left coordinates (R, C) for the output block
            R = r * scaling_factor_S
            C = c * scaling_factor_S

            # d. Draw horizontal line
            # Ensure row index is within bounds (should always be)
            row_idx = R + center_idx
            if 0 <= row_idx < output_height:
                 output_grid[row_idx, C : C + scaling_factor_S] = pattern_color

            # e. Draw vertical line
            # Ensure column index is within bounds (should always be)
            col_idx = C + center_idx
            if 0 <= col_idx < output_width:
                output_grid[R : R + scaling_factor_S, col_idx] = pattern_color

    # 5. Return the completed output grid
    return output_grid
```