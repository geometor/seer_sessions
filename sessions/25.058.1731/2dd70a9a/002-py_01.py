"""
The transformation rule is as follows:
1. Identify Seed Points: Find all green (3) pixels in the input grid. Also, Identify the red (2) pixel.
2. Green Expansion: Starting from the green pixels closest to red, iteratively expand the green (3) color to adjacent white (0) pixels. The growth of green is limited by azure, red, and other green pixels.
3. Azure Preservation: Azure (8) pixels remain unchanged throughout the transformation.
4. Red Preservation: Red (2) pixels remain unchanged.

In simple terms, green expands from existing green pixels that are closest to the red pixel. Green replaces white and stops at azure or red, or itself.
"""

import numpy as np
from collections import deque

def find_pixels(grid, color):
    """Finds all pixels of a given color in the grid."""
    return np.argwhere(grid == color)

def closest_green_to_red(red_pixels, green_pixels):
    """Finds the green pixel(s) closest to any red pixel."""
    if not red_pixels.size or not green_pixels.size:
        return []

    red_pixel = red_pixels[0]  # Assuming there's only one red pixel
    distances = np.sum((green_pixels - red_pixel) ** 2, axis=1)
    min_dist = np.min(distances)
    closest_greens = green_pixels[distances == min_dist]
    return closest_greens

def transform(input_grid):
    """Transforms the input grid according to the specified rule."""
    
    grid = np.array(input_grid)  # Convert to NumPy array
    output_grid = np.copy(grid)
    
    red_pixels = find_pixels(grid, 2)
    green_pixels = find_pixels(grid, 3)
    
    seed_pixels = closest_green_to_red(red_pixels, green_pixels)
    if not seed_pixels.size and green_pixels.size:
      seed_pixels = green_pixels

    queue = deque(seed_pixels)


    visited = set()
    for r, c in seed_pixels:
      visited.add((r,c))
    
    while queue:
        row, col = queue.popleft()
        output_grid[row, col] = 3

        # Check adjacent pixels
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_row, new_col = row + dr, col + dc

            # Check boundaries
            if 0 <= new_row < grid.shape[0] and 0 <= new_col < grid.shape[1]:
                # Check if the pixel is white and hasn't been visited
                if grid[new_row, new_col] == 0 and (new_row, new_col) not in visited:
                    queue.append((new_row, new_col))
                    visited.add((new_row, new_col))

    return output_grid.tolist()