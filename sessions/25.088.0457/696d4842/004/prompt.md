
Previous Code:
```python
import numpy as np
from collections import deque
import heapq # For potential priority queue in distance calculation, though BFS is sufficient

"""
Identifies seeds (single non-white pixels) and shapes (connected components > 1 pixel of the same non-white color, 4-way connected).
For each shape, determines the closest seed based on the shortest path distance through adjacent (8-way) white pixels.
For each shape and its assigned closest seed, performs a BFS starting from the seed through adjacent (8-way) white pixels.
Colors all visited white pixels from this BFS that are also adjacent (8-way) to the associated shape with the color of the seed.
"""

def find_objects(grid):
    """
    Finds connected components of non-background pixels (color != 0).
    Classifies them as shapes (size > 1, 4-way connected) or seeds (size == 1).

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
    
    # 4-way neighbors for defining object connectivity
    neighbors_4 = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    for r in range(H):
        for c in range(W):
            if grid[r, c] != 0 and (r, c) not in visited:
                color = grid[r, c]
                component_coords = set()
                q = deque([(r, c)])
                visited.add((r, c))
                component_coords.add((r, c))
                
                # BFS to find the connected component (4-connectivity)
                while q:
                    curr_r, curr_c = q.popleft()
                    for dr, dc in neighbors_4:
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

def bfs_shortest_distance(grid, start_coord, target_coords_set):
    """
    Calculates the shortest path distance from start_coord to any coord in 
    target_coords_set, moving only through adjacent (8-way) white pixels (0).
    The distance is the number of white pixels in the path.

    Args:
        grid (np.array): The input grid.
        start_coord (tuple): The (r, c) of the seed pixel.
        target_coords_set (set): A set of (r, c) tuples representing the target shape.

    Returns:
        int: The shortest distance (number of white steps), or float('inf') if unreachable.
    """
    H, W = grid.shape
    neighbors_8 = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    
    # Start BFS from adjacent white cells to the seed
    queue = deque()
    visited_white = set() # Keep track of visited white cells to avoid cycles

    # Find initial white neighbors of the seed
    start_r, start_c = start_coord
    for dr, dc in neighbors_8:
        nr, nc = start_r + dr, start_c + dc
        if 0 <= nr < H and 0 <= nc < W:
            # If neighbor is the target shape, distance is 0 white steps
            if (nr, nc) in target_coords_set:
                 return 0 # Directly adjacent
            # If neighbor is white, add to queue with distance 1
            if grid[nr, nc] == 0 and (nr, nc) not in visited_white:
                queue.append(((nr, nc), 1)) # (coord, distance)
                visited_white.add((nr, nc))

    # Perform BFS
    while queue:
        (curr_r, curr_c), dist = queue.popleft()

        # Check neighbors of the current white cell
        for dr, dc in neighbors_8:
            nr, nc = curr_r + dr, curr_c + dc
            if 0 <= nr < H and 0 <= nc < W:
                # If neighbor is part of the target shape, return current distance
                if (nr, nc) in target_coords_set:
                    return dist 
                
                # If neighbor is white and not visited, add to queue
                if grid[nr, nc] == 0 and (nr, nc) not in visited_white:
                    visited_white.add((nr, nc))
                    queue.append(((nr, nc), dist + 1))

    # Target shape not reachable via white path
    return float('inf')

def transform(input_grid):
    """
    Transforms the input grid by coloring white pixels adjacent to shapes
    based on the closest seed reachable via a white path.
    """
    H, W = input_grid.shape
    output_grid = np.copy(input_grid)
    neighbors_8 = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    # 1. Identify Objects
    shapes, seeds = find_objects(input_grid)

    if not shapes or not seeds:
        return output_grid # No transformation possible if no shapes or no seeds

    # Store shape info with indices for easy mapping
    shape_data = [{'coords': coords, 'color': color, 'id': i} for i, (coords, color) in enumerate(shapes)]
    seed_data = [{'coord': coord, 'color': color, 'id': i} for i, (coord, color) in enumerate(seeds)]

    # 2. Determine Closest Seed for Each Shape
    shape_to_closest_seed = {} # {shape_id: {'seed_id': id, 'distance': dist}}
    for shape in shape_data:
        min_dist = float('inf')
        closest_seed_id = -1
        
        for seed in seed_data:
            # Calculate distance from this seed to the current shape
            distance = bfs_shortest_distance(input_grid, seed['coord'], shape['coords'])
            
            # Update closest seed if this one is closer
            if distance < min_dist:
                min_dist = distance
                closest_seed_id = seed['id']
            # Optional: Add tie-breaking logic here if needed (e.g., seed index)
        
        # Store the result if a reachable seed was found
        if closest_seed_id != -1:
            shape_to_closest_seed[shape['id']] = {'seed_id': closest_seed_id, 'distance': min_dist}

    # 3. Color Adjacent White Pixels
    pixels_to_color = {} # {(r, c): color} - Store potential colorings, handle overlaps later if needed (e.g., closest point) - current logic overwrites

    for shape_id, assignment in shape_to_closest_seed.items():
        seed_id = assignment['seed_id']
        
        # Get the relevant shape and seed info
        target_shape = next(s for s in shape_data if s['id'] == shape_id)
        assigned_seed = next(s for s in seed_data if s['id'] == seed_id)
        
        start_coord = assigned_seed['coord']
        fill_color = assigned_seed['color']
        target_shape_coords = target_shape['coords']

        # Perform BFS from the assigned seed, exploring only white pixels (8-way)
        queue = deque([start_coord])
        # visited_bfs includes the seed and all reachable cells (white or not)
        # to prevent cycles and redundant exploration in this specific BFS run.
        visited_bfs = {start_coord} 
        # reachable_white_pixels stores only the white pixels found by this BFS
        reachable_white_pixels = set() 

        while queue:
            r, c = queue.popleft()

            # Explore 8-way neighbors
            for dr, dc in neighbors_8:
                nr, nc = r + dr, c + dc

                if 0 <= nr < H and 0 <= nc < W and (nr, nc) not in visited_bfs:
                    visited_bfs.add((nr, nc))
                    # If neighbor is white, add to queue and track it
                    if input_grid[nr, nc] == 0:
                        reachable_white_pixels.add((nr, nc))
                        queue.append((nr, nc))
                    # If neighbor is colored (part of a shape or another seed),
                    # we visit it but don't add to the white pixel set or queue
                    # (as the path must be through white).
        
        # Identify which of the reachable white pixels are adjacent to the target shape
        for wr, wc in reachable_white_pixels:
            is_adjacent_to_target_shape = False
            for dr, dc in neighbors_8:
                nnr, nnc = wr + dr, wc + dc
                # Check bounds and if neighbor is in the target shape's coordinates
                if 0 <= nnr < H and 0 <= nnc < W and (nnr, nnc) in target_shape_coords:
                    is_adjacent_to_target_shape = True
                    break # Found adjacency
            
            if is_adjacent_to_target_shape:
                # Store the pixel and its color. If multiple seeds claim the same pixel,
                # the last one processed will win. A more complex rule might be needed
                # for ties (e.g., closest seed overall). Current logic implies processing order matters.
                 pixels_to_color[(wr, wc)] = fill_color
                 # Instead of direct assignment, collect first:
                 # if (wr, wc) not in pixels_to_color:
                 #    pixels_to_color[(wr, wc)] = []
                 # pixels_to_color[(wr, wc)].append({'seed_id': seed_id, 'color': fill_color, 'dist_from_seed': ?})
                 # Then resolve conflicts after all BFS runs. 
                 # Let's stick to the simpler overwrite logic for now based on the NLP.

    # Apply the collected color changes
    for (r, c), color in pixels_to_color.items():
        output_grid[r, c] = color
        
    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 6 6 6 6 6 6 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 4 4 4 4 6 6 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0
0 4 3 3 3 3 3 4 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 4 3 4 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 3 4 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 8 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0 8 6 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 6 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 6 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 6 8 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 6 8 0 0 0 0 0 0 0 0
0 0 0 8 6 6 6 6 6 6 6 8 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 62
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 31.0

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 4 4 4 4 4 0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 0 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 4 4 4 4 4 4 4 4 4 4 4 2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 6 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 6 6 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 4 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 4 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 4 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 4 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 4 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 4 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 4 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 4 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 4 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 4 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 4 4 4 4 4 4 2 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 6 6 6 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 6 1 1 1 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 6 6 1 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 6 1 6 6 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 6 1 1 1 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 6 6 6 6 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 80
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 17.77777777777777

## Example 3:
Input:
```
0 0 0 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 4 4 4 4 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 3 3 3 0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0
0 0 6 6 6 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 4 4 4 4 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 6 6 6 6 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 6 4 4 4 6 0 6 6 6 0 0 0 0 0 0 0 0 0 0
0 6 6 6 4 6 0 6 4 6 0 0 0 0 0 0 0 0 0 0
0 0 0 6 4 6 6 6 4 6 0 0 0 0 0 0 0 0 0 0
0 0 0 6 4 4 4 4 4 6 0 0 0 0 0 0 0 0 0 0
0 0 0 6 6 6 6 6 6 6 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0
0 0 8 3 3 3 3 3 3 3 8 0 0 0 0 0 0 0 0 0
0 0 8 8 8 8 8 8 8 3 8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 3 8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 3 8 8 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 3 3 3 8 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 8 8 8 8 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 78
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 39.0
