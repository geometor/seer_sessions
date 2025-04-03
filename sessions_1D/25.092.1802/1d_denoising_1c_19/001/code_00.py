import numpy as np
from collections import deque

"""
Identify all unique non-background colors present in the input grid.
For each unique non-background color:
  Find all distinct connected components (objects) composed of pixels of this color (using horizontal/vertical adjacency).
  Calculate the size (number of pixels) of each component.
  Identify the component with the maximum size.
Initialize an output grid of the same dimensions as the input, filled with the background color (white, 0).
For each non-background color, add the pixels of its largest component to the output grid, preserving their original color.
The resulting grid is the final output.
"""

def find_connected_components(grid, color):
    """
    Finds all connected components of a specific color in a grid.

    Args:
        grid (np.array): The input grid.
        color (int): The color to find components for.

    Returns:
        list: A list of components, where each component is a list of (row, col) tuples.
    """
    rows, cols = grid.shape
    visited = set()
    components = []

    for r in range(rows):
        for c in range(cols):
            # Check if the current cell is the target color and hasn't been visited
            if grid[r, c] == color and (r, c) not in visited:
                # Start a Breadth-First Search (BFS) to find the component
                current_component = []
                q = deque([(r, c)])
                visited.add((r, c))

                while q:
                    row, col = q.popleft()
                    current_component.append((row, col))

                    # Check neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc

                        # Check boundaries
                        if 0 <= nr < rows and 0 <= nc < cols:
                            # Check if neighbor is the target color and not visited
                            if grid[nr, nc] == color and (nr, nc) not in visited:
                                visited.add((nr, nc))
                                q.append((nr, nc))
                
                # Add the found component to the list
                if current_component:
                    components.append(current_component)
    return components

def transform(input_grid):
    """
    Transforms the input grid by keeping only the largest connected component
    for each non-background color.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    input_grid = np.array(input_grid) # Ensure input is a numpy array
    rows, cols = input_grid.shape
    background_color = 0

    # Initialize output_grid with the background color
    output_grid = np.full((rows, cols), background_color, dtype=int)

    # Find unique non-background colors
    unique_colors = np.unique(input_grid)
    non_background_colors = [color for color in unique_colors if color != background_color]

    # Process each non-background color
    for color in non_background_colors:
        # Find all connected components of the current color
        components = find_connected_components(input_grid, color)

        # If no components found for this color, continue
        if not components:
            continue

        # Find the largest component (by number of pixels)
        largest_component = max(components, key=len)

        # Add the pixels of the largest component to the output grid
        for r, c in largest_component:
            output_grid[r, c] = color

    return output_grid.tolist() # Return as a list of lists