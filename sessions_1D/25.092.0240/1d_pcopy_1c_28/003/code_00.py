import numpy as np
import copy

"""
Transforms a 2D grid based on the following rule:
1. Identify the single non-white (non-zero) color present in the input grid ('active_color'). If none exists, return the input grid unchanged.
2. Create a copy of the input grid to serve as the output grid.
3. Iterate through each pixel of the *input* grid.
4. If a pixel contains the 'active_color':
    a. Check its immediate horizontal neighbor to the left. If this neighbor exists (is within grid bounds) and is white (0) in the *input* grid, mark this neighbor's coordinates for coloring.
    b. Check its immediate horizontal neighbor to the right. If this neighbor exists (is within grid bounds) and is white (0) in the *input* grid, mark this neighbor's coordinates for coloring.
5. After checking all active pixels, change the color of all marked white neighbors in the *output* grid to the 'active_color'.
6. Return the modified output grid.
"""

def find_active_color(grid):
    """
    Finds the unique non-zero color in the grid.
    Returns the color value or 0 if none is found or multiple are found (though examples suggest only one).
    """
    unique_colors = np.unique(grid)
    active_color = 0
    non_zero_count = 0
    for color in unique_colors:
        if color != 0:
            active_color = color
            non_zero_count += 1

    # Based on examples, we expect exactly one active color.
    # If there's none or more than one, the rule might not apply as expected.
    # Returning 0 handles the 'all white' case gracefully.
    if non_zero_count != 1:
         # Check if grid is all zeros
        if np.all(grid == 0):
            return 0 # No active color
        else:
            # If there are non-zero colors but not exactly one,
            # return the first one found based on example structure,
            # but acknowledge this might be an edge case.
            for color in unique_colors:
                 if color != 0:
                     return color # Return first non-zero found
            return 0 # Should not happen if unique_colors had non-zeros

    return active_color

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    # Find the active color
    active_color = find_active_color(input_grid)

    # If no active color (grid is all white or assumption violated), return copy
    if active_color == 0:
        return copy.deepcopy(input_grid)

    # Get grid dimensions
    rows, cols = input_grid.shape

    # Initialize output_grid as a copy of the input
    output_grid = copy.deepcopy(input_grid)

    # Use a set to store coordinates of white neighbors to color (avoids duplicates)
    pixels_to_color = set()

    # Iterate through the input grid to find active pixels and identify neighbors
    for r in range(rows):
        for c in range(cols):
            # Check if the current pixel has the active color
            if input_grid[r, c] == active_color:
                # Check left neighbor
                if c > 0 and input_grid[r, c - 1] == 0:
                    pixels_to_color.add((r, c - 1))

                # Check right neighbor
                if c < cols - 1 and input_grid[r, c + 1] == 0:
                    pixels_to_color.add((r, c + 1))

    # Apply the color changes to the output grid
    for r_change, c_change in pixels_to_color:
        output_grid[r_change, c_change] = active_color

    return output_grid