import numpy as np

"""
Generates an output grid by streaking non-background pixels from the input grid diagonally downwards and to the right.

The transformation rule involves the following steps:
1. Determine the input grid dimensions (H, W).
2. Calculate the output grid dimensions (H' = H + 3, W' = W + 3).
3. Create an output grid of size H' x W', initialized with the background color (0).
4. Iterate through each pixel (r, c) in the input grid.
5. If the input pixel color C at (r, c) is not the background color (0):
   a. Starting from the corresponding position (r, c) in the output grid, set the pixel color to C.
   b. Continue setting pixels diagonally downwards and to the right (r+1, c+1), (r+2, c+2), ... with color C, until the coordinates go out of the output grid bounds (H', W').
6. Return the final output grid.
"""

def transform(input_grid):
    """
    Applies the diagonal streaking transformation to the input grid.

    Args:
        input_grid (list of lists or np.ndarray): The input grid.

    Returns:
        np.ndarray: The transformed output grid.
    """
    # Convert input to numpy array for easier handling
    input_array = np.array(input_grid, dtype=int)
    
    # 1. Determine input grid dimensions
    input_height, input_width = input_array.shape

    # 2. Calculate output grid dimensions
    output_height = input_height + 3
    output_width = input_width + 3

    # 3. Create an output grid initialized with background color (0)
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # 4. Iterate through each cell of the input grid
    for r in range(input_height):
        for c in range(input_width):
            # 5. Get the color of the input cell
            color = input_array[r, c]

            # 6. If the color is not the background color (0)
            if color != 0:
                # a. Initialize current row and column for the streak in the output grid
                dr = r
                dc = c

                # b. Start the loop to create the diagonal streak
                while dr < output_height and dc < output_width:
                    # c. Set the color of the output grid cell
                    output_grid[dr, dc] = color
                    
                    # d. Increment row index
                    dr += 1
                    # e. Increment column index
                    dc += 1

    # 7. Return the completed output grid
    return output_grid.tolist() # Convert back to list of lists if required by the environment