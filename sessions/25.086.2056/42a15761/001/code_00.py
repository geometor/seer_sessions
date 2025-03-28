import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on a local neighborhood rule.

    1. Create a new grid (output grid) identical to the input grid.
    2. Iterate through each pixel of the input grid, examining its row `r` and column `c`, focusing on pixels that could potentially change based on neighbor availability. Specifically, iterate through rows `r` from 0 up to (but not including) the last row, and columns `c` from 1 up to (but not including) the last column.
    3. For each considered pixel at `(r, c)` in the input grid:
        a. Check if the pixel's color is white (0).
        b. If it is white, then check the colors of its immediate neighbors:
            i. The pixel to the left at `(r, c-1)`.
            ii. The pixel to the right at `(r, c+1)`.
            iii. The pixel below at `(r+1, c)`.
        c. If the pixel at `(r, c)` is white AND the left neighbor is red (2) AND the right neighbor is red (2) AND the bottom neighbor is red (2), then change the color of the pixel at `(r, c)` in the *output grid* to red (2).
    4. After checking all applicable pixels, return the completed output grid.
    """

    # Convert input list of lists to numpy array for easier indexing
    input_array = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input_grid
    output_array = np.copy(input_array)
    
    # Get the dimensions of the grid
    height, width = input_array.shape
    
    # Iterate through the pixels, excluding borders where neighbors might not exist
    # Rows: 0 to height-2 (to allow checking row r+1)
    # Columns: 1 to width-2 (to allow checking cols c-1 and c+1)
    for r in range(height - 1):
        for c in range(1, width - 1):
            # Check if the current pixel is white (0)
            if input_array[r, c] == 0:
                # Check the color of the left, right, and bottom neighbors
                left_neighbor = input_array[r, c - 1]
                right_neighbor = input_array[r, c + 1]
                bottom_neighbor = input_array[r + 1, c]
                
                # If all three neighbors are red (2)
                if left_neighbor == 2 and right_neighbor == 2 and bottom_neighbor == 2:
                    # Change the corresponding pixel in the output grid to red (2)
                    output_array[r, c] = 2
                    
    # Convert the numpy array back to a list of lists for the final output
    output_grid = output_array.tolist()

    return output_grid