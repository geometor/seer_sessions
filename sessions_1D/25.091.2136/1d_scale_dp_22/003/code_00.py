"""
Transforms a 2D grid by performing a sequential fill operation that stops at a 
specific boundary color (Azure, 8).

The transformation proceeds as follows:
1.  Iterates through the grid cells in row-major order (left-to-right, top-to-bottom).
2.  Maintains an 'active fill color', initialized to White (0).
3.  If a cell contains a color that is neither White (0) nor Azure (8), 
    the 'active fill color' is updated to this cell's color.
4.  If a cell contains White (0), its color is changed in the output grid to 
    the current 'active fill color'.
5.  This process continues until a cell containing Azure (8) is encountered.
6.  Once the Azure (8) boundary cell is found, the filling process stops. 
    All subsequent cells processed in the iteration order retain their 
    original colors from the input grid.
"""

import numpy as np

# Define color constants for clarity
WHITE = 0
AZURE = 8

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies a sequential fill transformation to a 2D grid, stopping at an 
    azure boundary.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed grid.
    """
    # Create a copy of the input grid to modify and return as the output
    output_grid = np.copy(input_grid)

    # Get grid dimensions
    height, width = input_grid.shape

    # Initialize the active fill color to white
    active_fill_color = WHITE
    # Initialize the boundary flag
    boundary_encountered = False

    # Iterate through the grid cells in row-major order
    for r in range(height):
        for c in range(width):
            # If the boundary has already been encountered, do nothing further for this cell
            # The output_grid already has the correct value from the initial copy
            if boundary_encountered:
                continue 

            # Get the color of the current cell from the original input grid
            current_color = input_grid[r, c]

            # Check for the boundary color (Azure 8)
            if current_color == AZURE:
                boundary_encountered = True
                # The azure pixel itself remains azure in the output (already copied)
                continue # Move to the next pixel

            # Check for a fill source color (not white, not azure)
            elif current_color != WHITE: # We already handled AZURE above
                # Update the active fill color
                active_fill_color = current_color
                # The source pixel itself remains its original color in the output (already copied)
                continue # Move to the next pixel

            # Check for a fill target color (White 0)
            elif current_color == WHITE:
                # Change the corresponding cell in the output grid to the active fill color
                output_grid[r, c] = active_fill_color
                # Continue to the next pixel (this continue is logically redundant but can stay for clarity)
                continue 
                
    # Return the modified grid
    return output_grid