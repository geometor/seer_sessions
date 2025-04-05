import copy
import numpy as np

"""
The transformation rule operates on a 2D grid containing 0s and 5s.
1. Copy the input grid to create the output grid.
2. Iterate through each cell of the input grid.
3. If a cell contains the value 5:
    a. Identify its four diagonal neighbor cells (Top-Left, Top-Right, Bottom-Left, Bottom-Right).
    b. For each diagonal neighbor that exists within the grid boundaries:
        i. Update the corresponding cell in the output grid with a specific value based on the relative position:
            - Top-Left neighbor becomes 6.
            - Top-Right neighbor becomes 9.
            - Bottom-Left neighbor becomes 7.
            - Bottom-Right neighbor becomes 3.
4. The original positions of the 5s remain unchanged in the output grid. Cells that are not 5s and are not updated diagonal neighbors also remain unchanged (initially 0s).
"""

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list of lists representing the input 2D grid.

    Returns:
        A list of lists representing the transformed output 2D grid.
    """
    # Convert input list of lists to a NumPy array for easier manipulation
    input_arr = np.array(input_grid, dtype=int)
    # Initialize the output grid as a copy of the input grid
    output_arr = np.copy(input_arr)
    height, width = input_arr.shape

    # Iterate through each cell of the input grid
    for r in range(height):
        for c in range(width):
            # Check if the current cell contains a 5
            if input_arr[r, c] == 5:
                # Define the relative coordinates and corresponding values for diagonal neighbors
                # (dr, dc), value
                neighbors = [
                    ((-1, -1), 6),  # Top-Left
                    ((-1,  1), 9),  # Top-Right
                    (( 1, -1), 7),  # Bottom-Left
                    (( 1,  1), 3)   # Bottom-Right
                ]

                # Process each potential diagonal neighbor
                for (dr, dc), value in neighbors:
                    nr, nc = r + dr, c + dc

                    # Check if the neighbor coordinates are within the grid boundaries
                    if 0 <= nr < height and 0 <= nc < width:
                        # Update the corresponding cell in the output grid
                        # Note: This will overwrite any existing 0 or previously placed number
                        # (except the original 5s, as they are not diagonal neighbors of themselves)
                        output_arr[nr, nc] = value

    # Convert the NumPy array back to a list of lists for the return value
    output_grid = output_arr.tolist()
    return output_grid
