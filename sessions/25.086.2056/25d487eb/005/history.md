
Previous Code:
```python
import numpy as np
from collections import deque

"""
Transformation Rule:
1. Identify all contiguous objects of non-background (non-zero) color.
2. Find the largest object ('container'). Record its color ('C_container').
3. Find a single-pixel object ('source') with a different color ('C_source') that is cardinally adjacent to the container object. Assume exactly one such source exists. Record its position ('r_src', 'c_src').
4. Calculate distances from the source pixel along the four cardinal directions. The distance in a direction is the count of consecutive pixels with color 'C_container' starting from the source's neighbor in that direction, stopping when a non-'C_container' pixel or the grid boundary is encountered.
5. Determine the direction(s) with the minimum distance.
6. The projection direction is the opposite of the minimum distance direction. (Assuming a single minimum direction based on examples).
7. Starting from the pixel adjacent to the source in the projection direction, paint pixels with 'C_source' along this direction until the grid boundary is reached, overwriting existing colors.
8. The modified grid is the output.
"""

def find_objects(grid, background_color=0):
    """
    Finds all contiguous objects of the same color in the grid.

    Args:
        grid (np.array): The input grid.
        background_color (int): The color to treat as background (default 0).

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              and contains {'color': int, 'coords': set_of_tuples, 'size': int}.
              Excludes background objects.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    for r in range(height):
        for c in range(width):
            if not visited[r, c]:
                color = grid[r, c]
                # Skip background color
                if color == background_color:
                    visited[r,c] = True
                    continue
                
                # Start BFS for a new object
                obj_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                obj_coords.add((r, c))
                
                while q:
                    row, col = q.popleft()
                    # Check cardinal neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            obj_coords.add((nr, nc))
                            
                # Store the found object
                if obj_coords:
                    objects.append({'color': color, 'coords': obj_coords, 'size': len(obj_coords)})
                    
    return objects

def get_neighbors(r, c, height, width):
    """
    Get coordinates of cardinal neighbors for a given cell.

    Args:
        r (int): Row index of the cell.
        c (int): Column index of the cell.
        height (int): Grid height.
        width (int): Grid width.

    Returns:
        list: A list of (row, col) tuples for valid neighbors.
    """
    neighbors = []
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]: # Right, Left, Down, Up
        nr, nc = r + dr, c + dc
        if 0 <= nr < height and 0 <= nc < width:
            neighbors.append((nr, nc))
    return neighbors

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    output_grid = np.copy(grid)
    height, width = grid.shape

    # 1. Identify Objects
    objects = find_objects(grid)
    if not objects:
        return output_grid.tolist() # Return copy if no non-background objects

    # 2. Identify Container (largest object)
    objects.sort(key=lambda x: x['size'], reverse=True)
    container = objects[0]
    container_color = container['color']

    # 3. Identify Source (single pixel, different color, adjacent to container)
    source_pixel = None
    for obj in objects:
        # Check if it's a single pixel object and not the container color
        if obj['size'] == 1 and obj['color'] != container_color:
            # Get the position of this single pixel
            r_src, c_src = list(obj['coords'])[0] 
            # Get its neighbors
            neighbors = get_neighbors(r_src, c_src, height, width)
            # Check if any neighbor has the container color
            is_adjacent_to_container = any(grid[nr, nc] == container_color for nr, nc in neighbors)
            
            if is_adjacent_to_container:
                source_pixel = {'color': obj['color'], 'pos': (r_src, c_src)}
                break # Assume exactly one such source as per analysis

    # If no valid source pixel found according to the rules, return original grid
    if not source_pixel:
        return output_grid.tolist() 

    source_color = source_pixel['color']
    source_r, source_c = source_pixel['pos']

    # 4. Calculate Distances (count consecutive container-colored cells from source)
    distances = {'up': 0, 'down': 0, 'left': 0, 'right': 0}
    
    # Calculate UP distance
    r = source_r - 1
    while r >= 0 and grid[r, source_c] == container_color:
        distances['up'] += 1
        r -= 1
        
    # Calculate DOWN distance
    r = source_r + 1
    while r < height and grid[r, source_c] == container_color:
        distances['down'] += 1
        r += 1

    # Calculate LEFT distance
    c = source_c - 1
    while c >= 0 and grid[source_r, c] == container_color:
        distances['left'] += 1
        c -= 1
        
    # Calculate RIGHT distance
    c = source_c + 1
    while c < width and grid[source_r, c] == container_color:
        distances['right'] += 1
        c += 1

    # 5. Determine Projection Direction (opposite of minimum distance direction)
    min_dist = float('inf')
    min_dir = None
    # Iterate in a fixed order to handle potential ties deterministically (first found wins)
    for direction in ['up', 'down', 'left', 'right']:
        if distances[direction] < min_dist:
            min_dist = distances[direction]
            min_dir = direction

    # This case should ideally not be reached if a source was found
    if min_dir is None: 
         return output_grid.tolist() 

    opposite_dirs = {'up': 'down', 'down': 'up', 'left': 'right', 'right': 'left'}
    projection_dir = opposite_dirs[min_dir]

    # 6. Perform Projection
    dr, dc = 0, 0
    if projection_dir == 'up': dr = -1
    elif projection_dir == 'down': dr = 1
    elif projection_dir == 'left': dc = -1
    elif projection_dir == 'right': dc = 1

    # Start projection from the cell *adjacent* to the source in the projection direction
    curr_r, curr_c = source_r + dr, source_c + dc 
    
    # Continue projection until the grid boundary is reached
    while 0 <= curr_r < height and 0 <= curr_c < width:
        output_grid[curr_r, curr_c] = source_color
        # Move to the next cell in the projection direction
        curr_r += dr
        curr_c += dc

    # 7. Output: Convert the result back to a list of lists
    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 8 8 8 0 0 0 0
0 0 0 0 8 8 8 8 8 0 0 0
0 0 0 8 8 8 3 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 8 8 8 0 0 0 0
0 0 0 0 8 8 8 8 8 0 0 0
0 0 0 8 8 8 3 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 8 3 8 0 0 0 0
0 0 0 0 8 8 3 8 8 0 0 0
0 0 0 8 8 8 3 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 3
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 4.166666666666686

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 0 0 0 0 0 0 0 0 0 0
0 0 0 1 2 2 0 0 0 0 0 0 0 0 0
0 0 0 2 2 0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 0 0 0 0 0 0 0 0 0 0
0 0 0 1 2 2 1 1 1 1 1 1 1 1 1
0 0 0 2 2 0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 0 0 0 0 0 0 0 0 0 0
0 0 0 1 1 1 1 1 1 1 1 1 1 1 1
0 0 0 2 2 0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 2
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 2.666666666666657

## Example 3:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 2 3 3 0 0 0 0 0
0 0 0 3 3 3 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 2 3 3 0 0 0 0 0
0 0 0 3 3 3 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 2 3 3 0 0 0 0 0
0 0 0 3 2 3 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 2
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 2.2222222222222285
**General Assessment**

The previous code failed on all training examples. The core logic correctly identified the 'container' (largest object) and 'source' (single pixel of different color adjacent to the container). It also correctly determined the projection direction as the opposite of the direction with the minimum 'reach' from the source within the container.

However, the failure occurred during the projection step. The code painted *over* existing pixels (including parts of the container) starting from the pixel adjacent to the source inside the container, extending to the grid boundary.

The analysis of the expected outputs reveals a different projection behavior:
1.  The projection should *not* overwrite the container object or the source pixel.
2.  The projection should start from the first *non-container* (background) pixel found along the projection path originating from the source, just outside the container's edge in that direction.
3.  The projection should continue from this starting point towards the grid boundary, painting only the background pixels with the source color.

The strategy is to modify the projection logic to find this correct starting point and ensure only background pixels are painted along the projection line.

**Metrics and Analysis**

Let's analyze each example based on the refined understanding using code execution.



*code_execution:*
```python
import numpy as np
from collections import deque

# Re-using the find_objects function from the previous code
def find_objects(grid, background_color=0):
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    for r in range(height):
        for c in range(width):
            if not visited[r, c]:
                color = grid[r, c]
                if color == background_color:
                    visited[r,c] = True
                    continue
                obj_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                obj_coords.add((r, c))
                while q:
                    row, col = q.popleft()
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            obj_coords.add((nr, nc))
                if obj_coords:
                    objects.append({'color': color, 'coords': obj_coords, 'size': len(obj_coords)})
    return objects

# Function to get neighbors
def get_neighbors(r, c, height, width):
    neighbors = []
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]: # Right, Left, Down, Up
        nr, nc = r + dr, c + dc
        if 0 <= nr < height and 0 <= nc < width:
            neighbors.append((nr, nc))
    return neighbors

# Function to analyze a single example
def analyze_example(input_grid_list):
    grid = np.array(input_grid_list, dtype=int)
    height, width = grid.shape
    analysis = {}
    analysis['dimensions'] = (height, width)

    objects = find_objects(grid)
    if not objects:
        analysis['error'] = "No non-background objects found"
        return analysis

    objects.sort(key=lambda x: x['size'], reverse=True)
    container = objects[0]
    container_color = container['color']
    container_coords = container['coords']
    analysis['container'] = {'color': container_color, 'size': container['size']} #, 'coords': container_coords} # coords can be large

    source_pixel = None
    for obj in objects:
        if obj['size'] == 1 and obj['color'] != container_color:
            r_src, c_src = list(obj['coords'])[0]
            neighbors = get_neighbors(r_src, c_src, height, width)
            is_adjacent_to_container = any(grid[nr, nc] == container_color for nr, nc in neighbors)
            if is_adjacent_to_container:
                source_pixel = {'color': obj['color'], 'pos': (r_src, c_src)}
                break

    if not source_pixel:
        analysis['error'] = "No valid source pixel found"
        return analysis

    analysis['source'] = source_pixel
    source_color = source_pixel['color']
    source_r, source_c = source_pixel['pos']

    # Calculate Distances within container
    distances = {'up': 0, 'down': 0, 'left': 0, 'right': 0}
    directions = {'up': (-1, 0), 'down': (1, 0), 'left': (0, -1), 'right': (0, 1)}

    for direction, (dr, dc) in directions.items():
        nr, nc = source_r + dr, source_c + dc
        dist = 0
        while 0 <= nr < height and 0 <= nc < width and grid[nr, nc] == container_color:
            dist += 1
            nr += dr
            nc += dc
        distances[direction] = dist

    analysis['distances_in_container'] = distances

    min_dist = float('inf')
    min_dir = None
    # Fixed order for tie-breaking
    for direction in ['up', 'down', 'left', 'right']:
        if distances[direction] < min_dist:
            min_dist = distances[direction]
            min_dir = direction

    analysis['min_distance_direction'] = min_dir
    analysis['min_distance'] = min_dist

    opposite_dirs = {'up': 'down', 'down': 'up', 'left': 'right', 'right': 'left'}
    projection_dir = opposite_dirs[min_dir]
    analysis['projection_direction'] = projection_dir

    # Find projection start point (first non-container cell along projection path from source)
    proj_dr, proj_dc = directions[projection_dir]
    curr_r, curr_c = source_r + proj_dr, source_c + proj_dc
    
    # Move through container along projection direction
    while 0 <= curr_r < height and 0 <= curr_c < width and grid[curr_r, curr_c] == container_color:
         curr_r += proj_dr
         curr_c += proj_dc

    # Now (curr_r, curr_c) is the first cell *outside* the container in the projection path
    # Check if it's within bounds
    if 0 <= curr_r < height and 0 <= curr_c < width:
         analysis['projection_start_point'] = (curr_r, curr_c)
         analysis['projection_start_color'] = int(grid[curr_r, curr_c]) # Use int() for JSON compatibility
    else:
         analysis['projection_start_point'] = 'Out of bounds'
         analysis['projection_start_color'] = None


    return analysis


# --- Example Data ---
ex1_in = [[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,8,0,0,0,0,0],[0,0,0,0,0,8,8,8,0,0,0,0],[0,0,0,0,8,8,8,8,8,0,0,0],[0,0,0,8,8,8,3,8,8,8,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0]]
ex2_in = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,2,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,2,2,0,0,0,0,0,0,0,0,0,0],[0,0,0,1,2,2,0,0,0,0,0,0,0,0,0],[0,0,0,2,2,0,0,0,0,0,0,0,0,0,0],[0,0,0,2,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
ex3_in = [[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,3,3,2,3,3,0,0,0,0,0],[0,0,0,3,3,3,0,0,0,0,0,0],[0,0,0,0,3,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0]]

analysis1 = analyze_example(ex1_in)
analysis2 = analyze_example(ex2_in)
analysis3 = analyze_example(ex3_in)

print("--- Analysis Example 1 ---")
print(analysis1)
print("\n--- Analysis Example 2 ---")
print(analysis2)
print("\n--- Analysis Example 3 ---")
print(analysis3)
```

*code_execution_result:*
outcome: OUTCOME_OK
```
--- Analysis Example 1 ---
{'dimensions': (12, 12), 'container': {'color': np.int64(8), 'size': 15}, 'source': {'color': np.int64(3), 'pos': (8, 6)}, 'distances_in_container': {'up': 3, 'down': 0, 'left': 3, 'right': 3}, 'min_distance_direction': 'down', 'min_distance': 0, 'projection_direction': 'up', 'projection_start_point': (4, 6), 'projection_start_color': 0}

--- Analysis Example 2 ---
{'dimensions': (10, 15), 'container': {'color': np.int64(2), 'size': 8}, 'source': {'color': np.int64(1), 'pos': (4, 3)}, 'distances_in_container': {'up': 2, 'down': 2, 'left': 0, 'right': 2}, 'min_distance_direction': 'left', 'min_distance': 0, 'projection_direction': 'right', 'projection_start_point': (4, 6), 'projection_start_color': 0}

--- Analysis Example 3 ---
{'dimensions': (15, 12), 'container': {'color': np.int64(3), 'size': 8}, 'source': {'color': np.int64(2), 'pos': (2, 4)}, 'distances_in_container': {'up': 0, 'down': 2, 'left': 2, 'right': 2}, 'min_distance_direction': 'up', 'min_distance': 0, 'projection_direction': 'down', 'projection_start_point': (5, 4), 'projection_start_color': 0}

```
**Facts (YAML)**


```yaml
task_description: >
  The task involves identifying two key objects in the input grid: a 'container'
  (the largest contiguous object of a single color) and a 'source' (a single pixel
  of a different color that is cardinally adjacent to the container). Based on the
  shortest path from the source to the 'outside' (non-container or grid boundary)
  through the container, a projection line is drawn outwards from the container
  in the opposite direction.

definitions:
  - &background_color 0
  - &container
    description: The largest contiguous object of a single non-background color.
    properties: [color, size, coordinates]
  - &source
    description: >
      A single pixel object with a color different from the container, which is
      cardinally adjacent to at least one pixel of the container. Assumed to be unique.
    properties: [color, position]
  - &distance
    description: >
      The number of contiguous container-colored pixels starting from a neighbor
      of the source pixel, moving away from the source along one of the four
      cardinal directions, stopping when a non-container pixel or grid boundary
      is encountered.
  - &min_distance_direction
    description: >
      The cardinal direction (up, down, left, right) associated with the smallest
      calculated distance. Ties are broken by order: up, down, left, right.
  - &projection_direction
    description: The cardinal direction opposite to the min_distance_direction.
  - &projection_start_point
    description: >
      The first non-container (background) pixel encountered when moving from the source
      pixel along the projection_direction, passing through the container pixels.
  - &projection_line
    description: >
      A line of pixels starting from the projection_start_point and extending to
      the grid boundary along the projection_direction.

example_analysis:
  example_1:
    container: { color: 8 (azure), size: 15 }
    source: { color: 3 (green), position: (8, 6) }
    distances_in_container: { up: 3, down: 0, left: 3, right: 3 }
    min_distance_direction: down
    projection_direction: up
    projection_start_point: (4, 6) (color 0 - background)
    action: Paint pixels from (4, 6) to (0, 6) with source color (3).
  example_2:
    container: { color: 2 (red), size: 8 }
    source: { color: 1 (blue), position: (4, 3) }
    distances_in_container: { up: 2, down: 2, left: 0, right: 2 }
    min_distance_direction: left
    projection_direction: right
    projection_start_point: (4, 6) (color 0 - background)
    action: Paint pixels from (4, 6) to (4, 14) with source color (1).
  example_3:
    container: { color: 3 (green), size: 8 }
    source: { color: 2 (red), position: (2, 4) }
    distances_in_container: { up: 0, down: 2, left: 2, right: 2 }
    min_distance_direction: up
    projection_direction: down
    projection_start_point: (5, 4) (color 0 - background)
    action: Paint pixels from (5, 4) to (14, 4) with source color (2).

```


**Natural Language Program**

1.  **Identify Objects**:
    *   Find all contiguous objects of non-background (non-zero) colors.
    *   Identify the object with the largest number of pixels as the 'container'. Record its color (`C_container`) and coordinates.
    *   Find a single-pixel object whose color (`C_source`) is different from `C_container` and which is cardinally adjacent to any pixel of the container. Assume exactly one such 'source' exists. Record its position (`P_source`).
2.  **Calculate Distances**:
    *   For each cardinal direction (up, down, left, right), calculate the 'distance' from the source `P_source`. The distance is the count of contiguous pixels *having the container color `C_container`*, starting from the neighbor of `P_source` in that direction and moving outwards, stopping when a pixel with a different color or the grid boundary is reached.
3.  **Determine Projection Direction**:
    *   Find the direction(s) with the minimum calculated distance. If there are ties, select the first one in the order: up, down, left, right. This is the `min_distance_direction`.
    *   Determine the `projection_direction` which is the cardinal direction opposite to the `min_distance_direction` (up <-> down, left <-> right).
4.  **Find Projection Start Point**:
    *   Starting from `P_source`, trace a path along the `projection_direction`.
    *   Follow this path through all contiguous pixels belonging to the container.
    *   The first pixel encountered along this path *after exiting the container* (i.e., the first non-`C_container` pixel that is adjacent to the container edge along this path) is the `projection_start_point`. Ensure this point is within the grid boundaries.
5.  **Perform Projection**:
    *   Starting from the `projection_start_point`, paint pixels with the source color `C_source` along the `projection_direction` until the grid boundary is reached. Overwrite only the existing pixels along this line (which should typically be background color based on the examples).
6.  **Output**: The modified grid is the result. If no container or source is found matching the criteria, return the original grid unchanged.
