```python
import numpy as np
from collections import Counter, deque

def find_connected_objects(grid, target_color):
    """
    Finds all connected objects of a specific color in a grid using BFS.

    Args:
        grid (np.array): The input grid.
        target_color (int): The color of the objects to find.

    Returns:
        list: A list of objects, where each object is represented as a list
              of (row, col) coordinate tuples.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            # If we find a pixel of the target color that hasn't been visited yet,
            # start a BFS to find its connected component (object).
            if grid[r, c] == target_color and not visited[r, c]:
                current_object_coords = []
                q = deque([(r, c)])
                visited[r, c] = True

                while q:
                    row, col = q.popleft()
                    current_object_coords.append((row, col))

                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc

                        # Check boundaries and if the neighbor is the target color and not visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == target_color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                if current_object_coords:
                    objects.append(current_object_coords)
    
    return objects

def transform(input_grid):
    """
    Transforms the input grid by performing the following steps:
    1. Identify all unique non-background pixel colors (0 is background).
    2. Count the frequency of each non-background color.
    3. Determine the color(s) with the highest frequency ('primary' color(s)).
    4. Find all contiguous objects composed of the primary color(s).
    5. Identify the largest size among these primary color objects.
    6. Create an output grid containing only the pixels belonging to the largest object(s) 
       of the primary color(s), preserving their original color. All other pixels are 
       set to the background color (0).
    """
    input_grid_np = np.array(input_grid)
    rows, cols = input_grid_np.shape
    output_grid = np.zeros_like(input_grid_np) # Initialize output with background color

    # 1. & 2. Count frequencies of non-background colors
    pixels = input_grid_np.flatten()
    non_background_pixels = pixels[pixels != 0]
    
    if len(non_background_pixels) == 0:
        # If the input grid is empty or only background, return the empty grid
        return output_grid.tolist()
        
    color_counts = Counter(non_background_pixels)
    
    # 3. Determine the primary color(s) - highest frequency
    max_freq = 0
    primary_colors = []
    if color_counts: # Check if there are any non-background colors
        max_freq = max(color_counts.values())
        primary_colors = [color for color, count in color_counts.items() if count == max_freq]

    # If no primary color identified (e.g., only background color present), return zero grid
    if not primary_colors:
         return output_grid.tolist()

    # 4. Find all objects of the primary color(s)
    all_primary_objects = []
    for color in primary_colors:
        objects_of_color = find_connected_objects(input_grid_np, color)
        all_primary_objects.extend(objects_of_color) # Store objects as lists of coordinates

    # If no objects found for any primary color, return zero grid
    if not all_primary_objects:
        return output_grid.tolist()

    # 5. Identify the maximum object size
    max_object_size = 0
    for obj in all_primary_objects:
        max_object_size = max(max_object_size, len(obj))

    # 6. Filter and create the output grid
    for obj_coords in all_primary_objects:
        if len(obj_coords) == max_object_size:
            # Keep this object - copy its pixels to the output grid
            for r, c in obj_coords:
                # We already know the color from the primary_colors list, 
                # or we can just grab it from the input grid
                output_grid[r, c] = input_grid_np[r, c] 

    return output_grid.tolist()
```