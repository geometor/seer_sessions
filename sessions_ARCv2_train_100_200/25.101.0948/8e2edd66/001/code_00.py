"""
Transform a 3x3 input grid into a 9x9 output grid based on the following rules:

1. Identify the active color (C) in the input grid (the non-white color).
2. Create a 3x3 'inverse pattern' grid where white pixels in the input become the active color (C), and active color pixels in the input become white (0).
3. Create a 9x9 output grid, initialized to white (0).
4. Iterate through the 3x3 input grid. For each cell:
    a. If the input cell is white (0), copy the 3x3 'inverse pattern' into the corresponding 3x3 subgrid of the output grid.
    b. If the input cell contains the active color (C), leave the corresponding 3x3 subgrid in the output grid as white (0).
5. Return the resulting 9x9 output grid.
"""

import numpy as np

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rules to the input grid.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    input_rows, input_cols = input_np.shape

    # Ensure input is 3x3 as per observed pattern
    if input_rows != 3 or input_cols != 3:
        # Handle unexpected input size if necessary, maybe return input or raise error
        # For this specific task based on examples, we assume 3x3
        print("Warning: Input grid is not 3x3. Behavior might be undefined.")
        # Attempting to proceed, but results might be incorrect

    # 1. Identify the active color (C) - find the first non-zero value
    active_color = 0
    for r in range(input_rows):
        for c in range(input_cols):
            if input_np[r, c] != 0:
                active_color = input_np[r, c]
                break
        if active_color != 0:
            break

    # Handle case where input is all white (though not seen in examples)
    if active_color == 0:
        # Default behavior: return an all-white 9x9 grid
        return [[0]*9 for _ in range(9)]

    # 2. Create the 3x3 'inverse pattern' (InvP)
    inverse_pattern = np.zeros_like(input_np)
    for r in range(input_rows):
        for c in range(input_cols):
            if input_np[r, c] == 0:
                inverse_pattern[r, c] = active_color
            else: # input_np[r, c] == active_color
                inverse_pattern[r, c] = 0

    # 3. Create the 9x9 output grid (O) and initialize to white (0)
    output_rows, output_cols = input_rows * 3, input_cols * 3
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # 4. Iterate through the input grid and place the inverse pattern
    for r_sub in range(input_rows):
        for c_sub in range(input_cols):
            # 5. Check if the input cell is white (0)
            if input_np[r_sub, c_sub] == 0:
                # Calculate top-left coordinates for the subgrid in the output
                r_out = r_sub * 3
                c_out = c_sub * 3
                # Copy the inverse pattern into the output grid
                output_grid[r_out:r_out+3, c_out:c_out+3] = inverse_pattern
            # 6. If input cell is active color, do nothing (subgrid remains 0)

    # Convert the final numpy array back to a list of lists
    return output_grid.tolist()
