import numpy as np
from collections import Counter, defaultdict
import copy

def find_objects(grid, color):
    """
    Finds all contiguous objects of a specific color in the grid.

    Args:
        grid (np.array): The input grid.
        color (int): The color of the objects to find.

    Returns:
        list: A list of objects, where each object is represented by a set 
              of (row, col) tuples. Returns an empty list if the color 
              is not found.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                current_object = set()
                q = [(r, c)]
                visited[r, c] = True
                while q:
                    row, col = q.pop(0)
                    current_object.add((row, col))
                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                if current_object:
                    objects.append(current_object)
    return objects

def transform(input_grid):
    """
    Identifies the two non-background colors that form the fewest distinct 
    contiguous objects. Swaps all occurrences of these two colors in the grid. 
    The background color is assumed to be the most frequent color. If there 
    are fewer than two non-background colors, no changes are made.

    Args:
        input_grid (list of lists of int): The input grid.

    Returns:
        list of lists of int: The transformed grid.
    """
    
    # Convert input grid to a numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    output_array = np.copy(input_array)
    
    # Flatten the array to count color frequencies
    flat_array = input_array.flatten()
    
    # Count the occurrences of each color
    color_counts = Counter(flat_array)
    
    # If there are fewer than 3 unique colors (background + 2 others), 
    # no swap is possible/needed
    if len(color_counts) < 3:
        return output_array.tolist()
        
    # Find the most frequent color (background)
    background_color = color_counts.most_common(1)[0][0]
    
    # Identify non-background colors
    non_background_colors = [color for color in color_counts if color != background_color]

    # If there are fewer than 2 non-background colors after removing background,
    # no swap is possible/needed
    if len(non_background_colors) < 2:
         return output_array.tolist()

    # Count the number of distinct objects for each non-background color
    object_counts = {}
    for color in non_background_colors:
        objects = find_objects(input_array, color)
        object_counts[color] = len(objects)

    # Sort the non-background colors by their object count (ascending)
    # If object counts are tied, the original order (which depends on dict iteration order, 
    # roughly insertion order in modern Python) might influence the result, 
    # but it shouldn't affect the final swap as it's symmetrical.
    # A more robust tie-breaker could be added if needed, e.g., sorting by color value.
    sorted_colors_by_objects = sorted(object_counts.items(), key=lambda item: item[1])
    
    # Identify the two colors with the fewest objects
    color1, _ = sorted_colors_by_objects[0]
    color2, _ = sorted_colors_by_objects[1]
    
    # Iterate through the grid and swap the colors
    rows, cols = input_array.shape
    for r in range(rows):
        for c in range(cols):
            if input_array[r, c] == color1:
                output_array[r, c] = color2
            elif input_array[r, c] == color2:
                output_array[r, c] = color1
                
    # Return the transformed grid as a list of lists
    return output_array.tolist()