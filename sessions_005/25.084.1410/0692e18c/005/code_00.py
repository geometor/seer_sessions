import numpy as np

"""
Transform an input grid into a larger output grid by scaling and tiling based on background patterns.

The output grid's dimensions are H*H rows and W*W columns, where H and W are the input grid's height and width. 
The transformation process involves creating a template based on the background pixels (color 0) of the input grid. This template is then colored by the non-background pixels of the input grid and tiled into the larger output grid.

1.  **Determine Output Size:** Calculate output dimensions `(H*H, W*W)`. Initialize an output grid of this size with the background color (white, 0).
2.  **Create Background Template:** Create a template grid `T` of size `H x W`. Set `T[r, c] = 1` if `input_grid[r, c] == 0` (background), otherwise set `T[r, c] = 0`. This template effectively marks the positions of the background pixels in the input grid.
3.  **Iterate and Populate:** Loop through each cell `(r, c)` of the `input_grid`.
    a.  **Get Paint Color:** Let `paint_color = input_grid[r, c]`.
    b.  **Check if Non-Background:** If `paint_color != 0`:
        i.  **Color the Template:** Create a `colored_subgrid` by taking the template `T`. Replace all 1s in `T` with `paint_color`. Pixels that were 0 in `T` (corresponding to non-background pixels in the input) remain 0 in the `colored_subgrid`.
        ii. **Calculate Position:** Determine the top-left corner `(start_row, start_col)` for placing the `colored_subgrid` in the output: `start_row = r * H`, `start_col = c * W`.
        iii. **Place Subgrid:** Copy the `colored_subgrid` into the `output_grid` at the calculated slice `output_grid[start_row : start_row + H, start_col : start_col + W]`.
4.  **Return Output:** Return the final `output_grid`. Cells in the output corresponding to background pixels in the input remain background (0) because their corresponding `paint_color` is 0, skipping the placement step.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by scaling it up and using a background-derived template,
    colored by the corresponding non-background pixel in the original input.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # 1. Determine Output Size
    # Get the dimensions of the input grid
    H, W = input_grid.shape

    # Calculate the dimensions of the output grid
    output_H = H * H
    output_W = W * W

    # Initialize the output grid with the background color (white, 0)
    output_grid = np.zeros((output_H, output_W), dtype=int)

    # 2. Create Background Template
    # Create a template where 1 marks the background pixels (value 0) in the input grid.
    # This uses boolean indexing: (input_grid == 0) creates a boolean array (True where 0, False otherwise).
    # .astype(int) converts True to 1 and False to 0.
    background_template = (input_grid == 0).astype(int) 

    # 3. Iterate and Populate
    # Iterate through each cell (pixel) of the input grid using its row (r) and column (c) index.
    for r in range(H):
        for c in range(W):
            # a. Get Paint Color
            # Get the color of the current pixel in the input grid.
            paint_color = input_grid[r, c]

            # b. Check if Non-Background
            # Only proceed if the current input pixel is not the background color (0).
            if paint_color != 0:
                # i. Color the Template
                # Create the subgrid to be placed in the output.
                # Use np.where: if the background_template at a position is 1 (meaning it was background in input),
                # set the corresponding pixel in colored_subgrid to paint_color.
                # Otherwise (if it was non-background in input), set it to 0.
                colored_subgrid = np.where(background_template == 1, paint_color, 0)

                # ii. Calculate Position
                # Calculate the top-left coordinates for placing this subgrid in the larger output grid.
                # The output grid is conceptually divided into HxW blocks, each of size HxW.
                start_row = r * H
                start_col = c * W
                
                # Calculate the bottom-right coordinates (exclusive) for the slice where the subgrid will be placed.
                end_row = start_row + H
                end_col = start_col + W
                
                # iii. Place Subgrid
                # Assign the newly created colored_subgrid to the appropriate slice in the output grid.
                output_grid[start_row:end_row, start_col:end_col] = colored_subgrid
                
            # If paint_color is 0, the corresponding block in the output_grid remains 0 (as initialized).

    # 4. Return Output
    # Return the completed output grid.
    return output_grid