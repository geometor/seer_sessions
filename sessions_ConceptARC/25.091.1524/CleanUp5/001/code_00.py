import numpy as np
from collections import Counter

"""
Identifies the non-background color(s) with the minimum frequency in the input grid.
Then, for each pixel of that minimum frequency color ('target color'), 
it checks its 8 neighbors (Moore neighborhood) in the original input grid. 
If all existing neighbors are the background color (0, White), the target pixel 
is changed to the background color in the output grid. 
All other pixels retain their original color.
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
    """
    Transforms the input grid based on the isolation of the least frequent non-background color.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    background_color = 0

    # Find all non-background pixels and their colors
    non_background_pixels = input_grid[input_grid != background_color]

    # If there are no non-background pixels, return the original grid
    if non_background_pixels.size == 0:
        return output_grid

    # Count the frequency of each non-background color
    color_counts = Counter(non_background_pixels)

    # Find the minimum frequency
    min_frequency = min(color_counts.values())

    # Identify all colors that have the minimum frequency
    target_colors = {color for color, count in color_counts.items() if count == min_frequency}

    # Iterate through each pixel of the input grid
    for r in range(rows):
        for c in range(cols):
            pixel_color = input_grid[r, c]

            # Check if the current pixel's color is one of the target colors
            if pixel_color in target_colors:
                # Get the values of its neighbors from the *input* grid
                neighbors = get_neighbors(input_grid, r, c)
                
                # Check if all neighbors are the background color
                # An empty neighbor list (e.g., 1x1 grid) also counts as isolated
                is_isolated = all(neighbor == background_color for neighbor in neighbors)
                
                # If the pixel is isolated, change its color to background in the output grid
                if is_isolated:
                    output_grid[r, c] = background_color

    return output_grid