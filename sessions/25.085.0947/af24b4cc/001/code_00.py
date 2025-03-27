import numpy as np
from collections import Counter

"""
Identifies 6 distinct connected components (objects) of non-white pixels in the input grid using 8-way adjacency.
Sorts these components spatially (top-to-bottom, then left-to-right).
For each component, determines the most frequent non-white color.
If there's a tie in frequency, selects the color that appears first when scanning the component's pixels top-to-bottom, then left-to-right.
Constructs a 4x5 output grid, placing the determined dominant colors from the 6 components into the cells (1,1) through (2,3) in their sorted order.
"""

def find_connected_components(grid):
    """
    Finds all connected components of non-white pixels using 8-way adjacency.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of components. Each component is a list of (row, col, color) tuples.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    components = []
    
    # Define 8-way connectivity neighbors (relative coordinates)
    neighbors = [(-1, -1), (-1, 0), (-1, 1),
                 (0, -1),          (0, 1),
                 (1, -1), (1, 0), (1, 1)]

    for r in range(rows):
        for c in range(cols):
            # If pixel is non-white and not visited, start BFS
            if grid[r, c] != 0 and not visited[r, c]:
                component_pixels = []
                q = [(r, c)]
                visited[r, c] = True
                
                while q:
                    row, col = q.pop(0)
                    color = grid[row, col]
                    component_pixels.append((row, col, color))
                    
                    # Check neighbors
                    for dr, dc in neighbors:
                        nr, nc = row + dr, col + dc
                        # Check bounds, if non-white, and not visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] != 0 and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                # Sort pixels within the component for consistent tie-breaking order later
                component_pixels.sort() 
                components.append(component_pixels)
                
    return components

def get_dominant_color(component):
    """
    Determines the dominant color in a component based on frequency,
    with tie-breaking based on scan order (top-to-bottom, left-to-right).

    Args:
        component (list): A list of (row, col, color) tuples representing the component,
                          pre-sorted by row, then column.

    Returns:
        int: The dominant color.
    """
    if not component:
        return 0 # Should not happen with non-empty components

    # Count frequencies of colors
    colors = [pixel[2] for pixel in component]
    color_counts = Counter(colors)
    
    if not color_counts:
         return 0 # Empty component case
         
    # Find the maximum frequency
    max_freq = 0
    for color in color_counts:
        if color_counts[color] > max_freq:
            max_freq = color_counts[color]

    # Identify colors with the maximum frequency
    tied_colors = {color for color, count in color_counts.items() if count == max_freq}

    # If only one color has max frequency, return it
    if len(tied_colors) == 1:
        return tied_colors.pop()
    else:
        # Tie-breaking: iterate through sorted pixels and return the first color found that is in the tied set
        for r, c, color in component:
            if color in tied_colors:
                return color
        
        # Fallback, should ideally not be reached if component is non-empty and tied_colors has elements
        return component[0][2] 


def transform(input_grid):
    """
    Transforms the input grid based on finding dominant colors in connected components.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed output grid.
    """
    input_np = np.array(input_grid, dtype=int)
    
    # Initialize output grid (4x5, white)
    output_grid = np.zeros((4, 5), dtype=int)

    # Find connected components
    components = find_connected_components(input_np)

    # Sort components based on the top-most, then left-most pixel
    def sort_key(component):
        min_row = min(p[0] for p in component)
        min_col = min(p[1] for p in component if p[0] == min_row)
        return (min_row, min_col)

    components.sort(key=sort_key)

    # Determine dominant color for each component
    dominant_colors = [get_dominant_color(comp) for comp in components]

    # Populate the 2x3 area in the output grid
    output_indices = [(1, 1), (1, 2), (1, 3), 
                      (2, 1), (2, 2), (2, 3)]
    
    for i, color in enumerate(dominant_colors):
        if i < len(output_indices): # Ensure we don't exceed the 6 target cells
            r, c = output_indices[i]
            output_grid[r, c] = color

    # Convert back to list of lists for the required output format
    return output_grid.tolist()