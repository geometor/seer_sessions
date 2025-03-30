import numpy as np
from collections import deque

"""
Colors white (0) background pixels based on their proximity to distinct maroon (9) rectangular objects using 8-directional (Chebyshev) distance.
- Finds all distinct maroon objects (4-directional connectivity).
- Performs a multi-source Breadth-First Search (BFS) starting simultaneously from all maroon pixels.
- Calculates the shortest distance from each grid cell to the nearest maroon object(s).
- Tracks the set of unique maroon object IDs that are equidistant at the shortest distance.
- Colors originally white pixels:
    - Green (3) if closest to exactly one maroon object.
    - Blue (1) if equidistant from multiple maroon objects.
- Maroon pixels remain maroon (9).
- White pixels unreachable by the BFS (infinitely far) remain white (0).
"""

def find_objects(grid, color_val):
    """
    Finds connected components of a specific color in the grid using 4-directional adjacency.
    
    Args:
        grid (np.array): The input grid.
        color_val (int): The color value to find objects of.

    Returns:
        tuple: A tuple containing:
            - list: A list of objects, where each object is a set of (row, col) tuples.
            - dict: A dictionary mapping each pixel coordinate (row, col) belonging 
                    to an object to its unique object ID (1-based integer).
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    pixel_to_object_id = {}
    object_id_counter = 0

    for r in range(height):
        for c in range(width):
            # Start BFS if we find a pixel of the target color that hasn't been visited
            if grid[r, c] == color_val and not visited[r, c]:
                object_id_counter += 1
                current_object_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True
                
                while q:
                    row, col = q.popleft()
                    # Add pixel to the current object and map it to the object ID
                    current_object_pixels.add((row, col))
                    pixel_to_object_id[(row, col)] = object_id_counter
                    
                    # Explore 4-directional neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds, color, and visited status
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] == color_val and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                # Add the completed object to the list
                if current_object_pixels:
                    objects.append(current_object_pixels)
                    
    return objects, pixel_to_object_id

def transform(input_grid):
    """
    Transforms the input grid based on proximity to maroon objects.
    
    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed output grid.
    """
    input_arr = np.array(input_grid, dtype=int)
    height, width = input_arr.shape
    # Initialize output grid as a copy of the input
    output_grid = input_arr.copy() 

    # 1. Identify maroon objects and map pixels to object IDs
    maroon_objects, pixel_to_object_id = find_objects(input_arr, 9)
    
    # If there are no maroon objects, return the original grid
    if not maroon_objects: 
        return output_grid.tolist()

    # 2. Initialize helper grids for BFS
    # Distance grid: stores shortest distance (Chebyshev) to any maroon object
    distance = np.full((height, width), np.inf, dtype=float)
    # Sources grid: stores sets of object IDs for the closest object(s)
    sources = np.empty((height, width), dtype=object)
    for r in range(height):
        for c in range(width):
            sources[r, c] = set() # Initialize each cell with an empty set

    # 3. Initialize BFS queue with all maroon pixels
    queue = deque()
    for r in range(height):
        for c in range(width):
            if input_arr[r, c] == 9:
                obj_id = pixel_to_object_id[(r, c)]
                distance[r, c] = 0.0
                sources[r, c] = {obj_id} # Source is the object itself
                queue.append((r, c))

    # 4. Perform Multi-Source BFS (using 8 directions for distance)
    # Define 8 directions (including diagonals)
    directions = [(dr, dc) for dr in [-1, 0, 1] for dc in [-1, 0, 1] if not (dr == 0 and dc == 0)]

    while queue:
        r, c = queue.popleft()
        current_dist = distance[r, c]
        current_sources = sources[r, c]
        
        # Explore 8 neighbors
        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            # Check if neighbor is within grid bounds
            if 0 <= nr < height and 0 <= nc < width:
                # Calculate distance to neighbor (always +1 in Chebyshev)
                new_dist = current_dist + 1.0
                
                # If we found a shorter path to this neighbor
                if new_dist < distance[nr, nc]:
                    distance[nr, nc] = new_dist
                    # Replace sources with sources from the current path
                    sources[nr, nc] = current_sources.copy() 
                    queue.append((nr, nc)) # Add neighbor to queue
                # If we found another path of the same minimum distance
                elif new_dist == distance[nr, nc]:
                    # Add sources from the current path to the neighbor's sources
                    # Important: Only update if the sources are different to potentially avoid cycles
                    # although BFS structure largely prevents infinite loops here.
                    # Check if current_sources is already fully contained within sources[nr, nc]
                    if not current_sources.issubset(sources[nr, nc]):
                        sources[nr, nc].update(current_sources)
                        # No need to re-add to queue, as shortest distance is already known.
                        # Any further paths reaching this neighbor will either be longer,
                        # or if equal, will also update sources.

    # 5. Color the output grid based on the calculated distances and sources
    for r in range(height):
        for c in range(width):
            # Only modify originally white pixels that were reached by the BFS
            if input_arr[r, c] == 0 and distance[r, c] != np.inf:
                num_sources = len(sources[r, c])
                if num_sources == 1:
                    output_grid[r, c] = 3 # Green for single closest object
                elif num_sources > 1:
                    output_grid[r, c] = 1 # Blue for multiple equidistant objects
            # Pixels that were originally maroon (9) or were white (0) but unreachable 
            # (distance == inf) retain their original color (already set in output_grid copy).

    # Convert final numpy array back to list of lists
    return output_grid.tolist()