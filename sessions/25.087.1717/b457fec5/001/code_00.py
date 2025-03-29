import numpy as np
from collections import deque

"""
Identifies a horizontal sequence of non-white (0), non-gray (5) colors (the 'key sequence').
Identifies all distinct connected components (objects) of gray (5) pixels.
Replaces the gray pixels in each object with colors from the key sequence, applied cyclically.
The coloring order within an object follows the grid scan order (top-to-bottom, left-to-right).
Each object starts its coloring cycle from the beginning of the key sequence.
Pixels that are not gray and not part of the key sequence remain unchanged.
The original key sequence also remains unchanged in the output.
"""

def find_key_sequence(grid):
    """
    Finds the first horizontal contiguous sequence of non-white (0), non-gray (5) pixels.

    Args:
        grid: numpy array representing the input grid.

    Returns:
        A list of colors in the key sequence, or None if not found.
    """
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and grid[r, c] != 5:
                sequence = []
                start_c = c
                while c < cols and grid[r, c] != 0 and grid[r, c] != 5:
                    sequence.append(grid[r, c])
                    c += 1
                # Ensure it's contiguous and horizontal, return the first one found
                if sequence:
                    return sequence
    return None # No sequence found

def find_connected_components(grid, color):
    """
    Finds all connected components of a specific color using 4-way adjacency.

    Args:
        grid: numpy array representing the input grid.
        color: The target color for finding components.

    Returns:
        A list of sets, where each set contains (row, col) tuples for a component.
    """
    rows, cols = grid.shape
    visited = set()
    components = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and (r, c) not in visited:
                # Start BFS for a new component
                component = set()
                q = deque([(r, c)])
                visited.add((r, c))
                
                while q:
                    curr_r, curr_c = q.popleft()
                    component.add((curr_r, curr_c))

                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        
                        # Check bounds and color match
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            q.append((nr, nc))
                            
                if component:
                    components.append(component)
                    
    return components

def transform(input_grid):
    """
    Transforms the input grid by coloring gray objects based on a key sequence.

    Args:
        input_grid: A numpy array representing the input grid.

    Returns:
        A numpy array representing the transformed output grid.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Find the key sequence
    key_sequence = find_key_sequence(input_grid)
    if not key_sequence:
        # If no key sequence, return the original grid (or handle as error)
        return output_grid 
        
    key_len = len(key_sequence)
    if key_len == 0: # Should not happen if find_key_sequence returns list, but check
        return output_grid

    # 2. Find all gray (5) objects (connected components)
    gray_objects = find_connected_components(input_grid, 5)

    # 3. Color each gray object
    for component in gray_objects:
        # Get coordinates and sort them by scan order (row, then column)
        sorted_coords = sorted(list(component), key=lambda x: (x[0], x[1]))
        
        # Iterate through the sorted coordinates and apply colors cyclically
        for i, (r, c) in enumerate(sorted_coords):
            color_index = i % key_len
            new_color = key_sequence[color_index]
            output_grid[r, c] = new_color
            
    # 4. Return the modified grid
    return output_grid