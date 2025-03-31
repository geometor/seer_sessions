import numpy as np

"""
1. Determine the height (H) and width (W) of the input grid.
2. Create a new output grid with height 2H and width 2W.
3. Initialize all cells of the new output grid with the background color (white/0).
4. Copy the content of the input grid into the top-left quadrant of the output grid (rows 0 to H-1, columns 0 to W-1).
5. Copy the content of the input grid again into the bottom-right quadrant of the output grid (rows H to 2H-1, columns W to 2W-1).
6. Return the completed output grid.
"""

def transform(input_grid):
    """
    Creates an output grid double the dimensions of the input grid,
    placing two copies of the input grid diagonally (top-left and bottom-right)
    and filling the remaining quadrants with the background color (0).
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)

    # 1. Determine the height (H) and width (W) of the input grid.
    H, W = input_np.shape

    # 2. Create a new output grid with height 2H and width 2W.
    output_height = 2 * H
    output_width = 2 * W

    # 3. Initialize all cells of the new output grid with the background color (white/0).
    # Assuming background color is 0 based on examples.
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # 4. Copy the content of the input grid into the top-left quadrant.
    output_grid[0:H, 0:W] = input_np

    # 5. Copy the content of the input grid again into the bottom-right quadrant.
    output_grid[H:output_height, W:output_width] = input_np

    # 6. Return the completed output grid (implicitly converted back to list of lists if needed by caller).
    return output_grid.tolist()