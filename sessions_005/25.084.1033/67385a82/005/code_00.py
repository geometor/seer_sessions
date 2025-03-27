"""
Transforms the input grid based on the following rules:
1. Identify all connected components of green pixels (value 3) using 4-way (von Neumann) adjacency.
2. Select components with a size (number of pixels) of 3 or more.
3. For each selected component, change the color of all pixels within that component from green (3) to azure (8).
4. Leave all other pixels unchanged.
"""

import numpy as np
from collections import deque

def find_connected_components_4way(grid, target_color):
    """
    Finds all connected components of a specific color in a grid using 4-way connectivity.

    Args:
        grid (np.ndarray): The input grid.
        target_color (int): The color of the pixels to form components.

    Returns:
        list: A list of components, where each component is a list of (row, col) tuples.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    components = []

    # Define 4 directions for neighbors (up, down, left, right)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for r in range(rows):
        for c in range(cols):
            # If we find a pixel of the target color that hasn't been visited
            if grid[r, c] == target_color and not visited[r, c]:
                current_component = []
                q = deque([(r, c)])
                visited[r, c] = True

                # Start Breadth-First Search (BFS)
                while q:
                    curr_r, curr_c = q.popleft()
                    current_component.append((curr_r, curr_c))

                    # Check all 4 neighbors
                    for dr, dc in directions:
                        nr, nc = curr_r + dr, curr_c + dc

                        # Check if neighbor is within bounds
                        if 0 <= nr < rows and 0 <= nc < cols:
                            # Check if neighbor is the target color and not visited
                            if grid[nr, nc] == target_color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                
                # Add the found component to the list
                components.append(current_component)

    return components

def transform(input_grid):
    """
    Applies the transformation rule based on 4-way green components of size 3 or more.
    """
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    
    # Define constants
    target_color = 3  # green
    replacement_color = 8  # azure
    size_threshold = 3

    # 1. Identify all 4-way connected components of green pixels
    components = find_connected_components_4way(output_grid, target_color)

    # Process each component
    for component in components:
        # 2. Check if the component size is 3 or more
        if len(component) >= size_threshold:
            # 3. Change the color of all pixels in the selected component
            for r, c in component:
                # Ensure the pixel is actually green before changing (safety check)
                if output_grid[r, c] == target_color:
                    output_grid[r, c] = replacement_color

    # 4. Return the modified grid (unchanged pixels are implicitly handled by the initial copy)
    return output_grid
