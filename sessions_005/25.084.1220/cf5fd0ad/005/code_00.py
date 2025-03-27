"""
Transforms a 3x3 input grid into a 12x12 output grid by tiling it 
in a 4x4 pattern. Each tile in the 4x4 pattern is a geometrically 
transformed version of the input grid based on its quadrant location:
- Top-left quadrant (tiles 0,0 to 1,1): Input rotated 180 degrees.
- Top-right quadrant (tiles 0,2 to 1,3): Input rotated 90 degrees clockwise.
- Bottom-left quadrant (tiles 2,0 to 3,1): Input rotated 90 degrees counter-clockwise. # Corrected
- Bottom-right quadrant (tiles 2,2 to 3,3): Input used as is (identity).
"""

import numpy as np

def transform(input_grid):
    """
    Applies geometric transformations to a 3x3 input grid and tiles the results
    into a 12x12 output grid based on quadrant location.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    input_h, input_w = input_np.shape # Should be 3x3 based on examples

    # Calculate output dimensions (4x input dimensions)
    output_h = input_h * 4
    output_w = input_w * 4

    # Initialize the output grid as a numpy array (filled with zeros initially)
    output_grid_np = np.zeros((output_h, output_w), dtype=int)

    # --- Pre-calculate transformed versions of the input grid ---

    # Rotate 180 degrees (rotate 90 degrees twice)
    input_rot180 = np.rot90(input_np, k=2) 
    
    # Rotate 90 degrees clockwise (equivalent to k=-1 or k=3 for rot90)
    input_rot90_cw = np.rot90(input_np, k=-1) 
    
    # Rotate 90 degrees counter-clockwise (equivalent to k=1 for rot90) # Corrected
    input_rot90_ccw = np.rot90(input_np, k=1) 
    
    # Identity (original input) - already have input_np

    # --- Tile the output grid with transformed inputs ---

    # Iterate through the 4x4 grid of tiles
    for tr in range(4):  # tile row index
        for tc in range(4):  # tile column index

            # Determine the starting row and column in the output grid for the current tile
            r_start = tr * input_h
            c_start = tc * input_w
            
            # Select the appropriate transformed input based on the tile's quadrant
            if tr < 2 and tc < 2:  # Top-left quadrant (rows 0-1, cols 0-1)
                tile_to_place = input_rot180
            elif tr < 2 and tc >= 2: # Top-right quadrant (rows 0-1, cols 2-3)
                tile_to_place = input_rot90_cw 
            elif tr >= 2 and tc < 2: # Bottom-left quadrant (rows 2-3, cols 0-1)
                tile_to_place = input_rot90_ccw # Corrected transformation
            else: # Bottom-right quadrant (rows 2-3, cols 2-3)
                tile_to_place = input_np # Identity

            # Place the selected tile into the corresponding block in the output grid
            output_grid_np[r_start : r_start + input_h, c_start : c_start + input_w] = tile_to_place

    # Convert the final numpy array back to a list of lists for the required output format
    output_grid = output_grid_np.tolist()

    return output_grid