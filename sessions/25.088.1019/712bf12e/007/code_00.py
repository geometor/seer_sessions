"""
Perform a flood fill starting from all red (color 2) pixels in the input grid.
The fill spreads to adjacent (up, down, left, right) white (color 0) pixels, turning them red.
Any non-white pixel (colors 1, 3-9) acts as a barrier, stopping the fill in that direction.
Barrier pixels and the original red pixels retain their original colors.
"""

import numpy as np
from collections import deque

def find_pixels_by_color(grid, color_value):
    """
    Finds the coordinates of all pixels with a specific color value.

    Args:
        grid (np.array): The input grid.
        color_value (int): The color value to search for.

    Returns:
        list: A list of tuples, where each tuple is (row, column) coordinate.
    """
    rows, cols = np.where(grid == color_value)
    return list(zip(rows, cols))

def transform(input_grid):
    """
    Applies a flood fill transformation starting from red pixels.

    Args:
        input_grid (np.array): A 2D NumPy array representing the input grid.

    Returns:
        np.array: A 2D NumPy array representing the transformed output grid.
    """
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    num_rows, num_cols = input_grid.shape
    
    # Define the target fill color (red) and the background color to fill (white)
    fill_color = 2
    background_color = 0

    # Find all initial red (2) pixels (source pixels) in the input grid
    source_pixel_coords = find_pixels_by_color(input_grid, fill_color)

    # Initialize a queue for Breadth-First Search (BFS)
    queue = deque()
    # Initialize a set to keep track of visited coordinates to avoid cycles and redundant checks
    visited = set()

    # Add all source pixels to the queue and mark them as visited
    # Note: We don't change the source pixels themselves, but start the fill *from* them.
    # The visited set prevents us from adding neighbors of already processed cells unnecessarily.
    # We will process neighbors *of* these source pixels.
    for r, c in source_pixel_coords:
        # Add neighbors of source pixels if they are white (0)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]: # Right, Left, Down, Up
            nr, nc = r + dr, c + dc
            
            # Check boundaries
            if 0 <= nr < num_rows and 0 <= nc < num_cols:
                # Check if the neighbor is white and not visited
                if input_grid[nr, nc] == background_color and (nr, nc) not in visited:
                    # Mark as visited
                    visited.add((nr, nc))
                    # Change color in the output grid
                    output_grid[nr, nc] = fill_color
                    # Add to the queue to process its neighbors later
                    queue.append((nr, nc))

    # Perform BFS starting from the neighbors of the initial red pixels
    while queue:
        # Get the next coordinate from the queue
        r, c = queue.popleft()

        # Explore its 4-directional neighbors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]: # Right, Left, Down, Up
            nr, nc = r + dr, c + dc

            # Check boundaries
            if 0 <= nr < num_rows and 0 <= nc < num_cols:
                # Check if the neighbor is white (background) in the *input* grid
                # and hasn't been visited/added to the queue yet.
                # We check input_grid because non-white pixels are barriers.
                if input_grid[nr, nc] == background_color and (nr, nc) not in visited:
                    # Mark as visited
                    visited.add((nr, nc))
                    # Change color in the output grid
                    output_grid[nr, nc] = fill_color
                    # Add to the queue to process its neighbors later
                    queue.append((nr, nc))

    # Return the modified grid
    return output_grid