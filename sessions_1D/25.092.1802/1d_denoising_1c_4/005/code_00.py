"""
Retains only the largest contiguous block of pixels (based on 4-way adjacency) 
for each non-white color within the input 2D grid. All pixels of a given color 
that are not part of its single largest contiguous block are changed to white (0).
"""

import numpy as np
from collections import deque

def _find_connected_components(grid, target_color):
    """
    Finds all connected components of a specific color in the grid using 4-way adjacency.

    Args:
        grid (np.array): The 2D input grid.
        target_color (int): The color to find components for.

    Returns:
        list[list[tuple[int, int]]]: A list where each inner list contains 
                                      the (row, col) coordinates of a single 
                                      connected component. Returns empty list
                                      if no pixels of target_color exist.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    components = []

    # Iterate through each pixel in the grid
    for r in range(rows):
        for c in range(cols):
            # If this cell is the target color and hasn't been visited yet, start a search
            if grid[r, c] == target_color and not visited[r, c]:
                # Initialize structure for the current component and the BFS queue
                component = []
                q = deque([(r, c)])
                visited[r, c] = True # Mark the starting pixel as visited

                # Perform Breadth-First Search (BFS)
                while q:
                    curr_r, curr_c = q.popleft()
                    component.append((curr_r, curr_c)) # Add current pixel to the component

                    # Explore 4 adjacent neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc

                        # Check if the neighbor is within grid bounds
                        if 0 <= nr < rows and 0 <= nc < cols:
                            # Check if the neighbor has the target color and hasn't been visited
                            if grid[nr, nc] == target_color and not visited[nr, nc]:
                                visited[nr, nc] = True # Mark neighbor as visited
                                q.append((nr, nc)) # Add neighbor to the queue to explore from later
                
                # Once BFS is complete for this starting pixel, add the found component
                if component:
                    components.append(component)
                    
    return components

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed grid.
    """
    # Ensure input is a numpy array
    if not isinstance(input_grid, np.ndarray):
        input_grid = np.array(input_grid)
        
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Identify all unique non-white colors present in the grid
    unique_colors = np.unique(input_grid)
    non_white_colors = [color for color in unique_colors if color != 0]

    # Process each non-white color independently
    for color in non_white_colors:
        # Find all connected components (objects) of the current color
        components = _find_connected_components(input_grid, color)

        # If there's more than one component for this color, filter out smaller ones
        if len(components) > 1:
            # Find the component with the maximum number of pixels (largest size)
            # The key=len tells max to compare components based on the length of their coordinate lists
            largest_component = max(components, key=len)
            
            # Create a set of coordinates for the largest component for efficient checking later
            # (Optional optimization, direct list comparison works too but might be slower for huge components)
            # largest_component_coords = set(largest_component) 

            # Iterate through all components found for this color
            for component in components:
                # Check if the current component is NOT the largest one 
                # (Direct list comparison is sufficient here as the coordinate lists are unique)
                if component != largest_component: 
                    # If it's a smaller component, change its pixels to white (0) in the output grid
                    for r, c in component:
                        output_grid[r, c] = 0
        
        # If there's only one component (or zero components) of this color, 
        # no changes are needed, as the largest (only) component is implicitly kept 
        # because output_grid started as a copy of input_grid.

    # Return the modified grid
    return output_grid