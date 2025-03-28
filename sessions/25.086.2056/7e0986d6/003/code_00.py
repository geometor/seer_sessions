"""
Identify the non-background color that forms the smallest connected object (by pixel count). 
Replace all pixels of this identified color with the background color (white, 0).
If multiple colors share the same smallest object size, choose the color with the lowest numerical value as the tie-breaker.
Connectedness is defined by sharing an edge (up, down, left, right), not just a corner.
"""

import numpy as np
from collections import defaultdict

BACKGROUND_COLOR = 0

def find_objects(grid, color):
    """
    Finds all connected objects of a specific color in the grid.

    Args:
        grid (np.array): The input grid.
        color (int): The color of the objects to find.

    Returns:
        list of sets: A list where each set contains the (row, col) tuples of pixels belonging to one object.
    """
    rows, cols = grid.shape
    visited = set()
    objects = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and (r, c) not in visited:
                # Start a Breadth-First Search (BFS) for a new object
                current_object = set()
                q = [(r, c)]
                visited.add((r, c))
                
                while q:
                    row, col = q.pop(0)
                    current_object.add((row, col))

                    # Check neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        
                        # Check bounds and if neighbor is the correct color and not visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            q.append((nr, nc))
                
                objects.append(current_object)
                
    return objects

def transform(input_grid):
    """
    Identifies the non-background color forming the smallest object and replaces 
    all occurrences of that color with the background color (0). Uses color value
    as a tie-breaker if minimum object sizes are equal.

    Args:
        input_grid (list of lists): A 2D list representing the input grid.

    Returns:
        list of lists: A 2D list representing the transformed grid.
    """
    # Convert input list of lists to a numpy array
    input_array = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy
    output_grid = np.copy(input_array)
    
    # Find unique non-background colors
    unique_colors = np.unique(input_array)
    non_background_colors = [color for color in unique_colors if color != BACKGROUND_COLOR]

    # If there are fewer than two non-background colors, no change is needed
    if len(non_background_colors) < 1: # Changed from < 2 because even with one color, we might need to process it if it has the smallest object
         return output_grid.tolist()

    min_object_sizes = {} # Dictionary to store {color: min_object_size}

    # Iterate through each non-background color
    for color in non_background_colors:
        # Find all objects of the current color
        objects = find_objects(input_array, color)
        
        # If no objects of this color are found (shouldn't happen if color is present), skip
        if not objects:
            continue
            
        # Calculate the size of each object and find the minimum size for this color
        min_size_for_color = min(len(obj) for obj in objects)
        min_object_sizes[color] = min_size_for_color

    # If min_object_sizes is empty (no non-background colors found objects), return original
    if not min_object_sizes:
         return output_grid.tolist()

    # Find the overall minimum object size among all colors
    overall_min_size = min(min_object_sizes.values())

    # Find all colors that share this overall minimum size
    colors_with_min_size = [color for color, size in min_object_sizes.items() if size == overall_min_size]

    # Apply tie-breaking rule: choose the color with the lowest numerical value
    target_color = min(colors_with_min_size)

    # Replace all occurrences of the target_color with the BACKGROUND_COLOR
    output_grid[output_grid == target_color] = BACKGROUND_COLOR

    # Convert the result back to a list of lists
    return output_grid.tolist()