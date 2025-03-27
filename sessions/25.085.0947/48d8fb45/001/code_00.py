import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on the following rules:
    1. Locate the single gray (5) pixel (anchor).
    2. Identify the unique color that is not white (0) or gray (5) (target_color).
    3. Create a 3x3 output grid filled with white (0).
    4. For each cell (out_r, out_c) in the output grid, calculate the corresponding
       source coordinates (src_r, src_c) in the input grid relative to the anchor:
       src_r = anchor_row + out_r + 1
       src_c = anchor_col + out_c - 1
    5. If the source coordinates are valid and the pixel at input_grid[src_r][src_c]
       matches the target_color, set output_grid[out_r][out_c] to the target_color.
    """

    # Convert input list of lists to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    input_rows, input_cols = grid.shape

    # 1. Locate the single gray (5) pixel (anchor)
    anchor_coords = np.where(grid == 5)
    if len(anchor_coords[0]) == 0:
        # Handle case where anchor is not found (though problem implies it exists)
        # For robustness, return an empty or default grid, or raise an error
        return np.zeros((3, 3), dtype=int).tolist() 
    anchor_row, anchor_col = anchor_coords[0][0], anchor_coords[1][0]

    # 2. Identify the unique color that is not white (0) or gray (5) (target_color)
    target_color = -1 # Initialize with an invalid value
    unique_colors = np.unique(grid)
    for color in unique_colors:
        if color != 0 and color != 5:
            target_color = color
            break
            
    if target_color == -1:
        # Handle case where target color is not found 
        # Return the empty output grid
         return np.zeros((3, 3), dtype=int).tolist() 

    # 3. Create a 3x3 output grid filled with white (0)
    output_grid = np.zeros((3, 3), dtype=int)

    # 4. Iterate through the output grid and map relative pixels
    for out_r in range(3):
        for out_c in range(3):
            # a. Calculate relative coordinates for source lookup
            # Output row 0 maps to relative row +1, output row 1 to +2, etc.
            rel_r = out_r + 1 
            # Output col 0 maps to relative col -1, output col 1 to 0, etc.
            rel_c = out_c - 1 

            # b. Calculate the corresponding source coordinates in the input grid
            src_r = anchor_row + rel_r
            src_c = anchor_col + rel_c

            # c. Check if the source coordinates are within the input grid boundaries
            if 0 <= src_r < input_rows and 0 <= src_c < input_cols:
                # d. Check if the pixel at the source coordinates matches the target color
                if grid[src_r, src_c] == target_color:
                    # e. If it matches, set the corresponding pixel in the output grid
                    output_grid[out_r, out_c] = target_color

    # 5. Return the final output_grid (converted back to list of lists)
    return output_grid.tolist()