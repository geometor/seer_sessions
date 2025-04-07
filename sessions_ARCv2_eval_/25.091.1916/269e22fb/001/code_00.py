import numpy as np

"""
Tiles the input grid pattern onto a fixed 20x20 output grid.
The tiling involves repeating the input pattern across and down the output grid.
Horizontal repetitions alternate between the original pattern and a horizontally flipped version.
Vertical repetitions alternate between the current horizontal row pattern (original or flipped) 
and a vertically flipped version of that row pattern.

Specifically:
1. Determine the height (H) and width (W) of the input grid.
2. Create a new 20x20 output grid.
3. For each cell (row, col) in the 20x20 output grid:
    a. Find the effective row and column within the input pattern: 
       eff_row = row % H
       eff_col = col % W
    b. Determine if the pattern tile at this location needs horizontal flipping:
       needs_h_flip = (col // W) % 2 == 1
    c. Determine if the pattern tile at this location needs vertical flipping:
       needs_v_flip = (row // H) % 2 == 1
    d. Calculate the source row index in the input grid, applying vertical flip if needed:
       input_row = (H - 1 - eff_row) if needs_v_flip else eff_row
    e. Calculate the source column index in the input grid, applying horizontal flip if needed:
       input_col = (W - 1 - eff_col) if needs_h_flip else eff_col
    f. Set the output cell value: output_grid[row, col] = input_grid[input_row, input_col]
4. Return the populated 20x20 output grid.
"""

def transform(input_grid):
    """
    Transforms the input grid by tiling it onto a 20x20 grid with alternating flips.
    """
    # Convert input list of lists to a numpy array for easier handling
    input_np = np.array(input_grid, dtype=int)
    
    # Determine the height (H) and width (W) of the input grid
    H, W = input_np.shape
    
    # Define the dimensions of the output grid
    output_height = 20
    output_width = 20
    
    # Initialize the output grid (e.g., with zeros)
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through each cell of the output grid
    for row in range(output_height):
        for col in range(output_width):
            # Calculate effective row and column within the input pattern dimensions
            eff_row = row % H
            eff_col = col % W
            
            # Determine if horizontal flip is needed based on the tile column index
            needs_h_flip = (col // W) % 2 == 1
            
            # Determine if vertical flip is needed based on the tile row index
            needs_v_flip = (row // H) % 2 == 1
            
            # Calculate the source row index from the input grid, applying vertical flip if needed
            input_row = (H - 1 - eff_row) if needs_v_flip else eff_row
            
            # Calculate the source column index from the input grid, applying horizontal flip if needed
            input_col = (W - 1 - eff_col) if needs_h_flip else eff_col
            
            # Assign the value from the calculated input cell to the output cell
            output_grid[row, col] = input_np[input_row, input_col]

    # Convert the numpy array back to a list of lists for the expected output format
    return output_grid.tolist()