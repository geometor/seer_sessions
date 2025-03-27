```python
"""
Identify all connected components of green pixels (value 3) in the input grid, 
considering 8-way connectivity (horizontal, vertical, and diagonal). 
Find the component with the largest number of pixels. Change the color of all 
pixels belonging to this largest component from green (3) to azure (8). 
Leave all other pixels (white pixels and green pixels not in the largest component) 
unchanged.
"""

import numpy as np
from collections import deque

def find_connected_components(grid, target_color):
    """
    Finds all connected components of a specific color in a grid using 8-way connectivity.

    Args:
        grid (np.ndarray): The input grid.
        target_color (int): The color of the pixels to form components.

    Returns:
        list: A list of components, where each component is a list of (row, col) tuples.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    components = []

    # Define 8 directions for neighbors (including diagonals)
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),          (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]

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

                    # Check all 8 neighbors
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
    Transforms the input grid by changing the color of the largest connected 
    component of green (3) pixels to azure (8).

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    
    # Define the target color (green)
    target_color = 3
    # Define the replacement color (azure)
    replacement_color = 8

    # Find all connected components of the target color (green)
    components = find_connected_components(output_grid, target_color)

    # If no green components are found, return the original grid copy
    if not components:
        return output_grid

    # Find the largest component
    largest_component = []
    max_size = 0
    for component in components:
        if len(component) > max_size:
            max_size = len(component)
            largest_component = component
        # Note: If there's a tie for the largest size, this implementation 
        # will pick the first one encountered. Based on the problem description 
        # assuming a unique largest component.

    # Change the color of pixels in the largest component
    if largest_component: # Ensure a largest component was actually found
        for r, c in largest_component:
            output_grid[r, c] = replacement_color

    # Return the modified grid
    return output_grid
```