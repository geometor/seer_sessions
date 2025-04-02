"""
Transforms the input grid by extending diagonal lines (down and to the right)
from each non-white pixel in the original input grid, with wrapping around the
grid boundaries. The line extension stops when it encounters a non-white pixel
in the evolving output grid.

1. Creates an output grid as a copy of the input grid.
2. Gets the height (H) and width (W) of the grid.
3. Iterates through each cell (row, col) of the *original* input grid.
4. If a cell in the original input grid contains a non-white color C:
    a. Initializes the path coordinates (r, c) to start one step down and right: (row + 1, col + 1).
    b. Enters a loop to trace the diagonal path:
        i. Calculates the wrapped coordinates (r_wrapped, c_wrapped) using the modulo operator: r_wrapped = r % H, c_wrapped = c % W.
        ii. Checks the color of the cell (r_wrapped, c_wrapped) in the *current* output grid.
        iii. If the cell (r_wrapped, c_wrapped) in the output grid is white (0):
            1. Colors the cell (r_wrapped, c_wrapped) in the output grid with color C.
            2. Advances the path coordinates: r = r + 1, c = c + 1.
            3. Continues the loop.
        iv. If the cell (r_wrapped, c_wrapped) in the output grid is *not* white:
            1. Stops tracing the path for the current source pixel. Breaks the loop.
5. Returns the modified output grid.
"""
import numpy as np

def transform(input_grid):
    """
    Applies the diagonal wrapping line transformation to the input grid.
    """
    # Convert input list of lists to a numpy array for efficient manipulation
    input_grid_np = np.array(input_grid, dtype=int)

    # Initialize output_grid as a copy of the input_grid numpy array
    output_grid = np.copy(input_grid_np)

    # Get the dimensions of the grid
    height, width = output_grid.shape

    # Iterate through each cell of the *original* input grid
    for row in range(height):
        for col in range(width):
            # Get the color of the current cell from the original input
            color = input_grid_np[row, col]

            # Check if the color is non-white (acts as a source)
            if color != 0:
                # Initialize the starting position for the diagonal trace
                # Start one step down and right from the source pixel
                r, c = row + 1, col + 1

                # Trace the diagonal line with wrapping
                while True:
                    # Calculate wrapped coordinates for the current trace position
                    r_wrapped = r % height
                    c_wrapped = c % width

                    # Check if the cell at the wrapped position in the output grid is currently white
                    if output_grid[r_wrapped, c_wrapped] == 0:
                        # If it's white, color it with the source pixel's color
                        output_grid[r_wrapped, c_wrapped] = color
                        # Move to the next diagonal position
                        r += 1
                        c += 1
                    else:
                        # If the cell is not white, the line is blocked, stop tracing for this source
                        break
                    
                    # Optional safety break: If a line wraps fully around and hits its start
                    # or continues indefinitely in a clear grid (unlikely given problem constraints,
                    # but good practice). A simpler check is if we've iterated H*W times.
                    # However, the non-white check should handle termination correctly.
                    # if (r - (row + 1)) >= height * width: # Avoid potential infinite loops
                    #    break

    # Convert the numpy array back to a list of lists before returning
    return output_grid.tolist()