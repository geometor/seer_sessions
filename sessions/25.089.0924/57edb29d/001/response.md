Warning: Response generation stopped. Finish Reason: MAX_TOKENS (2)
Partial text available:
---
```python
import numpy as np
from collections import defaultdict, Counter

"""
Transforms the input grid based on identifying an inner pattern color within multiple host objects,
selecting a specific host object based on the inner pattern color via a fixed mapping,
and extracting/recoloring the pattern from the selected host object's bounding box.

1. Find the background color (most frequent).
2. Find the unique "inner pattern color" (C_inner) by identifying the non-background color adjacent
   to the most *diverse* set of other non-background colors (using 8-way adjacency).
3. Determine the "selected host color" (h_selected) based on C_inner using the map:
   {5: 3, 7: 8, 6: 1}.
4. Locate the specific object (O_selected) of color h_selected (defined by 4-way contiguous pixels)
   that contains C_inner pixels within its bounding box.
5. Extract the subgrid corresponding to O_selected's bounding box.
6. Create the output grid with the dimensions of the bounding box, initially filled with h_selected.
7. Populate the output grid by copying pixels matching C_inner from the input subgrid; all other
   pixels remain h_selected.
"""

def _get_neighbors(r, c, height, width, connectivity=8):
    """
    Gets valid neighbor coordinates for a given cell (r, c).

    Args:
        r (int): Row index of the cell.
        c (int): Column index of the cell.
        height (int): Grid height.
        width (int): Grid width.
        connectivity (int): 4 or 8 for neighbor definition.

    Returns:
        list: A list of tuples representing valid neighbor coordinates (row, col).
    """
    neighbors = []
    if connectivity == 8:
        moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    elif connectivity == 4:
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    else:
        raise ValueError("Connectivity must be 4 or 8")
        
    for dr, dc in moves:
        nr, nc = r + dr, c + dc
        if 0 <= nr < height and 0 <= nc < width:
            neighbors.append((nr, nc))
    return neighbors

def _find_objects(grid, color_to_find):
    """
    Finds all contiguous objects (based on 4-way adjacency) of a specific color using BFS.
    Calculates the bounding box for each object found.

    Args:
        grid (np.array): The input grid.
        color_to_find (int): The color of the objects to find.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              and contains 'coords' (a set of (row, col) tuples) and
              'bbox' (a tuple: min_r, min_c, max_r, max_c).
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(height):
        for c in range(width):
            # Start BFS if we find a pixel of the target color that hasn't been visited
            if grid[r, c] == color_to_find and not visited[r, c]:
                obj_coords = set()
                q = [(r, c)] # Queue for BFS
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c
                
                head = 0 # Use index as queue pointer for efficiency
                while head < len(q):
                    row, col = q[head]
                    head += 1
                    
                    obj_coords.add((row, col))
                    # Update bounding box dynamically
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Explore 4-way neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]: 
                        nr, nc = row + dr, col + dc
                        # Check bounds, color match, and visited status
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] == color_to_find and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                # Store the found object and its bounding box
                if obj_coords:
                    bounding_box = (min_r, min_c, max_r, max_c)
                    objects.append({'coords': obj_coords, 'bbox': bounding_box})
    return objects


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    input_grid = np.array(input_grid, dtype=int)
    height, width = input_grid.shape

    # Step 1: Find background color (most frequent color)
    colors, counts = np.unique(input_grid, return_counts=True)
    if len(colors) == 1: # Handle grids with only one color
        # This case might need specific handling depending on task requirements,
        # but for this task, it likely implies an error or an unexpected input.
        # Returning an empty grid or the input might be options.
        # Based on the problem structure, assume valid inputs have patterns.
         print("Warning: Input grid has only one color.")
         # Returning a minimal grid based on the single color object might be an interpretation
         single_color = colors[0]
         host_map_inv = {v: k for k, v in {5: 3, 7: 8, 6: 1}.items()} # Find potential inner color
         if single_color in host_map_inv:
              # Assume this single color object IS the output
               obj = _find_objects(input_grid, single_color)
               if obj:
                    min_r, min_c, max_r, max_c = obj[0]['bbox']
                    return input_grid[min_r:max_r+1, min_c:max_c+1].tolist()
         return [] # Return empty list if unsure how to handle


    background_color = colors[np.argmax(counts)]

    # Step 2: Find the inner pattern color (C_inner)
    # It's the non-background color adjacent to the most *different* non-background colors.
    adjacencies = defaultdict(set)

    for r in range(height):
        for c in range(width):
            center_color = input_grid[r, c]
            # Skip background pixels
            if center_color == background_color:
                continue
                
            # Check 8 neighbors
            for nr, nc in _get_neighbors(r, c, height, width, connectivity=8):
                neighbor_color = input_grid[nr, nc]
                # Consider adjacency only if neighbor is non-background and different color
                if neighbor_color != background_color and neighbor_color != center_color:
                    adjacencies[center_color].add(neighbor_color)
                    adjacencies[neighbor_color].add(center_color) # Record reverse adjacency too

    inner_pattern_color = -1
    max_diverse_adjacencies = -1

    # Determine which color has the most diverse adjacencies
    potential_inner_colors = sorted(list(adjacencies.keys())) # Sort for consistent tie-breaking (lowest color wins)
    for color in potential_inner_colors:
        num_adjacent_colors = len(adjacencies[color])
        if num_adjacent_colors > max_diverse_adjacencies:
             max_diverse_adjacencies = num_adjacent_colors
             inner_pattern_color = color
        # Tie-breaking: If counts are equal, the sorting ensures we keep the lowest color index.
        
    if inner_pattern_color == -1:

---
