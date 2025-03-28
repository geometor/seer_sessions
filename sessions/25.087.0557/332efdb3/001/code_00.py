import numpy as np

"""
Transforms an input grid (which is always all white) into an output grid of the same dimensions.
The output grid follows a specific pattern:
1. Rows with an even index (0, 2, 4, ...) are filled entirely with blue pixels (1).
2. Rows with an odd index (1, 3, 5, ...) alternate between blue (1) and white (0) pixels, starting with blue (1) in the first column (index 0).
"""

def transform(input_grid):
    """
    Generates a patterned grid based on the input grid's dimensions.

    Args:
        input_grid (list of lists or np.ndarray): A grid, expected to be all white (0).

    Returns:
        np.ndarray: A new grid with the specified blue/white pattern.
    """
    # Convert input to numpy array for easier handling
    input_array = np.array(input_grid, dtype=int)
    
    # Determine the height and width from the input grid
    height, width = input_array.shape
    
    # Initialize the output grid with zeros (white) - though it will be overwritten
    output_grid = np.zeros((height, width), dtype=int)

    # Iterate through each pixel location (row, col)
    for r in range(height):
        for c in range(width):
            # Check if the row index is even
            if r % 2 == 0:
                # If row is even, set the pixel to blue (1)
                output_grid[r, c] = 1
            else:
                # If row is odd, check if the column index is even
                if c % 2 == 0:
                    # If column is even, set the pixel to blue (1)
                    output_grid[r, c] = 1
                else:
                    # If column is odd, set the pixel to white (0)
                    # Note: This is already the default if initialized with zeros,
                    # but explicitly setting it can be clearer.
                    output_grid[r, c] = 0 
                    
    return output_grid.tolist() # Return as list of lists per ARC standard