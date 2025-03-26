"""
Transformation Rule:
1. Determine the dimensions of the input grid (H, W).
2. Create an output grid with dimensions (2*H, 2*W), initialized with the background color (white, 0).
3. Iterate through each cell (r, c) of the input grid.
4. If the input cell contains a non-background color C:
   a. Propagate this color C diagonally down and to the right in the output grid, starting from the corresponding position (r, c).
   b. For each step k (starting from 0), set the output cell at (r + k, c + k) to color C, as long as the coordinates (r + k, c + k) remain within the bounds of the output grid.
5. Return the final output grid.
"""
import numpy as np

def transform(input_grid):
    """
    Applies the diagonal propagation transformation to the input grid.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # 1. Determine the dimensions of the input grid (H, W).
    input_height, input_width = input_grid.shape

    # 2. Calculate output dimensions and initialize output grid with background color (0).
    output_height = input_height * 2
    output_width = input_width * 2
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # 3. Iterate through each cell (r, c) of the input grid.
    for r in range(input_height):
        for c in range(input_width):
            # 4. Identify the color C at the current input cell.
            color = input_grid[r, c]

            # 5. If the color C is not the background color (0):
            if color != 0:
                # a. Propagate this color C diagonally down and to the right.
                k = 0
                while True:
                    # b. Calculate target coordinates.
                    target_r = r + k
                    target_c = c + k

                    # c. Check if target coordinates are within output grid bounds.
                    if target_r < output_height and target_c < output_width:
                        # i. Set output grid cell to color C.
                        output_grid[target_r, target_c] = color
                    else:
                        # ii. Stop propagation if out of bounds.
                        break
                    
                    # d. Increment k for the next diagonal step.
                    k += 1

    # 6. Return the final output grid.
    return output_grid