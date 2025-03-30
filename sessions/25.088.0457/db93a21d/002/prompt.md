
Previous Code:
```python
import numpy as np
from collections import deque

"""
Identifies distinct maroon (9) rectangular objects in the input grid. 
Calculates the shortest distance from each non-maroon pixel to the nearest maroon object(s), considering 8-directional adjacency (including diagonals).
Colors originally white (0) pixels based on this proximity:
- If a white pixel is closest to exactly one maroon object, it becomes green (3).
- If a white pixel is equidistant from multiple maroon objects, it becomes blue (1).
Maroon pixels remain unchanged. White pixels unreachable from any maroon object remain white.
"""

def find_objects(grid, color_val):
    """
    Finds connected components of a specific color in the grid.
    Uses BFS to find all pixels belonging to each object.
    Returns a list of objects, where each object is a set of (row, col) tuples,
    and a dictionary mapping each pixel coordinate to its object ID (1-based).
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    pixel_to_object_id = {}
    object_id_counter = 0

    for r in range(height):
        for c in range(width):
            if grid[r, c] == color_val and not visited[r, c]:
                object_id_counter += 1
                current_object_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True
                
                while q:
                    row, col = q.popleft()
                    current_object_pixels.add((row, col))
                    pixel_to_object_id[(row, col)] = object_id_counter
                    
                    # Check 4-directional neighbors for connectivity of the same color
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] == color_val and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
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
    output_grid = input_arr.copy() # Initialize output grid

    # 1. Identify maroon objects and map pixels to object IDs
    maroon_objects, pixel_to_object_id = find_objects(input_arr, 9)
    
    if not maroon_objects: # Handle case with no maroon objects
        return output_grid.tolist()

    # 2. Initialize helper grids for BFS
    # Distance grid: stores shortest distance to any maroon object
    distance = np.full((height, width), np.inf, dtype=float)
    # Sources grid: stores sets of object IDs for the closest object(s)
    sources = np.empty((height, width), dtype=object)
    for r in range(height):
        for c in range(width):
            sources[r, c] = set() # Initialize each cell with an empty set

    # 3. Initialize BFS queue with pixels adjacent to maroon objects
    queue = deque()
    
    # Define 8 directions for adjacency check
    directions = [(dr, dc) for dr in [-1, 0, 1] for dc in [-1, 0, 1] if not (dr == 0 and dc == 0)]

    for r in range(height):
        for c in range(width):
            if input_arr[r, c] == 0: # Consider only background pixels
                adjacent_maroon_ids = set()
                is_adjacent = False
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < height and 0 <= nc < width and input_arr[nr, nc] == 9:
                        is_adjacent = True
                        # Add the ID of the adjacent maroon object
                        adjacent_maroon_ids.add(pixel_to_object_id[(nr, nc)]) 
                
                if is_adjacent:
                    distance[r, c] = 1.0 # Distance for directly adjacent pixels is 1
                    sources[r, c] = adjacent_maroon_ids
                    queue.append(((r, c), 1.0)) # Add (coordinate, distance) to queue

    # 4. Perform BFS to calculate distances and sources for all reachable white pixels
    while queue:
        (r, c), d = queue.popleft()

        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            if 0 <= nr < height and 0 <= nc < width and input_arr[nr, nc] == 0:
                new_dist = d + 1.0
                
                # If we found a shorter path to this pixel
                if new_dist < distance[nr, nc]:
                    distance[nr, nc] = new_dist
                    sources[nr, nc] = sources[r, c].copy() # Inherit sources from the closer path
                    queue.append(((nr, nc), new_dist))
                # If we found another path of the same minimum distance
                elif new_dist == distance[nr, nc]:
                     # Check if the sources are different before updating and appending
                    if not sources[r,c].issubset(sources[nr,nc]):
                        sources[nr, nc].update(sources[r, c]) # Add sources from this new path
                        # No need to re-add to queue if distance hasn't changed, 
                        # but subsequent steps might need the updated source info.
                        # This is tricky; standard BFS usually doesn't re-queue on equal distance.
                        # However, source propagation requires considering equal paths.
                        # A simple approach is to just update sources. If a neighbor finds 
                        # *this* node later with the same distance, it will update its own sources correctly.

    # 5. Color the output grid based on the calculated sources
    for r in range(height):
        for c in range(width):
            # Only color originally white pixels that were reached
            if input_arr[r, c] == 0 and distance[r, c] != np.inf:
                num_sources = len(sources[r, c])
                if num_sources == 1:
                    output_grid[r, c] = 3 # Green for single source
                elif num_sources > 1:
                    output_grid[r, c] = 1 # Blue for multiple equidistant sources
            # Maroon pixels (9) and unreachable white pixels (0) remain unchanged

    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 9 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 9 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 9 9 9 9 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 9 9 9 9 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 9 9 9 9 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 9 9 9 9 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 9 9 9 9 9 9 0 0 0 0 0 0 0 0
0 0 0 0 0 0 9 9 9 9 9 9 0 0 0 0 0 0 0 0
0 0 0 0 0 0 9 9 9 9 9 9 0 0 0 0 0 0 0 0
0 0 0 0 0 0 9 9 9 9 9 9 0 0 0 0 0 0 0 0
0 0 0 0 0 0 9 9 9 9 9 9 0 0 0 0 0 0 0 0
0 0 0 0 0 0 9 9 9 9 9 9 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 9 9 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 9 9 3 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3
0 3 3 3 3 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3
0 0 1 1 0 0 0 0 0 0 0 0 0 3 3 9 9 9 9 3
0 0 1 1 0 0 0 0 0 0 0 0 0 3 3 9 9 9 9 3
0 0 1 1 0 0 0 0 0 0 0 0 0 3 3 9 9 9 9 3
0 0 1 3 3 3 3 3 3 3 3 3 3 3 3 9 9 9 9 3
0 0 1 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
0 0 1 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
0 0 1 3 3 3 9 9 9 9 9 9 3 3 3 1 1 1 1 0
0 0 1 3 3 3 9 9 9 9 9 9 3 3 3 1 1 1 1 0
0 0 1 3 3 3 9 9 9 9 9 9 3 3 3 1 1 1 1 0
0 0 1 3 3 3 9 9 9 9 9 9 3 3 3 1 1 1 1 0
0 0 1 3 3 3 9 9 9 9 9 9 3 3 3 1 1 1 1 0
0 0 1 3 3 3 9 9 9 9 9 9 3 3 3 1 1 1 1 0
0 0 1 3 3 3 3 3 3 3 3 3 3 3 3 1 1 1 1 0
0 0 1 3 3 3 3 3 3 3 3 3 3 3 3 1 1 1 1 0
```
Transformed Output:
```
3 3 3 3 3 3 3 3 3 1 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 1 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 1 3 3 3 3 3 3 3 3 3 3
3 3 9 9 3 3 3 3 3 1 3 3 3 3 3 3 3 3 3 3
3 3 9 9 3 3 3 3 3 1 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 1 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 1 3 3 3 3 3 9 9 9 9 3
3 3 3 3 3 3 3 3 1 3 1 3 3 3 3 9 9 9 9 3
3 3 1 1 1 1 1 1 3 3 3 1 3 3 3 9 9 9 9 3
3 1 3 3 3 3 3 3 3 3 3 3 1 3 3 9 9 9 9 3
1 3 3 3 3 3 3 3 3 3 3 3 3 1 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3 3 1 3 3 3 3 3 3
3 3 3 3 3 3 9 9 9 9 9 9 3 3 1 3 3 3 3 3
3 3 3 3 3 3 9 9 9 9 9 9 3 3 3 1 3 3 3 3
3 3 3 3 3 3 9 9 9 9 9 9 3 3 3 3 1 3 3 3
3 3 3 3 3 3 9 9 9 9 9 9 3 3 3 3 3 1 3 3
3 3 3 3 3 3 9 9 9 9 9 9 3 3 3 3 3 3 1 3
3 3 3 3 3 3 9 9 9 9 9 9 3 3 3 3 3 3 3 1
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
```
Match: False
Pixels Off: 200
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 100.0

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 9 9 9 9 0 0 0
0 0 0 0 0 0 0 0 9 9 9 9 0 0 0
0 0 0 0 0 0 0 0 9 9 9 9 0 0 0
0 0 0 0 0 0 0 0 9 9 9 9 0 0 0
0 0 0 9 9 0 0 0 0 0 0 0 0 0 0
0 0 0 9 9 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 9 9
0 0 0 0 0 0 0 0 0 0 0 0 0 9 9
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 3 3 3 3 3 3 3 3 0
0 0 0 0 0 0 3 3 3 3 3 3 3 3 0
0 0 0 0 0 0 3 3 9 9 9 9 3 3 0
0 0 0 0 0 0 3 3 9 9 9 9 3 3 0
0 0 0 0 0 0 3 3 9 9 9 9 3 3 0
0 0 3 3 3 3 3 3 9 9 9 9 3 3 0
0 0 3 9 9 3 3 3 3 3 3 3 3 3 0
0 0 3 9 9 3 3 3 3 3 3 3 3 3 0
0 0 3 3 3 3 0 0 1 1 1 1 3 3 3
0 0 0 1 1 0 0 0 1 1 1 1 3 9 9
0 0 0 1 1 0 0 0 1 1 1 1 3 9 9
0 0 0 1 1 0 0 0 1 1 1 1 3 3 3
0 0 0 1 1 0 0 0 1 1 1 1 0 1 1
0 0 0 1 1 0 0 0 1 1 1 1 0 1 1
0 0 0 1 1 0 0 0 1 1 1 1 0 1 1
```
Transformed Output:
```
3 3 1 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 1 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 1 3 3 3 9 9 9 9 3 3 3
3 3 3 3 3 1 3 3 9 9 9 9 3 3 3
3 3 3 3 3 3 1 3 9 9 9 9 3 3 3
3 3 3 3 3 3 1 3 9 9 9 9 3 3 3
3 3 3 9 9 3 1 3 3 3 3 3 3 3 1
3 3 3 9 9 3 1 3 3 3 3 1 1 1 3
3 3 3 3 3 3 3 1 3 3 1 3 3 3 3
3 3 3 3 3 3 3 3 1 1 3 3 3 9 9
3 3 3 3 3 3 3 3 3 3 3 3 3 9 9
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 1 3 3 3 3 3 3
3 3 3 3 3 3 3 1 3 3 3 3 3 3 3
3 3 3 3 3 3 1 3 3 3 3 3 3 3 3
```
Match: False
Pixels Off: 136
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 120.88888888888889

## Example 3:
Input:
```
0 0 0 0 0 0 0 9 9 9 9 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 9 9 9 9 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 9 9 9 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 9 9 9 9 0 0 0 0 0 0 0 0 9 9 9 9 9 9
0 0 9 9 9 9 0 0 0 0 0 0 0 0 9 9 9 9 9 9
0 0 9 9 9 9 0 0 0 0 0 0 0 0 9 9 9 9 9 9
0 0 0 0 0 0 0 0 0 0 0 0 0 0 9 9 9 9 9 9
0 0 0 0 0 0 0 0 0 0 0 0 0 0 9 9 9 9 9 9
0 0 0 0 0 0 0 0 0 0 0 0 0 0 9 9 9 9 9 9
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 3 3 9 9 9 9 3 3 0 0 0 0 0 0 0
0 0 0 0 0 3 3 9 9 9 9 3 3 0 0 0 0 0 0 0
0 0 0 0 0 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0
0 0 0 0 0 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 1 1 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 1 1 1 0 0 0 0 0 0 0 0 0
3 3 3 3 3 3 3 3 1 1 1 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 1 1 1 3 3 3 3 3 3 3 3 3
3 3 9 9 9 9 3 3 1 1 1 3 3 3 3 3 3 3 3 3
3 3 9 9 9 9 3 3 1 1 1 3 3 3 9 9 9 9 9 9
3 3 9 9 9 9 3 3 1 1 1 3 3 3 9 9 9 9 9 9
3 3 9 9 9 9 3 3 1 1 1 3 3 3 9 9 9 9 9 9
3 3 3 3 3 3 3 3 1 1 1 3 3 3 9 9 9 9 9 9
3 3 3 3 3 3 3 3 1 1 1 3 3 3 9 9 9 9 9 9
0 0 1 1 1 1 0 1 1 1 1 3 3 3 9 9 9 9 9 9
0 0 1 1 1 1 0 1 1 1 1 3 3 3 3 3 3 3 3 3
0 0 1 1 1 1 0 1 1 1 1 3 3 3 3 3 3 3 3 3
0 0 1 1 1 1 0 1 1 1 1 3 3 3 3 3 3 3 3 3
0 0 1 1 1 1 0 1 1 1 1 0 0 0 1 1 1 1 1 1
0 0 1 1 1 1 0 1 1 1 1 0 0 0 1 1 1 1 1 1
```
Transformed Output:
```
3 3 3 3 3 3 3 9 9 9 9 3 3 3 3 3 3 3 3 1
1 3 3 3 3 3 3 9 9 9 9 3 3 3 3 3 3 3 1 3
3 1 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 1 3 3
3 3 1 3 3 3 3 3 3 3 3 3 3 3 3 3 1 3 3 3
3 3 3 1 3 3 3 3 3 3 3 3 3 3 3 1 3 3 3 3
3 3 3 3 3 3 3 3 3 1 1 1 1 1 1 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 9 9 9 9 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 9 9 9 9 3 3 3 3 3 3 3 3 9 9 9 9 9 9
3 3 9 9 9 9 3 3 3 3 3 3 3 3 9 9 9 9 9 9
3 3 9 9 9 9 3 3 3 3 3 3 3 3 9 9 9 9 9 9
3 3 3 3 3 3 3 3 3 3 3 3 3 3 9 9 9 9 9 9
3 3 3 3 3 3 3 3 3 3 3 3 3 3 9 9 9 9 9 9
3 3 3 3 3 3 3 3 3 3 3 3 3 3 9 9 9 9 9 9
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 1 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 1 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 1 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 1 3 3 3 3 3 3 3 3 3 3 3 3 3
```
Match: False
Pixels Off: 191
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 95.5

## Example 4:
Input:
```
0 0 0 0 0 0 9 9 0 0
0 0 0 0 0 0 9 9 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 9 9 0 0 0 0 0 0 0
0 9 9 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 3 9 9 3 0
0 0 0 0 0 3 9 9 3 0
0 0 0 0 0 3 3 3 3 0
0 0 0 0 0 0 1 1 0 0
0 0 0 0 0 0 1 1 0 0
0 0 0 0 0 0 1 1 0 0
3 3 3 3 0 0 1 1 0 0
3 9 9 3 0 0 1 1 0 0
3 9 9 3 0 0 1 1 0 0
3 3 3 3 0 0 1 1 0 0
```
Transformed Output:
```
3 3 3 3 3 3 9 9 3 3
1 3 3 3 3 3 9 9 3 3
3 1 3 3 3 3 3 3 3 3
3 3 1 3 3 3 3 3 3 3
3 3 3 1 1 1 3 3 3 3
3 3 3 3 3 3 1 3 3 3
3 3 3 3 3 3 3 1 3 3
3 9 9 3 3 3 3 3 1 3
3 9 9 3 3 3 3 3 3 1
3 3 3 3 3 3 3 3 3 3
```
Match: False
Pixels Off: 70
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 140.0
