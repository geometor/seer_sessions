"""
Identifies all contiguous objects of the primary non-background color in the input grid using orthogonal adjacency.
Determines the largest object based on pixel count.
Generates an output grid of the same dimensions, initially filled with the background color (white-0).
Places the pixels corresponding to the largest object onto the output grid, preserving their color and position. All other pixels remain background color.
"""

import numpy as np
from collections import deque

def _find_objects(grid, primary_color):
    """
    Finds all connected components (objects) of a specific color in the grid.

    Args:
        grid (np.array): The input grid.
        primary_color (int): The color of the objects to find.

    Returns:
        list: A list of sets, where each set contains the (row, col) coordinates
              of the pixels belonging to a single connected object.
    """
    height, width = grid.shape
    visited = np.zeros((height, width), dtype=bool)
    objects = []

    for r in range(height):
        for c in range(width):
            # If this pixel is the primary color and hasn't been visited yet,
            # start a search (BFS) to find the connected component.
            if grid[r, c] == primary_color and not visited[r, c]:
                current_object = set()
                q = deque([(r, c)])
                visited[r, c] = True

                while q:
                    row, col = q.popleft()
                    current_object.add((row, col))

                    # Check orthogonal neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds and if the neighbor is the same color and unvisited
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] == primary_color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                objects.append(current_object)
    return objects

def transform(input_grid_list):
    """
    Transforms the input grid by keeping only the largest object of the primary color.

    Args:
        input_grid_list (list): A list of lists representing the input grid.

    Returns:
        list: A list of lists representing the transformed output grid.
    """
    input_grid = np.array(input_grid_list)
    height, width = input_grid.shape
    background_color = 0

    # 1: Identify the primary non-background color.
    # Find the first non-zero element or assume if only one non-zero exists.
    unique_colors = np.unique(input_grid)
    primary_color = None
    for color in unique_colors:
        if color != background_color:
            primary_color = color
            break

    # If there's no primary color (grid is all background), return the input.
    if primary_color is None:
        return input_grid_list

    # 2 & 3: Find all distinct contiguous objects and implicitly know their sizes.
    objects = _find_objects(input_grid, primary_color)

    # Handle case where no objects of primary color are found
    if not objects:
         return np.full((height, width), background_color, dtype=int).tolist()

    # 4: Determine the object with the maximum size (pixel count).
    largest_object = max(objects, key=len)

    # 5: Create a new grid filled with the background color.
    output_grid = np.full((height, width), background_color, dtype=int)

    # 6: Place the pixels corresponding to the largest object onto the new grid.
    for r, c in largest_object:
        output_grid[r, c] = primary_color

    return output_grid.tolist()