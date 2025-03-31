import numpy as np

"""
1. Receive the input grid. Determine its height (H) and width (W).
2. Create a new intermediate grid, `base_tile`, of the same dimensions (H x W).
3. Find all rows in the input grid that contain at least one non-white pixel. Store their indices.
4. Find all columns in the input grid that contain at least one non-white pixel. Store their indices.
5. Iterate through each cell of the input grid at row `r` and column `c`:
    a. Get the `input_color`.
    b. If `input_color` is non-white (not 0), copy it to `base_tile[r, c]`.
    c. If `input_color` is white (0):
        i. Check if row `r` OR column `c` contains a non-white pixel (using the stored indices).
        ii. If true, set `base_tile[r, c]` to azure (8).
        iii. If false, set `base_tile[r, c]` to white (0).
6. Create the final output grid with dimensions (2*H) x (2*W).
7. Place copies of the `base_tile` into the four quadrants of the output grid.
8. Return the completed output grid.
"""

def transform(input_grid):
    """
    Transforms the input grid by first creating a 'base_tile' where white pixels 
    are changed to azure (8) if their row or column in the original input contained 
    any non-white pixel. Non-white pixels are preserved. This base_tile is then 
    tiled 2x2 to form the output grid.
    """
    
    # Convert input to numpy array for easier processing
    input_np = np.array(input_grid, dtype=int)
    
    # 1. Determine input grid dimensions
    H, W = input_np.shape
    
    # 2. Create the base_tile grid, initialized with zeros (white)
    base_tile = np.zeros_like(input_np)
    
    # 3. Find rows containing non-white pixels
    rows_with_non_white = set(r for r in range(H) if np.any(input_np[r, :] != 0))
    
    # 4. Find columns containing non-white pixels
    cols_with_non_white = set(c for c in range(W) if np.any(input_np[:, c] != 0))
    
    # 5. Iterate through each cell to populate the base_tile
    for r in range(H):
        for c in range(W):
            input_color = input_np[r, c]
            
            # 5b. If input color is non-white, copy it
            if input_color != 0:
                base_tile[r, c] = input_color
            # 5c. If input color is white
            else:
                # 5c.i. Check if row or column had non-white pixels
                if r in rows_with_non_white or c in cols_with_non_white:
                    # 5c.ii. Set to azure (8)
                    base_tile[r, c] = 8
                else:
                    # 5c.iii. Keep as white (0) - already initialized to 0
                    pass # base_tile[r, c] remains 0

    # 6. Create the final output grid with doubled dimensions
    output_H, output_W = 2 * H, 2 * W
    output_grid_np = np.zeros((output_H, output_W), dtype=int)
    
    # 7. Tile the base_tile into the output grid quadrants
    output_grid_np[0:H, 0:W] = base_tile       # Top-left
    output_grid_np[0:H, W:output_W] = base_tile # Top-right
    output_grid_np[H:output_H, 0:W] = base_tile # Bottom-left
    output_grid_np[H:output_H, W:output_W] = base_tile # Bottom-right

    # 8. Return the completed output grid (convert back to list of lists if necessary)
    return output_grid_np.tolist()
