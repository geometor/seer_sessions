import numpy as np

"""
Determine the connectivity of red (2) pixels in a 3x3 input grid.
If all red pixels form a single connected component (considering horizontal, vertical, and diagonal adjacency), the output is a 1x1 grid with orange (7).
Otherwise (if there are no red pixels or multiple disconnected components of red pixels), the output is a 1x1 grid with blue (1).
"""

def find_pixels(grid, color):
    """Finds all coordinates of pixels with a specific color."""
    coords = np.argwhere(grid == color)
    # Convert to list of tuples for easier handling
    return [tuple(coord) for coord in coords]

def get_neighbors(coord, grid_shape):
    """Gets all 8 neighboring coordinates (including diagonals) within grid bounds."""
    row, col = coord
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue # Skip self
            nr, nc = row + dr, col + dc
            # Check bounds
            if 0 <= nr < grid_shape[0] and 0 <= nc < grid_shape[1]:
                neighbors.append((nr, nc))
    return neighbors

def find_connected_components(grid, color):
    """Finds the number of connected components for a given color, considering diagonal adjacency."""
    pixels = find_pixels(grid, color)
    if not pixels:
        return 0 # No pixels of the given color

    visited = set()
    num_components = 0
    grid_shape = grid.shape

    for pixel in pixels:
        if pixel not in visited:
            num_components += 1
            # Start a search (BFS or DFS) from this pixel
            queue = [pixel]
            visited.add(pixel)
            while queue:
                current_pixel = queue.pop(0)
                for neighbor in get_neighbors(current_pixel, grid_shape):
                    # Check if neighbor is the target color and not visited
                    if grid[neighbor] == color and neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
                        
    return num_components

def transform(input_grid):
    """
    Transforms the input grid based on the connectivity of red pixels.
    """
    # Convert input list of lists to numpy array for easier processing
    grid = np.array(input_grid)

    # Define the target color (red)
    target_color = 2

    # Find the number of connected components of the target color
    num_components = find_connected_components(grid, target_color)

    # Determine the output color based on the number of components
    if num_components == 1:
        output_color = 7 # orange
    else: # Handles 0 components or > 1 component
        output_color = 1 # blue

    # Initialize the output grid as a 1x1 numpy array
    output_grid = np.array([[output_color]])

    return output_grid.tolist() # Convert back to list of lists as required by the framework