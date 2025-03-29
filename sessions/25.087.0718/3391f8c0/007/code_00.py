import numpy as np
from collections import deque

"""
The transformation identifies the two distinct non-white colors present in the input grid.
It then finds all distinct objects (contiguous areas of the same non-white color).
An output grid of the same size is created, initially filled with the background color (white, 0).
The transformation then redraws each object found in the input grid onto the output grid, but swaps its color.
Objects originally of the first non-white color are drawn with the second non-white color, and vice versa.
The position and shape of each object remain the same; only their colors are swapped.
Background pixels (white) remain white.
"""

def find_objects(grid: np.ndarray) -> list[tuple[int, set[tuple[int, int]]]]:
    """
    Finds all connected objects of the same non-white color in the grid.

    Args:
        grid: The input numpy array grid.

    Returns:
        A list where each element is a tuple: (color, set_of_coordinates).
        Each set_of_coordinates contains (row, col) tuples for pixels belonging to that object.
    """
    rows, cols = grid.shape
    visited = set()
    objects = []
    
    for r in range(rows):
        for c in range(cols):
            # Check if the pixel is non-white and not visited yet
            if grid[r, c] != 0 and (r, c) not in visited:
                color = grid[r, c]
                current_object_coords = set()
                q = deque([(r, c)])
                visited.add((r, c))
                current_object_coords.add((r, c))
                
                # Start Breadth-First Search (BFS) to find connected pixels of the same color
                while q:
                    row, col = q.popleft()
                    
                    # Check 4-directional neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        
                        # Check bounds and if neighbor is part of the same object
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            current_object_coords.add((nr, nc))
                            q.append((nr, nc))
                            
                # Add the found object (color and coordinates) to the list
                if current_object_coords:
                    objects.append((color, current_object_coords))
                    
    return objects

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Swaps the colors of distinct objects based on the two non-white colors found.

    Args:
        input_grid: A numpy array representing the input grid.

    Returns:
        A numpy array representing the output grid with object colors swapped.
    """
    # Find the unique non-white color values
    unique_colors = np.unique(input_grid)
    non_white_colors = unique_colors[unique_colors != 0]

    # If there are not exactly two non-white colors, return the original grid
    # (or handle based on specific problem constraints if different)
    if len(non_white_colors) != 2:
        # This case might need refinement based on task requirements if inputs
        # can deviate from having exactly two non-background colors.
        # For now, assume valid inputs have exactly two or return original.
        return input_grid.copy()

    color1 = non_white_colors[0]
    color2 = non_white_colors[1]

    # Find all distinct objects in the input grid
    objects = find_objects(input_grid)

    # Initialize the output grid with the background color (0)
    output_grid = np.zeros_like(input_grid)

    # Iterate through the found objects and draw them with swapped colors
    for obj_color, obj_coords in objects:
        # Determine the swapped color
        swapped_color = -1 # Placeholder for invalid state
        if obj_color == color1:
            swapped_color = color2
        elif obj_color == color2:
            swapped_color = color1
        
        # Draw the object with the swapped color onto the output grid
        if swapped_color != -1:
            for r, c in obj_coords:
                output_grid[r, c] = swapped_color

    return output_grid