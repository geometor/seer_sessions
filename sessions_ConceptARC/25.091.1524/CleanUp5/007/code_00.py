import numpy as np
from collections import Counter

"""
Transforms the input grid based on the number of distinct non-background colors present.

1. If there is more than one distinct non-background color:
   - Identify the non-background color(s) with the minimum frequency.
   - Change *all* pixels of these minimum-frequency color(s) to the background color (0).

2. If there is exactly one distinct non-background color:
   - Identify this single non-background color.
   - For each pixel of this color, check its 8 neighbors (Moore neighborhood) in the original input grid.
   - If *all* neighbors are the background color (0), change the pixel to the background color (0). Otherwise, leave it unchanged.

3. If there are no non-background colors:
   - The grid remains unchanged.

The background color is assumed to be 0 (White).
"""

def get_neighbors(grid, r, c):
    """
    Gets the values of the 8 neighboring pixels (Moore neighborhood) for a given cell (r, c).
    Handles boundary conditions by only returning values of neighbors within the grid.
    """
    rows, cols = grid.shape
    neighbor_values = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            # Skip the center pixel itself
            if dr == 0 and dc == 0:
                continue

            nr, nc = r + dr, c + dc

            # Check if the neighbor coordinates are within the grid bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbor_values.append(grid[nr, nc])

    return neighbor_values

def transform(input_grid):
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    background_color = 0

    # Find all non-background pixels and their colors
    non_background_pixels = input_grid[input_grid != background_color]

    # Early exit (Case 3): If there are no non-background pixels, return the original grid copy
    if non_background_pixels.size == 0:
        return output_grid

    # Count the frequency of each non-background color
    color_counts = Counter(non_background_pixels)
    distinct_color_count = len(color_counts)

    # Case 1: More than one distinct non-background color
    if distinct_color_count > 1:
        # Find the minimum frequency among non-background colors
        min_frequency = min(color_counts.values())
        # Identify all colors that have this minimum frequency
        target_colors = {color for color, count in color_counts.items() if count == min_frequency}

        # Iterate through the grid and change all pixels of the target color(s) to background
        for r in range(rows):
            for c in range(cols):
                if input_grid[r, c] in target_colors:
                    output_grid[r, c] = background_color

    # Case 2: Exactly one distinct non-background color
    elif distinct_color_count == 1:
        # The single non-background color is the target color
        target_color = list(color_counts.keys())[0] # Get the only key

        # Iterate through the grid
        for r in range(rows):
            for c in range(cols):
                pixel_color = input_grid[r, c]

                # Check if the current pixel's color is the target color
                if pixel_color == target_color:
                    # Get the values of its neighbors from the *input* grid
                    neighbors = get_neighbors(input_grid, r, c)

                    # Check if all neighbors are the background color (i.e., the pixel is isolated)
                    # An empty neighbor list (e.g., 1x1 grid with the target color) also counts as isolated
                    is_isolated = all(neighbor == background_color for neighbor in neighbors)

                    # If the pixel is isolated, change its color to background in the output grid
                    if is_isolated:
                        output_grid[r, c] = background_color
                        
    # Case 3 handled by early exit

    # Return the modified or copied grid
    return output_grid