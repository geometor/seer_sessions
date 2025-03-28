"""
Moves a single green pixel (3) one step towards a single yellow pixel (4) in a grid.

The transformation rule is as follows:
1. Locate the coordinates of the green pixel (3) and the yellow pixel (4).
2. Calculate the difference in rows (dR) and columns (dC) between the yellow and green pixels (Yellow - Green).
3. Determine the movement direction: 
   - Vertical step (moveR): +1 if dR > 0, -1 if dR < 0, 0 if dR = 0.
   - Horizontal step (moveC): +1 if dC > 0, -1 if dC < 0, 0 if dC = 0.
4. Calculate the new coordinates for the green pixel by adding the movement steps (moveR, moveC) to its original coordinates.
5. Create the output grid by copying the input grid.
6. Update the output grid: set the original green pixel location to white (0) and the new calculated location to green (3). The yellow pixel's position remains unchanged.
"""

import numpy as np

def find_pixel_coords(grid, color):
    """Finds the coordinates (row, col) of the first pixel with the given color."""
    coords = np.argwhere(grid == color)
    if len(coords) > 0:
        return coords[0]  # Return the first instance (row, col)
    return None

def transform(input_grid):
    """
    Moves the green pixel one step towards the yellow pixel.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed grid.
    """
    # Convert input list of lists to numpy array if necessary
    grid = np.array(input_grid)

    # Initialize output_grid as a copy of the input grid
    output_grid = grid.copy()

    # Find the coordinates of the green (3) and yellow (4) pixels
    green_coords = find_pixel_coords(grid, 3)
    yellow_coords = find_pixel_coords(grid, 4)

    # If either pixel is not found, return the original grid (or handle error)
    if green_coords is None or yellow_coords is None:
        print("Warning: Green or Yellow pixel not found.")
        return output_grid

    Gr, Gc = green_coords
    Yr, Yc = yellow_coords

    # Calculate the difference in rows and columns
    dR = Yr - Gr
    dC = Yc - Gc

    # Determine the movement step using np.sign which returns -1, 0, or 1
    moveR = int(np.sign(dR))
    moveC = int(np.sign(dC))

    # Calculate the new coordinates for the green pixel
    newGr = Gr + moveR
    newGc = Gc + moveC

    # Check if the new coordinates are valid (within grid bounds)
    # Although based on the examples, this might not be strictly necessary
    # as the green pixel never reaches the yellow one in a single step.
    height, width = grid.shape
    if 0 <= newGr < height and 0 <= newGc < width:
        # Change the original green pixel position to white (0) in the output grid
        output_grid[Gr, Gc] = 0
        # Place the green pixel (3) at the new coordinates in the output grid
        output_grid[newGr, newGc] = 3
    else:
        # Handle edge case if needed, though not observed in examples
        print(f"Warning: Calculated new green coordinates ({newGr}, {newGc}) are out of bounds.")
        # In this case, maybe the green pixel stays put? Return unmodified output_grid.
        # Based on provided examples, this scenario doesn't occur.

    return output_grid.tolist() # Convert back to list of lists if required by the environment