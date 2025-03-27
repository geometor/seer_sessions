```python
import numpy as np
from collections import deque

"""
Identify closed regions ("containers") made of gray (5) pixels. 
For each container, find if there is exactly one distinct, non-white (0), non-gray (5) colored object adjacent to its exterior boundary. 
If such a unique adjacent object ("filler source") exists:
1. Fill the interior area enclosed by the gray container with the color of the filler source.
2. Remove the filler source object by replacing its pixels with white (0).
Objects not involved in this interaction remain unchanged. Adjacency includes diagonals.
"""

def find_connected_components(grid, target_colors=None, ignore_colors=None):
    """
    Finds all connected components of specified colors in the grid.

    Args:
        grid (np.array): The input grid.
        target_colors (set, optional): Set of colors to find components for. 
                                        If None, finds components for all colors.
        ignore_colors (set, optional): Set of colors to ignore during traversal.

    Returns:
        list: A list of tuples, where each tuple is (color, set_of_coords).
              set_of_coords contains (row, col) tuples for the component.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    components = []

    if ignore_colors is None:
        ignore_colors = set()

    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            
            # Skip if visited, ignored color, or not a target color (if specified)
            if visited[r, c] or \
               color in ignore_colors or \
               (target_colors is not None and color not in target_colors):
                continue

            component_coords = set()
            q = deque([(r, c)])
            visited[r, c] = True
            component_coords.add((r, c))

            while q:
                row, col = q.popleft()

                # Check 8 neighbors (including diagonals)
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        
                        nr, nc = row + dr, col + dc

                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and \
                           grid[nr, nc] == color and \
                           color not in ignore_colors:
                            
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            component_coords.add((nr, nc))
            
            if component_coords:
                components.append((color, component_coords))

    return components

def get_neighbors(r, c, rows, cols, include_diagonal=True):
    """Gets valid neighbor coordinates."""
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            if not include_diagonal and abs(dr) + abs(dc) > 1:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbors.append((nr, nc))
    return neighbors

def find_interior(grid, container_coords):
    """
    Finds the interior pixels enclosed by a container.
    Uses flood fill from the grid borders to identify exterior pixels.
    """
    rows, cols = grid.shape
    exterior_visited = np.zeros_like(grid, dtype=bool)
    q = deque()

    # Add border cells that are not part of the container to the queue
    for r in range(rows):
        for c in [0, cols - 1]:
            if (r, c) not in container_coords and not exterior_visited[r, c]:
                q.append((r, c))
                exterior_visited[r, c] = True
    for c in range(cols):
        for r in [0, rows - 1]:
             if (r, c) not in container_coords and not exterior_visited[r, c]:
                q.append((r, c))
                exterior_visited[r, c] = True

    # Flood fill from borders (4-connectivity is sufficient for finding exterior reachable area)
    while q:
        r, c = q.popleft()
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and \
               not exterior_visited[nr, nc] and \
               (nr, nc) not in container_coords:
                exterior_visited[nr, nc] = True
                q.append((nr, nc))

    # Interior points are those not visited by exterior flood fill and not part of the container
    interior_coords = set()
    for r in range(rows):
        for c in range(cols):
            if not exterior_visited[r, c] and (r, c) not in container_coords:
                interior_coords.add((r, c))
                
    # Check if interior is empty or contains only gray pixels - means it wasn't a proper enclosure
    is_valid_enclosure = False
    for r,c in interior_coords:
        if grid[r,c] != 5: # If any non-gray pixel is inside
            is_valid_enclosure = True
            break
            
    if not is_valid_enclosure:
         return set() # Return empty set if not a valid enclosure

    return interior_coords


def transform(input_grid):
    """
    Applies the container-filler transformation rule.
    1. Finds gray containers and potential filler objects.
    2. For each container, identifies its interior.
    3. Finds unique filler objects adjacent to the container's exterior.
    4. If exactly one unique filler is found, fills the interior with its color 
       and removes the filler object (sets to white).
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    
    # 1. Identify potential containers (gray=5) and fillers (not white=0, not gray=5)
    all_components = find_connected_components(input_grid)
    
    containers = []
    potential_fillers = []
    filler_map = {} # Map coord -> filler index for quick lookup
    
    for i, (color, coords) in enumerate(all_components):
        if color == 5:
            containers.append((color, coords))
        elif color != 0:
            potential_fillers.append({'id': i, 'color': color, 'coords': coords})
            for coord in coords:
                filler_map[coord] = i # Store the component id for this coord

    # Process each container
    for _, container_coords in containers:
        
        # 2. Determine interior pixels (if any)
        interior_pixels = find_interior(input_grid, container_coords)
        if not interior_pixels: # Skip if no valid interior found
            continue

        # 3. Find adjacent filler objects to the *exterior* boundary
        adjacent_filler_ids = set()
        exterior_boundary_pixels = set()

        for r, c in container_coords:
            is_exterior_boundary = False
            for nr, nc in get_neighbors(r, c, rows, cols, include_diagonal=True):
                 # If neighbor is outside the container (not gray) and not interior, it's exterior adjacent
                 if (nr, nc) not in container_coords and (nr, nc) not in interior_pixels:
                     is_exterior_boundary = True
                     # Check if this exterior neighbor belongs to a potential filler
                     if (nr, nc) in filler_map:
                         adjacent_filler_ids.add(filler_map[(nr, nc)])
            if is_exterior_boundary:
                 exterior_boundary_pixels.add((r,c)) # Keep track for potential debugging

        # 4. Check condition: exactly one unique adjacent filler
        if len(adjacent_filler_ids) == 1:
            filler_id = list(adjacent_filler_ids)[0]
            
            # Find the actual filler object data
            unique_filler = None
            for filler in potential_fillers:
                if filler['id'] == filler_id:
                    unique_filler = filler
                    break
            
            if unique_filler:
                filler_color = unique_filler['color']
                filler_coords = unique_filler['coords']
                
                # 5a. Fill interior in output grid
                for r_int, c_int in interior_pixels:
                    output_grid[r_int, c_int] = filler_color
                    
                # 5b. Remove filler source in output grid
                for r_fill, c_fill in filler_coords:
                    output_grid[r_fill, c_fill] = 0 # Set to white

    return output_grid
```