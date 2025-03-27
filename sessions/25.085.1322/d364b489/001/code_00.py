"""
Transforms the input grid by coloring the orthogonal neighbors of blue (1) pixels.
- Pixels above blue become red (2).
- Pixels below blue become azure (8).
- Pixels left of blue become orange (7).
- Pixels right of blue become magenta (6).
The original blue pixels remain. Coloring only occurs within grid boundaries.
"""

import numpy as np

# Define color constants for clarity
BLUE = 1
RED = 2
AZURE = 8
ORANGE = 7
MAGENTA = 6

def transform(input_grid):
    """
    Applies a coloring rule based on the position of blue pixels.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input list of lists to a numpy array for efficient manipulation
    input_np = np.array(input_grid, dtype=int)
    # Create the output grid initially as a copy of the input grid
    # This preserves the original blue pixels and the background
    output_grid = np.copy(input_np)
    height, width = input_np.shape

    # Iterate through each pixel of the input grid to find blue pixels
    for r in range(height):
        for c in range(width):
            # Check if the current pixel in the original input is blue (1)
            if input_np[r, c] == BLUE:
                # Define the relative coordinates and target colors for orthogonal neighbors
                # (delta_row, delta_col), color
                neighbor_rules = [
                    ((-1, 0), RED),    # Up
                    ((+1, 0), AZURE),  # Down
                    ((0, -1), ORANGE), # Left
                    ((0, +1), MAGENTA) # Right
                ]

                # Apply the coloring rules for each neighbor
                for (dr, dc), color in neighbor_rules:
                    nr, nc = r + dr, c + dc # Calculate neighbor coordinates

                    # Check if the neighbor coordinates are within the grid boundaries
                    if 0 <= nr < height and 0 <= nc < width:
                        # Update the corresponding pixel in the output grid with the specified color
                        # Note: This overwrites any existing pixel (including background 0)
                        # In this specific task, neighbors are always background 0 in the input examples.
                        output_grid[nr, nc] = color

    # Convert the final numpy array back to a list of lists before returning
    return output_grid.tolist()