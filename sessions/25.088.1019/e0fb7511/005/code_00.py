"""
Identify contiguous regions of white pixels (0). If a region does not touch any of the grid's borders, change all pixels in that region to azure (8). Otherwise, leave the white pixels as they are. Blue pixels (1) remain unchanged.
"""

import numpy as np
from collections import deque

def find_connected_regions(grid, target_color=0):
    """
    Finds all contiguous regions of a specific color using BFS.

    Args:
        grid (np.ndarray): The input grid.
        target_color (int): The color of the regions to find.

    Returns:
        list[tuple(list[tuple(int, int)], bool)]: A list where each element represents a region.
            Each element is a tuple containing:
            - A list of (row, col) coordinates of pixels in the region.
            - A boolean indicating whether the region touches the border.
    """
    height, width = grid.shape
    visited = np.zeros((height, width), dtype=bool)
    regions = []

    for r in range(height):
        for c in range(width):
            # If the pixel has the target color and hasn't been visited yet, start a BFS
            if grid[r, c] == target_color and not visited[r, c]:
                current_region_pixels = []
                queue = deque([(r, c)])
                visited[r, c] = True
                touches_border = False

                while queue:
                    curr_r, curr_c = queue.popleft()
                    current_region_pixels.append((curr_r, curr_c))

                    # Check if the current pixel is on the border
                    if curr_r == 0 or curr_r == height - 1 or curr_c == 0 or curr_c == width - 1:
                        touches_border = True

                    # Explore cardinal neighbors (up, down, left, right)
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nr, nc = curr_r + dr, curr_c + dc

                        # Check if neighbor is within bounds
                        if 0 <= nr < height and 0 <= nc < width:
                            # Check if neighbor has the target color and not yet visited
                            if grid[nr, nc] == target_color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                queue.append((nr, nc))

                # Add the found region and its border status to the list
                regions.append((current_region_pixels, touches_border))

    return regions

def transform(input_grid):
    """
    Transforms the input grid by finding enclosed white regions (not touching borders)
    and coloring them azure (8).

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    # Convert input to numpy array for efficient processing
    input_grid_np = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input grid
    output_grid = input_grid_np.copy()
    
    # Define the colors involved
    white_color = 0
    azure_color = 8

    # Find all connected regions of white pixels
    white_regions = find_connected_regions(input_grid_np, target_color=white_color)

    # Process each white region
    for region_pixels, touches_border in white_regions:
        # If the region does NOT touch the border, color it azure
        if not touches_border:
            for r, c in region_pixels:
                output_grid[r, c] = azure_color
        # Otherwise (if it touches the border), leave it as white (already copied)

    # Convert the final numpy array back to a list of lists
    return output_grid.tolist()