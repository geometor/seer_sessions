import numpy as np
from collections import Counter

"""
Identify the background color (typically white/0). Find the largest contiguous object composed of non-background colors (considering horizontal and vertical connections). Determine the most frequent color (dominant color) within this largest object. Create the output grid by replacing all pixels within the largest object that are not the dominant color with the dominant color. Leave background pixels and dominant color pixels within the object unchanged.
"""

def find_connected_components(grid, background_color):
    """
    Finds all contiguous components (objects) of non-background colors in the grid.

    Args:
        grid (np.array): The input grid.
        background_color (int): The color designated as background.

    Returns:
        list: A list of lists, where each inner list contains the 
              (row, col) coordinates of a connected component.
    """
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    components = []

    for r in range(rows):
        for c in range(cols):
            # If the cell is not background and not visited yet, start BFS
            if grid[r, c] != background_color and not visited[r, c]:
                component_coords = []
                q = [(r, c)]
                visited[r, c] = True
                
                while q:
                    row, col = q.pop(0)
                    component_coords.append((row, col))

                    # Check neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds and if neighbor is valid (not background, not visited)
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] != background_color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                components.append(component_coords)
                
    return components

def get_dominant_color(grid, object_coords):
    """
    Finds the most frequent color within a given set of coordinates in the grid.

    Args:
        grid (np.array): The input grid.
        object_coords (list): A list of (row, col) coordinates for the object.

    Returns:
        int: The most frequent color value. Returns -1 if object_coords is empty.
    """
    if not object_coords:
        return -1 # Or raise an error, or handle as appropriate

    colors = [grid[r, c] for r, c in object_coords]
    if not colors:
        return -1 # Should not happen if object_coords is not empty, but safety check
        
    color_counts = Counter(colors)
    dominant_color = color_counts.most_common(1)[0][0]
    return dominant_color

def transform(input_grid):
    """
    Homogenizes the color of the largest non-background object in the grid.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to numpy array for easier handling
    grid_np = np.array(input_grid, dtype=int)
    output_grid = grid_np.copy() # Initialize output_grid as a copy

    # --- Workflow ---
    
    # 1. Identify background color (assuming 0 based on examples)
    background_color = 0 

    # 2. Find all connected components (objects) of non-background colors
    components = find_connected_components(grid_np, background_color)

    # If no non-background components found, return the original grid
    if not components:
        return output_grid.tolist()

    # 3. Identify the largest component (main object)
    largest_component = max(components, key=len)

    # 4. Determine the dominant color of the largest component
    dominant_color = get_dominant_color(grid_np, largest_component)

    # 5. Replace impurities within the largest component
    for r, c in largest_component:
        # Change the color in the output grid to the dominant color
        # This effectively replaces both dominant and non-dominant colors within the object's area
        # with the dominant color, achieving homogenization.
        output_grid[r, c] = dominant_color
        
    # Return the modified grid as a list of lists
    return output_grid.tolist()