import numpy as np
from collections import deque

"""
Identify the non-white color (dominant color) in the input grid.
Find all distinct connected components (groups) of this dominant color, 
considering horizontal, vertical, and diagonal adjacency (8-connectivity).
Determine the component with the largest number of pixels.
Create an output grid of the same dimensions as the input, filled with white (0).
Place the largest identified component onto the output grid at its original coordinates, 
using the dominant color. All other pixels remain white.
"""

def _find_connected_components(grid, target_color):
    """
    Finds all 8-connected components of a specific color in the grid.

    Args:
        grid (np.array): The input grid.
        target_color (int): The color of the components to find.

    Returns:
        list: A list of sets, where each set contains (row, col) tuples
              representing the coordinates of a connected component.
    """
    rows, cols = grid.shape
    visited = set()
    components = []

    # Define 8 directions for neighbors (including diagonals)
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]

    for r in range(rows):
        for c in range(cols):
            # If the cell has the target color and hasn't been visited yet
            if grid[r, c] == target_color and (r, c) not in visited:
                # Start a Breadth-First Search (BFS) to find the component
                component = set()
                queue = deque([(r, c)])
                visited.add((r, c))
                component.add((r, c))

                while queue:
                    row, col = queue.popleft()

                    # Check all 8 neighbors
                    for dr, dc in directions:
                        nr, nc = row + dr, col + dc

                        # Check if the neighbor is within bounds
                        if 0 <= nr < rows and 0 <= nc < cols:
                            # Check if the neighbor has the target color and hasn't been visited
                            if grid[nr, nc] == target_color and (nr, nc) not in visited:
                                visited.add((nr, nc))
                                component.add((nr, nc))
                                queue.append((nr, nc))
                
                # Add the found component to the list
                components.append(component)

    return components

def transform(input_grid):
    """
    Identifies the largest connected component of the dominant non-white color
    in the input grid and returns a new grid containing only that component
    on a white background.

    Args:
        input_grid (list or np.array): A 2D list or numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the output grid.
    """
    # Convert input to numpy array for easier handling
    grid = np.array(input_grid, dtype=int)
    rows, cols = grid.shape
    
    # Initialize output_grid with the background color (white = 0)
    output_grid = np.zeros_like(grid) # Creates a grid of same shape filled with 0s

    # Find the dominant non-white color
    unique_colors = np.unique(grid)
    dominant_color = 0 # Default in case grid is all white
    for color in unique_colors:
        if color != 0:
            dominant_color = color
            break
            
    # If the grid is all white, return the all-white grid
    if dominant_color == 0:
        return output_grid.tolist() # Return as list of lists per ARC standard

    # Find all connected components of the dominant color
    components = _find_connected_components(grid, dominant_color)

    # If no components are found, return the all-white grid
    if not components:
        return output_grid.tolist()

    # Find the largest component (the one with the most pixels)
    largest_component = max(components, key=len)

    # Place the largest component onto the output grid
    for r, c in largest_component:
        output_grid[r, c] = dominant_color

    # Return the output grid as a list of lists
    return output_grid.tolist()