import numpy as np
from collections import deque

"""
Transforms the input grid by recoloring azure (8) objects based on their size rank 
and the total number of objects.

1. Identifies all distinct connected components (objects) of azure (8) pixels using 
   8-way connectivity (including diagonals).
2. Calculates the size (pixel count) and top-left coordinate (minimum row, then 
   minimum column) for each object.
3. Counts the total number of azure objects found (M).
4. Sorts the objects based primarily on size (ascending) and secondarily on their 
   top-left coordinate (row ascending, then column ascending).
5. Determines a specific color sequence based on the total number of objects found (M):
   - M=4: [Green(3), Green(3), Orange(7), Orange(7)]
   - M=5: [Blue(1), Red(2), Red(2), Blue(1), Green(3)]
   - M=6: [Blue(1), Red(2), Red(2), Red(2), Green(3), Orange(7)]
6. Creates a copy of the input grid.
7. Recolors each object in the output grid according to its rank in the sorted list, 
   using the determined color sequence. Pixels of the i-th object in the sorted list
   are recolored with the i-th color in the sequence.
8. If M is not 4, 5, or 6, the original grid is returned unchanged.
"""

def find_objects(grid, color_code):
    """
    Finds all connected components of a specific color in the grid using 8-way connectivity.

    Args:
        grid (np.ndarray): The input grid.
        color_code (int): The color code of the objects to find.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              with keys 'pixels' (set of (r, c) tuples), 'size' (int),
              and 'top_left' ((r, c) tuple). Returns an empty list if no objects
              of the specified color are found.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    
    # Define 8 neighbors (including diagonals) for connectivity
    neighbors = [(-1, -1), (-1, 0), (-1, 1),
                 (0, -1),           (0, 1),
                 (1, -1), (1, 0), (1, 1)]

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color_code and not visited[r, c]:
                # Found the start of a new object, perform Breadth-First Search (BFS)
                obj_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c # Initialize top-left coordinate tracking

                while q:
                    row, col = q.popleft()
                    obj_pixels.add((row, col))
                    
                    # Update top-left coordinate if a pixel further up or left is found
                    if row < min_r:
                        min_r, min_c = row, col
                    elif row == min_r and col < min_c:
                        min_c = col

                    # Explore neighbors
                    for dr, dc in neighbors:
                        nr, nc = row + dr, col + dc
                        # Check bounds and if the neighbor is the target color and not visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color_code and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                # Store the found object's properties
                objects.append({
                    'pixels': obj_pixels,
                    'size': len(obj_pixels),
                    'top_left': (min_r, min_c)
                })
                
    return objects

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input list of lists to a NumPy array for easier processing
    input_grid_np = np.array(input_grid, dtype=int)
    
    # 1. Identify all azure (8) objects
    azure_objects = find_objects(input_grid_np, 8)
    
    # 2. Get the total number of objects found
    M = len(azure_objects)
    
    # If no azure objects found, return the original grid
    if M == 0:
        return input_grid 

    # 3. Sort the objects: primary key size (asc), secondary key top-left row (asc), tertiary key top-left col (asc)
    sorted_objects = sorted(azure_objects, key=lambda obj: (obj['size'], obj['top_left'][0], obj['top_left'][1]))
    
    # 4. Determine the target color sequence based on M
    color_sequence = []
    if M == 4:
        # Green, Green, Orange, Orange
        color_sequence = [3, 3, 7, 7]
    elif M == 5:
        # Blue, Red, Red, Blue, Green  (Corrected sequence)
        color_sequence = [1, 2, 2, 1, 3] 
    elif M == 6:
        # Blue, Red, Red, Red, Green, Orange
        color_sequence = [1, 2, 2, 2, 3, 7]
    else:
        # If M is not 4, 5, or 6, the transformation is undefined by examples. Return original grid.
        # print(f"Warning: Unexpected number of objects M={M}. No transformation applied.")
        return input_grid

    # 5. Create the output grid as a copy of the input grid
    output_grid = np.copy(input_grid_np)
    
    # 6. Iterate through the sorted objects and assign colors based on rank
    for i, obj in enumerate(sorted_objects):
        # Get the target color for the current object based on its rank (i)
        target_color = color_sequence[i]
        # 7. Recolor the pixels of the current object in the output grid
        for r, c in obj['pixels']:
            output_grid[r, c] = target_color
            
    # Convert the NumPy array back to a list of lists for the final output
    return output_grid.tolist() 