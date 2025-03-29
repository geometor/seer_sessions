```python
import numpy as np

"""
Transform an input grid (S x S) into an output grid ((S*S) x (S*S)).
The output grid is composed of S x S subgrids, each of size S x S.
Each subgrid corresponds to a cell (r, c) in the input grid.
The content of the subgrid located at row-block r and column-block c
is a copy of the original input grid, but filtered: only the pixels
matching the value of the input grid cell at (r, c) are kept, 
while all other pixels are set to white (0).
"""

def transform(input_grid):
    """
    Tiles the output grid with filtered versions of the input grid based on each input cell's value.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Convert input list of lists to numpy array for easier handling
    input_grid = np.array(input_grid)
    
    # Determine the size (S) of the input grid (assuming square)
    S = input_grid.shape[0]
    if input_grid.shape[0] != input_grid.shape[1]:
        # Handle non-square inputs if necessary, though examples are square
        # For now, we'll assume square as per the examples
        print("Warning: Input grid is not square.")
        # Or raise an error: raise ValueError("Input grid must be square")

    # Calculate the dimensions of the output grid
    output_height = S * S
    output_width = S * S

    # Initialize the output grid with the background color (white = 0)
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through each cell (r, c) of the input grid
    # This cell determines the filter value and the position of the subgrid
    for r in range(S):
        for c in range(S):
            # Get the filter value V from the current input cell
            filter_value = input_grid[r, c]

            # Calculate the top-left coordinates (R_start, C_start) for the subgrid in the output
            R_start = r * S
            C_start = c * S

            # Iterate through the input grid again (ir, ic) to generate the content for the current subgrid
            for ir in range(S):
                for ic in range(S):
                    # Get the value from the original input grid at this position
                    input_value = input_grid[ir, ic]

                    # Determine the value to place in the output subgrid
                    # If the input_value matches the filter_value, use filter_value, otherwise use background color 0
                    output_pixel_value = filter_value if input_value == filter_value else 0
                    
                    # Calculate the absolute coordinates in the output grid
                    output_r = R_start + ir
                    output_c = C_start + ic
                    
                    # Place the calculated pixel value into the output grid
                    output_grid[output_r, output_c] = output_pixel_value

    return output_grid.tolist() # Return as list of lists if required by the environment
```