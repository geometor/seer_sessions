import numpy as np

def transform(input_grid):
    """
    Transforms an input grid based on the following rules:

    1. Define the input grid `I` with height `H` and width `W`.
    2. Create a new output grid `O` with height `3 * H` and width `3 * W`, initializing all its pixels to `white` (0).
    3. Iterate through each row `r` (from 0 to `H-1`) and each column `c` (from 0 to `W-1`) of the input grid `I`.
    4. If the pixel `I[r, c]` has the color `red` (2):
        a. Calculate the target top-left coordinates in the output grid: `target_row = r * H`, `target_col = c * W`.
        b. Copy the entire input grid `I` into the output grid `O`, starting at the position `(target_row, target_col)`. This means for every `i` from 0 to `H-1` and `j` from 0 to `W-1`, set `O[target_row + i, target_col + j] = I[i, j]`.
    5. Return the final output grid `O`.
    """

    # Convert input list of lists to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Get input grid dimensions (Height H, Width W)
    H, W = input_np.shape
    
    # Define output grid dimensions (3*H, 3*W)
    output_H = H * 3
    output_W = W * 3
    
    # Initialize output grid with background color white (0)
    output_grid = np.zeros((output_H, output_W), dtype=int)
    
    # Define color constants
    RED = 2
    # WHITE = 0 # Background color, used in initialization

    # Iterate through each cell (r, c) of the input grid
    for r in range(H):
        for c in range(W):
            # Check if the input pixel color is red (2)
            if input_np[r, c] == RED:
                # Calculate the top-left coordinates for the target slot in the output grid
                # The row index 'r' determines the row-block, scaled by input height H
                # The column index 'c' determines the column-block, scaled by input width W
                start_row = r * H
                start_col = c * W
                
                # Define the boundaries for the copy operation in the output grid
                end_row = start_row + H
                end_col = start_col + W
                
                # Copy the entire input grid into the calculated slot using numpy slicing
                # output_grid[start_row:end_row, start_col:end_col] receives the values from input_np
                output_grid[start_row : end_row, start_col : end_col] = input_np

    # Convert the numpy array back to a list of lists for the expected output format
    return output_grid.tolist()