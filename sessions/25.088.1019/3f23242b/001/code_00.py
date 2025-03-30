import numpy as np

"""
Transforms the input grid by performing the following steps:
1. Creates an output grid of the same dimensions as the input grid, initialized with white pixels (0).
2. Finds the coordinates (row, column) of all green pixels (color 3) in the input grid.
3. For each found green pixel coordinate:
    a. Defines a fixed 5x10 pattern centered conceptually at the green pixel's location.
    b. Iterates through the relative coordinates and colors specified by the pattern.
    c. For each point in the pattern, calculates its absolute coordinates in the output grid based on the green pixel's location.
    d. Checks if the calculated absolute coordinates are within the bounds of the grid.
    e. If the coordinates are valid, places the pattern's specified color at that location in the output grid, overwriting any existing value.
4. Returns the final output grid.

The pattern details relative to the center green pixel (dr=0, dc=0):
- Row dr=-2: Gray (5) from dc=-2 to dc=+2
- Row dr=-1: Red (2) at dc=-2, Gray (5) at dc=0, Red (2) at dc=+2
- Row dr=0:  Red (2) at dc=-2, Green (3) at dc=0, Red (2) at dc=+2
- Row dr=+1: Red (2) at dc=-2, Red (2) at dc=+2
- Row dr=+2: Red (2) at dc=-4 and dc=-3, Azure (8) from dc=-2 to dc=+2, Red (2) at dc=+3, dc=+4, and dc=+5
"""


def transform(input_grid):
    """
    Applies a fixed pattern centered around each green pixel found in the input grid.

    Args:
        input_grid (list of lists of int): The input grid.

    Returns:
        list of lists of int: The transformed grid.
    """
    # Convert input grid to numpy array for easier handling
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Initialize output grid with white pixels (0)
    output_np = np.zeros_like(input_np)

    # Define the pattern as a dictionary: { (relative_row, relative_col): color }
    pattern_map = {
        # Row -2
        (-2, -2): 5, (-2, -1): 5, (-2, 0): 5, (-2, 1): 5, (-2, 2): 5,
        # Row -1
        (-1, -2): 2, (-1, 0): 5, (-1, 2): 2,
        # Row 0 (Center)
        (0, -2): 2, (0, 0): 3, (0, 2): 2,
        # Row +1
        (1, -2): 2, (1, 2): 2,
        # Row +2
        (2, -4): 2, (2, -3): 2, (2, -2): 8, (2, -1): 8, (2, 0): 8, (2, 1): 8, (2, 2): 8, (2, 3): 2, (2, 4): 2, (2, 5): 2,
    }

    # Find coordinates of all green pixels (color 3)
    green_pixels = np.argwhere(input_np == 3)

    # Iterate through each green pixel found
    for r_center, c_center in green_pixels:
        # Apply the pattern centered at this green pixel
        for (dr, dc), color in pattern_map.items():
            # Calculate target coordinates
            target_r = r_center + dr
            target_c = c_center + dc

            # Check if the target coordinates are within the grid boundaries
            if 0 <= target_r < height and 0 <= target_c < width:
                # Place the pattern pixel onto the output grid
                output_np[target_r, target_c] = color

    # Convert the output numpy array back to a list of lists
    output_grid = output_np.tolist()
    return output_grid
