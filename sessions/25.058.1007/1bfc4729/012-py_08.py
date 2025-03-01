"""
Transforms an input grid by expanding blue (1) and yellow (4) pixels into regions. Blue pixels expand upwards and downwards. Yellow pixels expand downwards and upwards. The expansion stops based on proximity to each other or the grid boundaries.
"""

import numpy as np

def find_pixels(grid, color_value):
    """Finds the coordinates of all pixels with a specific color value."""
    positions = []
    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            if value == color_value:
                positions.append((r, c))
    return positions

def transform(input_grid):
    output_grid = np.zeros_like(input_grid)  # Initialize with black (0)
    
    blue_pixels = find_pixels(input_grid, 1)
    yellow_pixels = find_pixels(input_grid, 4)

    # Blue Expansion
    if blue_pixels:
        for blue_pos in blue_pixels:
            # Upward expansion
            for r in range(blue_pos[0] + 1):
                output_grid[r, :] = 1
            # Downward expansion to original blue row
            for r in range(blue_pos[0] + 1):
                output_grid[r,:] = 1
            
            if not yellow_pixels: # expand to bottom if no yellow pixels
              for r in range(blue_pos[0] + 1, output_grid.shape[0]):
                output_grid[r,:] = 1

    # Yellow Expansion
    if yellow_pixels:
        for yellow_pos in yellow_pixels:
            # Downward expansion
            for r in range(yellow_pos[0], input_grid.shape[0]):
                output_grid[r, :] = 4

            # Upward expansion
            if not blue_pixels: #Expand upwards to top if no blue pixels
              for r in range(yellow_pos[0]):
                output_grid[r,:] = 4
            if blue_pixels: # Expand upwards to row below original blue pixel
              for blue_pos in blue_pixels:
                for r in range(blue_pos[0]+1, yellow_pos[0]):
                    output_grid[r,:] = 0

    return output_grid