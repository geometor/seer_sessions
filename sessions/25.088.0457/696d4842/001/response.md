```python
import numpy as np
from collections import deque

"""
Identify distinct shapes (connected components > 1 pixel) and seeds (single pixels) in the input grid.
For each seed pixel, perform a search (like BFS) outwards through adjacent white (0) pixels.
Determine which shapes are reachable from the seed via this white-pixel path.
For each reachable shape, identify all white pixels that were visited during the search AND are adjacent (8-way) to that specific shape.
Fill these identified adjacent white pixels with the color of the seed pixel in the output grid.
"""

def find_objects(grid):
    """
    Finds connected components of non-background pixels.
    Classifies them as shapes (size > 1) or seeds (size == 1).

    Args:
        grid (np.array): Input grid.

    Returns:
        tuple: (shapes, seeds)
            shapes: list of tuples [(coords_set, color)], where coords_set is a set of (r, c) tuples.
            seeds: list of tuples [(coord, color)], where coord is an (r, c) tuple.
    """
    H, W = grid.shape
    visited = set()
    shapes = []
    seeds = []
    
    for r in range(H):
        for c in range(W):
            if grid[r, c] != 0 and (r, c) not in visited:
                color = grid[r, c]
                component_coords = set()
                q = deque([(r, c)])
                visited.add((r, c))
                component_coords.add((r, c))
                
                # BFS to find the connected component (4-connectivity for object definition)
                while q:
                    curr_r, curr_c = q.popleft()
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        if 0 <= nr < H and 0 <= nc < W and \
                           (nr, nc) not in visited and grid[nr, nc] == color:
                            visited.add((nr, nc))
                            component_coords.add((nr, nc))
                            q.append((nr, nc))
                            
                if len(component_coords) == 1:
                    # It's a seed if it's a single pixel
                    seeds.append(((r, c), color))
                else:
                    # It's a shape if it has more than one pixel
                    shapes.append((component_coords, color))
                    
    return shapes, seeds

def transform(input_grid):
    """
    Transforms the input grid based on connectivity between seeds and shapes.

    1. Finds all shapes and seeds.
    2. For each seed:
        a. Performs BFS on white pixels starting from the seed.
        b. Identifies shapes reachable via this white path.
        c. Identifies white pixels visited AND adjacent to reachable shapes.
        d. Fills those white pixels with the seed's color.

    Args:
        input_grid (np.array): The input grid.

    Returns:
        np.array: The transformed output grid.
    """
    # Initialize output grid as a copy of the input
    output_grid = np.copy(input_grid)
    H, W = input_grid.shape

    # Find shapes and seeds
    shapes, seeds = find_objects(input_grid)
    
    # Create a quick lookup for all coordinates belonging to any shape
    all_shape_coords = set()
    for shape_coords, _ in shapes:
        all_shape_coords.update(shape_coords)

    # Define 8-way neighbors
    neighbors_8 = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    # Process each seed
    for seed_coord, seed_color in seeds:
        
        # BFS starting from the seed, moving only through white pixels (0)
        queue = deque([seed_coord])
        # visited_bfs includes the starting seed and all visited white cells in this specific BFS
        visited_bfs = set([seed_coord]) 
        reachable_white_pixels = set() # Store white pixels reached from this seed
        connected_shape_indices = set() # Store indices of shapes connected via white path

        while queue:
            r, c = queue.popleft()

            # Explore 8 neighbors
            for dr, dc in neighbors_8:
                nr, nc = r + dr, c + dc

                if 0 <= nr < H and 0 <= nc < W:
                    # Check if neighbor is already visited in this BFS
                    if (nr, nc) not in visited_bfs:
                        neighbor_val = input_grid[nr, nc]
                        
                        # If neighbor is white, add to queue and track it
                        if neighbor_val == 0:
                            visited_bfs.add((nr, nc))
                            queue.append((nr, nc))
                            reachable_white_pixels.add((nr, nc))
                        
                        # If neighbor is part of *any* shape, mark that shape as connected
                        elif (nr, nc) in all_shape_coords:
                           # We don't add the shape pixel itself to visited_bfs 
                           # or the queue, but we note the connection.
                           # Find which shape it belongs to
                           for i, (shape_coords, _) in enumerate(shapes):
                               if (nr, nc) in shape_coords:
                                   connected_shape_indices.add(i)
                                   break # Found the shape index


        # Now, identify the actual pixels to fill for this seed
        pixels_to_fill_for_this_seed = set()
        for shape_idx in connected_shape_indices:
            current_shape_coords = shapes[shape_idx][0]
            
            # Check every white pixel reached by the BFS
            for wr, wc in reachable_white_pixels:
                # Is this white pixel adjacent to the *current* connected shape?
                is_adjacent_to_current_shape = False
                for dr, dc in neighbors_8:
                    nnr, nnc = wr + dr, wc + dc
                    # Check bounds and if neighbor is in the current shape's coordinates
                    if 0 <= nnr < H and 0 <= nnc < W and (nnr, nnc) in current_shape_coords:
                        is_adjacent_to_current_shape = True
                        break # Found adjacency, no need to check other neighbors
                
                if is_adjacent_to_current_shape:
                    pixels_to_fill_for_this_seed.add((wr, wc))

        # Fill the identified pixels in the output grid with the seed's color
        for fr, fc in pixels_to_fill_for_this_seed:
            output_grid[fr, fc] = seed_color

    return output_grid
```