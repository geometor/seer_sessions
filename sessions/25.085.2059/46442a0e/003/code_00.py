import numpy as np

"""
The transformation takes an input grid of size HxW and produces an output grid of size 2Hx2W.
The output grid is composed of four quadrants, each of size HxW.
Each quadrant contains a transformed version of the input grid:
1. Top-Left (TL): The original input grid (identity).
2. Top-Right (TR): The input grid rotated 90 degrees clockwise.
3. Bottom-Left (BL): The input grid reflected across its anti-diagonal (transposed and then flipped vertically).
4. Bottom-Right (BR): The input grid rotated 180 degrees (flipped horizontally and vertically).
"""

def transform(input_grid):
    """
    Transforms the input grid by creating a 2x2 arrangement of transformed versions.

    Args:
        input_grid (list[list[int]]): The input grid.

    Returns:
        list[list[int]]: The transformed output grid.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    H, W = input_np.shape

    # Initialize the output grid with dimensions 2H x 2W
    # The background color doesn't matter as all cells will be overwritten.
    output_grid = np.zeros((2 * H, 2 * W), dtype=int)

    # Calculate the four transformed versions of the input grid
    # 1. Identity (original input)
    transform_TL = input_np

    # 2. Rotate 90 degrees clockwise
    # k=-1 or k=3 rotates clockwise
    transform_TR = np.rot90(input_np, k=-1)

    # 3. Anti-diagonal reflection (transpose then flip vertically)
    # Transpose swaps rows and columns.
    # Flip vertically (up-down) flips along the horizontal axis.
    transform_BL = np.flipud(input_np.T) 

    # 4. Rotate 180 degrees
    # k=2 performs two 90-degree counter-clockwise rotations.
    transform_BR = np.rot90(input_np, k=2)

    # Place the transformed grids into the corresponding quadrants of the output grid
    # Top-Left quadrant (rows 0 to H-1, cols 0 to W-1)
    output_grid[0:H, 0:W] = transform_TL

    # Top-Right quadrant (rows 0 to H-1, cols W to 2*W-1)
    output_grid[0:H, W:2*W] = transform_TR

    # Bottom-Left quadrant (rows H to 2*H-1, cols 0 to W-1)
    output_grid[H:2*H, 0:W] = transform_BL

    # Bottom-Right quadrant (rows H to 2*H-1, cols W to 2*W-1)
    output_grid[H:2*H, W:2*W] = transform_BR

    # Convert the final numpy array back to a list of lists
    return output_grid.tolist()