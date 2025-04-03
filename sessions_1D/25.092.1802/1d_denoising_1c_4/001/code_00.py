"""
Identifies contiguous objects of the same non-white color within a 2D grid representation of the input. 
For each non-white color present, it keeps only the largest contiguous object of that color. 
All pixels belonging to smaller objects of the same color are changed to white (0).
The input is assumed to be a 1D array representing a 4x8 grid.
Connectivity is defined by 4-way adjacency (up, down, left, right).
"""

import numpy as np
from collections import deque

def _find_connected_components(grid, target_color):
    """
    Finds all connected components of a specific color in the grid.

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

    for r in range(rows):
        for c in range(cols):
            # If this cell is the target color and hasn't been visited yet
            if grid[r, c] == target_color and not visited[r, c]:
                # Start a Breadth-First Search (BFS) to find the component
                component = []
                q = deque([(r, c)])
                visited[r, c] = True

                while q:
                    curr_r, curr_c = q.popleft()
                    component.append((curr_r, curr_c))

                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc

                        # Check bounds, color, and visited status
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == target_color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                # Add the found component to the list
                if component:
                    components.append(component)
                    
    return components

def transform(input_array):
    """
    Transforms the input grid by keeping only the largest connected component 
    for each non-white color.

    Args:
        input_array (list[int]): A 1D list representing the input grid pixels.
                                 Assumed to represent a 4x8 grid.

    Returns:
        list[int]: A 1D list representing the transformed grid pixels.
    """
    # --- Grid Initialization and Reshaping ---
    # Assuming the grid is 4x8 based on the 32 elements and visual patterns
    rows, cols = 4, 8
    if len(input_array) != rows * cols:
        # Handle potential dimension mismatch if needed, though examples fit 4x8
        raise ValueError(f"Input array length {len(input_array)} does not match assumed dimensions {rows}x{cols}")
        
    input_grid = np.array(input_array).reshape(rows, cols)
    output_grid = np.copy(input_grid) # Work on a copy

    # --- Identify Colors and Process Each ---
    # Find unique non-white colors in the grid
    unique_colors = np.unique(input_grid)
    non_white_colors = [color for color in unique_colors if color != 0]

    # Process each non-white color separately
    for color in non_white_colors:
        # Find all connected components (objects) of the current color
        components = _find_connected_components(input_grid, color)

        # If there's more than one component, find the largest and remove others
        if len(components) > 1:
            # Find the largest component based on the number of pixels
            largest_component = max(components, key=len)
            largest_component_coords = set(largest_component) # Use a set for efficient lookup

            # Iterate through all components of this color
            for component in components:
                # If this component is NOT the largest one
                if component != largest_component:
                    # Change the color of all pixels in this smaller component to white (0)
                    for r, c in component:
                        output_grid[r, c] = 0
        
        # If there's only one component (or zero), no changes are needed for this color

    # --- Final Output Formatting ---
    # Flatten the 2D output grid back to a 1D list
    return output_grid.flatten().tolist()