"""
Transforms an input grid by keeping only the largest contiguous object (based on 4-way adjacency) for each non-white color. 
All pixels belonging to smaller objects of the same color are changed to white (0). 
The input is assumed to be a list of integers representing a 4x8 grid.
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
                
                # Add the found component to the list if it's not empty
                if component:
                    components.append(component)
                    
    return components

def transform(input_array):
    """
    Applies the transformation rule to the input grid represented by input_array.

    Args:
        input_array (list[int]): A 1D list representing the input grid pixels.
                                 Assumed to represent a 4x8 grid.

    Returns:
        list[int]: A 1D list representing the transformed grid pixels.
    """
    # --- Grid Initialization and Reshaping ---
    # Assume dimensions 4x8 based on analysis (32 elements)
    rows, cols = 4, 8
    expected_length = rows * cols
    if len(input_array) != expected_length:
        # Basic validation, could raise error or try to infer dimensions
        print(f"Warning: Input array length {len(input_array)} does not match expected {expected_length}")
        # Attempt to infer if possible, otherwise error out. For now, assume 4x8.
        if len(input_array) == 32: # proceed if length is correct
             pass
        else: # fail if length is not 32
            raise ValueError(f"Input array length {len(input_array)} does not match assumed dimensions {rows}x{cols}")

    input_grid = np.array(input_array).reshape(rows, cols)
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid) 

    # --- Identify Colors and Process Each ---
    # Find unique non-white colors present in the grid
    unique_colors = np.unique(input_grid)
    non_white_colors = [color for color in unique_colors if color != 0]

    # Process each non-white color independently
    for color in non_white_colors:
        # Find all connected components (objects) of the current color using the helper function
        components = _find_connected_components(input_grid, color)

        # If there's more than one component for this color, apply the filtering logic
        if len(components) > 1:
            # Find the largest component based on the number of pixels (size)
            # The key=len tells max to compare the components based on their length (list of coordinates)
            largest_component = max(components, key=len)
            
            # Create a set of coordinates for the largest component for efficient lookup
            largest_component_coords = set(largest_component)

            # Iterate through all components found for this color
            for component in components:
                # Check if the current component is NOT the largest one
                # Comparing lists directly works here as component lists are unique
                if component != largest_component: 
                    # If it's a smaller component, change its pixels to white (0) in the output grid
                    for r, c in component:
                        output_grid[r, c] = 0
        
        # If there's only one component (or zero), no changes are needed for this color, 
        # as the single largest component is kept by default (output_grid started as a copy)

    # --- Final Output Formatting ---
    # Flatten the 2D output grid back into a 1D list for the return value
    return output_grid.flatten().tolist()