import numpy as np

"""
Identify all non-white pixels in the input grid. For each non-white pixel, 
project a diagonal line downwards and to the right, using the same color as 
the starting pixel. This line continues until it hits the grid boundary or 
reaches a cell that was non-white in the *original* input grid. The line stops 
*before* overwriting any original non-white pixel. The final output grid 
contains both the original non-white pixels and the newly drawn diagonal lines.
"""

def transform(input_grid):
    """
    Projects diagonal lines from non-white pixels in the input grid.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # Iterate through each cell of the input grid
    for r in range(height):
        for c in range(width):
            # Check if the current cell is non-white (not 0)
            if input_grid[r, c] != 0:
                # Get the color of the source pixel
                color = input_grid[r, c]
                
                # Initialize the starting position for the diagonal trace
                nr, nc = r + 1, c + 1

                # Start tracing the diagonal line downwards and to the right
                while nr < height and nc < width:
                    # Check if the next cell in the diagonal path *in the original input grid* is white
                    if input_grid[nr, nc] == 0:
                        # If it's white, draw the pixel with the source color in the output grid
                        output_grid[nr, nc] = color
                        # Move to the next diagonal position
                        nr += 1
                        nc += 1
                    else:
                        # If the next cell in the input grid is not white, stop tracing this line
                        break 
                # The loop also naturally stops if nr or nc go out of bounds

    # Return the modified output grid
    return output_grid
