
## train_1

**input:**
```
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 4 8 8 8 8 8 8 8
8 8 7 1 6 5 6 1 8 8
8 8 8 8 8 8 8 2 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
```


**output:**
```
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 2 8 8 8 8 8 8 8
8 8 1 6 5 6 1 7 8 8
8 8 8 8 8 8 8 4 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
```


## train_2

**input:**
```
8 8 8 8 8 8 8 8 8 8
8 8 1 8 8 8 8 8 8 8
8 8 7 8 8 8 8 8 8 8
8 8 9 6 8 8 8 8 8 8
8 8 8 4 7 7 8 8 8 8
8 8 8 8 8 1 8 8 8 8
8 8 8 8 8 4 8 8 8 8
8 8 8 8 8 4 2 1 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
```


**output:**
```
8 8 8 8 8 8 8 8 8 8
8 8 1 8 8 8 8 8 8 8
8 8 2 8 8 8 8 8 8 8
8 8 4 4 8 8 8 8 8 8
8 8 8 1 7 7 8 8 8 8
8 8 8 8 8 4 8 8 8 8
8 8 8 8 8 6 8 8 8 8
8 8 8 8 8 9 7 1 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
```

*   **Perception of Elements:**
    *   The input and output grids are the same size (10x10).
    *   Both grids have a dominant background color: azure (8).
    *   In both examples, there is a single connected object composed of non-azure pixels.
    *   The shape and position of this object remain the same from input to output.
    *   The colors of the pixels *within* the object change.
    *   The object in `train_1` is an 'L' shape with a horizontal segment and two vertical pixels attached at the ends. The object in `train_2` is a more complex, snake-like path.
    *   Comparing the input and output colors for the object suggests a transformation based on the object's structure. Specifically, the object appears to behave like a path or sequence.

*   **YAML Facts:**
    
```yaml
    task_context:
      grid_size: constant (10x10 in examples)
      background_color: azure (8)
      num_objects: 1 (connected component of non-background pixels)

    object_properties:
      type: connected component of non-background pixels
      structure: path-like (a sequence of connected pixels)
      invariance: position and shape remain constant between input and output
      endpoints: two pixels within the object having only one object neighbor (degree 1 nodes in the object graph)

    transformation:
      action: modify colors within the object
      rule: reverse the sequence of colors along the path connecting the two endpoints
      details:
        - identify the object pixels
        - find the two endpoint pixels
        - trace the path between endpoints
        - extract the color sequence along the path
        - reverse the color sequence
        - map the reversed colors back onto the path pixels in the output grid

    relationships:
      - pixels within the object are connected adjacently (including diagonals)
      - endpoints define the start and end of the color sequence to be reversed
      - background pixels are unchanged
    ```


*   **Natural Language Program:**
    1.  Identify the single connected object formed by pixels that are not the background color (azure, 8).
    2.  Find the two endpoint pixels of this object. An endpoint is an object pixel connected to only one other object pixel (considering 8-way adjacency).
    3.  Determine the unique path (sequence of adjacent pixels) that connects these two endpoints within the object.
    4.  Extract the list of colors corresponding to the pixels along this path, starting from one endpoint and proceeding to the other.
    5.  Reverse the order of the colors in this list.
    6.  Create the output grid by copying the input grid.
    7.  Replace the color of each pixel along the path in the output grid with the color at the corresponding position in the reversed list. Keep all background pixels unchanged.
```python
import numpy as np
from collections import deque

"""
Identifies a single connected object of non-background pixels (azure, 8). 
Finds the two endpoints of this object (pixels with only one object neighbor).
Traces the path connecting these endpoints.
Extracts the colors along this path, reverses the color sequence, and applies 
the reversed sequence back onto the path pixels in the output grid. 
The background remains unchanged.
"""

def get_neighbors(coord, grid_shape, connectivity=8):
    """Gets valid neighbor coordinates for a given coordinate."""
    r, c = coord
    rows, cols = grid_shape
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            if connectivity == 4 and abs(dr) + abs(dc) != 1:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbors.append((nr, nc))
    return neighbors

def find_object_pixels(grid, background_color):
    """Finds all coordinates belonging to non-background objects."""
    object_pixels = set()
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != background_color:
                object_pixels.add((r, c))
    return object_pixels

def find_endpoints(object_pixels, grid_shape):
    """Finds endpoint pixels within the object set."""
    endpoints = []
    for r, c in object_pixels:
        neighbor_count = 0
        for nr, nc in get_neighbors((r, c), grid_shape, connectivity=8):
            if (nr, nc) in object_pixels:
                neighbor_count += 1
        if neighbor_count == 1:
            endpoints.append((r, c))
    return endpoints

def find_path_bfs(start, end, object_pixels, grid_shape):
    """Finds the path between start and end points using BFS within object pixels."""
    if start not in object_pixels or end not in object_pixels:
        return None

    queue = deque([(start, [start])]) # Store (current_coord, path_so_far)
    visited = {start}

    while queue:
        current_coord, path = queue.popleft()

        if current_coord == end:
            return path

        for neighbor in get_neighbors(current_coord, grid_shape, connectivity=8):
            if neighbor in object_pixels and neighbor not in visited:
                visited.add(neighbor)
                new_path = list(path)
                new_path.append(neighbor)
                queue.append((neighbor, new_path))

    return None # Path not found

def transform(input_grid):
    """
    Reverses the color sequence along the path connecting the endpoints 
    of the single non-background object.
    """
    # Convert input to numpy array for easier handling
    input_grid_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_grid_np)
    grid_shape = input_grid_np.shape
    
    # Define background color (assuming 8 based on examples)
    background_color = 8 

    # 1. Identify the object pixels
    object_pixels = find_object_pixels(input_grid_np, background_color)

    if not object_pixels:
        # No object found, return the original grid
        return output_grid.tolist() 

    # 2. Find the endpoints
    endpoints = find_endpoints(object_pixels, grid_shape)

    # Expect exactly two endpoints for a simple path
    if len(endpoints) != 2:
        # Unexpected structure, return original grid 
        # (or handle differently based on more examples/rules)
         return output_grid.tolist()

    start_node, end_node = endpoints[0], endpoints[1]

    # 3. Determine the path between endpoints
    path_coords = find_path_bfs(start_node, end_node, object_pixels, grid_shape)

    if path_coords is None:
         # Path not found (shouldn't happen if endpoints are correct for a single connected object)
         return output_grid.tolist() 

    # 4. Extract the list of colors along the path
    path_colors = [input_grid_np[r, c] for r, c in path_coords]

    # 5. Reverse the order of the colors
    reversed_colors = path_colors[::-1]

    # 6. Create the output grid (already copied)
    # 7. Replace colors along the path with reversed colors
    for i, (r, c) in enumerate(path_coords):
        output_grid[r, c] = reversed_colors[i]

    # Return the modified grid as a list of lists
    return output_grid.tolist()
```
```python
import numpy as np
from collections import deque
import heapq

"""
Identifies the single connected object of non-background pixels (azure, 8).
Finds the two pixels within the object having the minimum number of object neighbors (using 8-way connectivity).
These pixels define the ends of a path that includes all pixels of the object.
Determines the path traversing all object pixels between these two ends.
Extracts the colors along this path, reverses the color sequence, and applies
the reversed sequence back onto the path pixels in the output grid.
The background (azure, 8) remains unchanged.
"""

# --- Helper Functions ---

def get_neighbors(coord, grid_shape, connectivity=8):
    """Gets valid neighbor coordinates for a given coordinate based on connectivity."""
    r, c = coord
    rows, cols = grid_shape
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0: continue
            # Skip diagonals if connectivity is 4
            if connectivity == 4 and abs(dr) + abs(dc) != 1: continue
            nr, nc = r + dr, c + dc
            # Check bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbors.append((nr, nc))
    return neighbors

def find_object_pixels(grid, background_color):
    """Finds all coordinates belonging to non-background objects."""
    object_pixels = set()
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != background_color:
                object_pixels.add((r, c))
    return object_pixels

def find_min_neighbor_ends(object_pixels, grid_shape, connectivity=8):
    """
    Finds the two pixels within the object that have the minimum number of
    neighbors also belonging to the object. Handles ties by picking the
    first two encountered based on heap ordering (approximates coordinate sort).
    Returns a sorted list of the two endpoint coordinates.
    """
    if not object_pixels: return []
    if len(object_pixels) == 1: return list(object_pixels) # Single pixel object

    neighbor_counts = [] # Store (count, coord) tuples
    neighbor_map = {} # Store {coord: count} for easy lookup

    # Calculate neighbor counts for each object pixel
    for r, c in object_pixels:
        count = 0
        for nr, nc in get_neighbors((r, c), grid_shape, connectivity):
            if (nr, nc) in object_pixels:
                count += 1
        heapq.heappush(neighbor_counts, (count, (r, c)))
        neighbor_map[(r, c)] = count

    if not neighbor_counts: return []

    # Find the minimum count
    min_count = neighbor_counts[0][0]

    # Collect all pixels with the minimum count
    min_count_pixels = [coord for count, coord in neighbor_counts if count == min_count]

    # If there are exactly two, these are our ends
    if len(min_count_pixels) == 2:
        return sorted(min_count_pixels)
    # If there's only one with the minimum count (e.g., start of a line ending in a thicker part)
    # Find the pixel with the second minimum count.
    elif len(min_count_pixels) == 1:
        first_end = min_count_pixels[0]
        second_end = None
        min_count2 = float('inf')
        # Find the minimum count > min_count
        for count, coord in neighbor_counts:
             if count > min_count:
                 min_count2 = min(min_count2, count)

        # Collect all pixels with this second minimum count
        second_min_pixels = [coord for count, coord in neighbor_counts if count == min_count2]

        # If there's one, that's our second end. If multiple, pick the first by sort order.
        if second_min_pixels:
             second_end = sorted(second_min_pixels)[0]
             return sorted([first_end, second_end])
        else: # Should not happen if object size > 1
             return sorted([first_end]) # Only found one end

    # If there are more than two pixels with the minimum count (e.g., corners of a rectangle)
    # We need a tie-breaker. Sorting by coordinates (row, then col) is a common heuristic.
    elif len(min_count_pixels) > 2:
         # Return the two extremes based on coordinate sorting
         sorted_min_pixels = sorted(min_count_pixels)
         return [sorted_min_pixels[0], sorted_min_pixels[-1]]

    return [] # Should not be reached

def find_full_path_dfs(start, end, object_pixels, grid_shape, connectivity=8):
    """
    Finds a path using Depth First Search that starts at 'start', ends at 'end',
    and visits every pixel in 'object_pixels' exactly once.
    """
    if not object_pixels: return None
    # Handle single pixel object case
    if start == end: return [start] if start in object_pixels else None
    if start not in object_pixels or end not in object_pixels: return None

    target_path_len = len(object_pixels)
    stack = [(start, [start])] # Stack stores (current_node, path_list_so_far)

    while stack:
        (current_node, path) = stack.pop()

        # Check if we reached the target end and the path includes all object pixels
        if current_node == end and len(path) == target_path_len:
            # Verify all object pixels are indeed in the path (sanity check)
            if set(path) == object_pixels:
                return path
            else:
                 # This case indicates an issue, maybe disconnected components mistakenly treated as one object?
                 continue # Continue searching

        # Explore neighbors
        # Get neighbors and filter for those within the object
        potential_neighbors = [n for n in get_neighbors(current_node, grid_shape, connectivity) if n in object_pixels]

        for neighbor in potential_neighbors:
            # If the neighbor hasn't been visited in the current path attempt
            if neighbor not in path:
                new_path = path + [neighbor]
                # Check again if we just reached the end with the correct length
                if neighbor == end and len(new_path) == target_path_len:
                     if set(new_path) == object_pixels:
                         return new_path
                     else:
                         continue
                # If not the end, or path too short, push to stack to explore further
                # Optimization: Don't push if path is already too long (shouldn't happen with 'not in path' check)
                elif len(new_path) <= target_path_len:
                     stack.append((neighbor, new_path))

    # If the loop finishes without returning, no valid path covering all pixels was found
    print(f"DFS Warning: Could not find a path from {start} to {end} covering all {target_path_len} pixels.")
    return None

# --- Main Transformation Function ---

def transform(input_grid):
    """
    Reverses the color sequence along the path covering all pixels of the
    single non-background object, defined by its min-neighbor endpoints.
    """
    # Convert input to numpy array for easier handling
    input_grid_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_grid_np)
    grid_shape = input_grid_np.shape

    # Define background color (assuming 8 based on examples)
    background_color = 8
    # Define connectivity (assuming 8 based on examples)
    connectivity = 8

    # 1. Identify the object pixels
    object_pixels = find_object_pixels(input_grid_np, background_color)

    # If no object, return original grid
    if not object_pixels:
        return output_grid.tolist()

    # Handle single-pixel object: color remains the same
    if len(object_pixels) == 1:
        return output_grid.tolist()

    # 2. Find the two 'end' pixels (those with minimum object neighbors)
    endpoints = find_min_neighbor_ends(object_pixels, grid_shape, connectivity)

    # Expect exactly two endpoints for a reversible path covering all pixels
    if len(endpoints) != 2:
        print(f"Warning: Expected 2 endpoints, found {len(endpoints)}: {endpoints}. Returning original grid.")
        # Or potentially handle single endpoint for loops if needed? For now, return original.
        return output_grid.tolist()

    # Endpoints are already sorted by find_min_neighbor_ends
    start_node, end_node = endpoints[0], endpoints[1]

    # 3. Determine the path covering all object pixels between endpoints using DFS
    path_coords = find_full_path_dfs(start_node, end_node, object_pixels, grid_shape, connectivity)

    # If DFS couldn't find a path covering all pixels (might happen for complex shapes)
    if path_coords is None:
        # Try reversing the start/end points just in case DFS implementation has directional bias
        # although a correct DFS shouldn't theoretically need this if a path exists.
        print(f"Retrying DFS with reversed endpoints: {end_node} -> {start_node}")
        path_coords = find_full_path_dfs(end_node, start_node, object_pixels, grid_shape, connectivity)

    if path_coords is None or len(path_coords) != len(object_pixels):
        print(f"Error: Failed to find a valid path covering all object pixels. Path length found: {len(path_coords) if path_coords else 0}, Object size: {len(object_pixels)}. Returning original grid.")
        return output_grid.tolist()

    # 4. Extract the list of colors along the found path
    path_colors = [input_grid_np[r, c] for r, c in path_coords]

    # 5. Reverse the order of the colors
    reversed_colors = path_colors[::-1]

    # 6. Create the output grid (already copied)
    # 7. Replace colors along the path coordinates with the reversed colors
    for i, (r, c) in enumerate(path_coords):
        output_grid[r, c] = reversed_colors[i]

    # Return the modified grid as a list of lists
    return output_grid.tolist()
```
```python
import numpy as np
from collections import deque

"""
Identifies the single connected object of non-background pixels (azure, 8).
Finds the two endpoint pixels of this object (pixels with only one object neighbor 
using 8-way connectivity).
Determines the unique path connecting these two endpoints within the object 
using Breadth-First Search (BFS).
Extracts the sequence of colors along this path.
Reverses the sequence of colors.
Applies the reversed color sequence back onto the path pixels in the output grid.
The background color (azure, 8) remains unchanged.
"""

# --- Helper Functions ---

def get_neighbors(coord, grid_shape, connectivity=8):
    """
    Gets valid neighbor coordinates for a given coordinate based on connectivity.

    Args:
        coord (tuple): The (row, col) coordinate.
        grid_shape (tuple): The (height, width) of the grid.
        connectivity (int): 4 or 8 for neighbor definition.

    Returns:
        list: A list of valid neighbor (row, col) tuples.
    """
    r, c = coord
    rows, cols = grid_shape
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            # Skip self
            if dr == 0 and dc == 0: continue
            # Skip diagonals if connectivity is 4
            if connectivity == 4 and abs(dr) + abs(dc) != 1: continue
            
            nr, nc = r + dr, c + dc
            # Check bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbors.append((nr, nc))
    return neighbors

def find_object_pixels(grid, background_color):
    """
    Finds all coordinates belonging to non-background objects.

    Args:
        grid (np.array): The input grid.
        background_color (int): The color considered background.

    Returns:
        set: A set of (row, col) tuples for object pixels.
    """
    object_pixels = set()
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != background_color:
                object_pixels.add((r, c))
    return object_pixels

def find_endpoints(object_pixels, grid_shape, connectivity=8):
    """
    Finds endpoint pixels within the object set. Endpoints are defined as
    object pixels having exactly one neighbor that is also an object pixel.

    Args:
        object_pixels (set): Set of (row, col) coordinates of the object.
        grid_shape (tuple): The (height, width) of the grid.
        connectivity (int): 4 or 8 for neighbor definition.

    Returns:
        list: A list of endpoint (row, col) coordinates. Returns the single
              pixel coordinate if the object has only one pixel. Returns an
              empty list if no object pixels are provided.
    """
    endpoints = []
    if not object_pixels:
        return endpoints
        
    # Handle single pixel object case explicitly
    if len(object_pixels) == 1:
        return list(object_pixels) 

    # Iterate through each pixel belonging to the object
    for r, c in object_pixels:
        neighbor_count = 0
        # Count how many of its neighbors are also part of the object
        for nr, nc in get_neighbors((r, c), grid_shape, connectivity):
            if (nr, nc) in object_pixels:
                neighbor_count += 1
        
        # An endpoint must have exactly one connection within the object
        if neighbor_count == 1:
            endpoints.append((r, c))
            
    # Note: For simple paths, we expect exactly 2 endpoints. 
    # Other structures (loops, branches) might have 0 or >2.
    return endpoints


def find_path_bfs(start, end, object_pixels, grid_shape, connectivity=8):
    """
    Finds the path between start and end points using Breadth-First Search (BFS),
    constrained to move only within the provided object pixels.

    Args:
        start (tuple): The starting (row, col) coordinate.
        end (tuple): The target (row, col) coordinate.
        object_pixels (set): The set of valid (row, col) pixels for the path.
        grid_shape (tuple): The (height, width) of the grid.
        connectivity (int): 4 or 8 for neighbor definition.

    Returns:
        list: A list of (row, col) coordinates forming the path from start 
              to end, including both. Returns None if no path exists. Returns
              [start] if start and end are the same.
    """
    # Basic checks
    if start not in object_pixels or end not in object_pixels:
        # print(f"Warning: Start {start} or End {end} not in object pixels.")
        return None
        
    # Handle case where start and end are the same
    if start == end:
        return [start]

    # Initialize BFS queue with (current_coordinate, path_so_far)
    queue = deque([(start, [start])]) 
    visited = {start} # Keep track of visited nodes to avoid cycles and redundant work

    while queue:
        current_coord, path = queue.popleft()

        # Check if we reached the target
        if current_coord == end:
            return path # Path found

        # Explore neighbors
        for neighbor in get_neighbors(current_coord, grid_shape, connectivity):
            # Check if the neighbor is part of the object and hasn't been visited yet
            if neighbor in object_pixels and neighbor not in visited:
                visited.add(neighbor)
                # Create the new path by extending the current path
                new_path = list(path)
                new_path.append(neighbor)
                # Add the neighbor and its path to the queue
                queue.append((neighbor, new_path))

    # If the queue becomes empty and we haven't found the end node, no path exists
    # print(f"Warning: BFS could not find a path from {start} to {end} within the object.")
    return None 

# --- Main Transformation Function ---

def transform(input_grid):
    """
    Transforms the input grid by reversing the color sequence along the path 
    connecting the endpoints of the single non-background object.
    
    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed grid. Returns the original grid if no
                       object is found, the object is a single pixel, or the
                       object doesn't have exactly two endpoints (indicating
                       it's not a simple path).
    """
    # Convert input to numpy array for efficient operations
    input_grid_np = np.array(input_grid, dtype=int)
    # Create a copy to modify, preserving the original input
    output_grid = np.copy(input_grid_np)
    grid_shape = input_grid_np.shape

    # --- Configuration ---
    background_color = 8  # Assume azure (8) is the background
    connectivity = 8      # Use 8-way connectivity (includes diagonals)

    # --- Workflow ---

    # 1. Identify the object pixels (all pixels not matching the background color)
    object_pixels = find_object_pixels(input_grid_np, background_color)

    # If no object pixels exist, return the original grid
    if not object_pixels:
        return output_grid.tolist()

    # If the object is just a single pixel, no reversal is possible/needed
    if len(object_pixels) == 1:
        return output_grid.tolist()

    # 2. Find the endpoint pixels (object pixels with exactly one object neighbor)
    endpoints = find_endpoints(object_pixels, grid_shape, connectivity)

    # For a reversible path structure, we expect exactly two endpoints.
    # If not, the structure is likely a loop, branched, or ill-defined for this task.
    if len(endpoints) != 2:
        # print(f"Warning: Expected 2 endpoints, found {len(endpoints)}. Returning original grid.")
        return output_grid.tolist()

    # Assign start and end points for path finding
    start_node, end_node = endpoints[0], endpoints[1]

    # 3. Determine the path connecting the two endpoints using BFS
    #    The path must stay within the identified object pixels.
    path_coords = find_path_bfs(start_node, end_node, object_pixels, grid_shape, connectivity)

    # Check if a valid path was found between the endpoints
    if path_coords is None:
         # print(f"Error: Failed to find path between endpoints {start_node} and {end_node}. Returning original grid.")
         return output_grid.tolist()
         
    # Optional Sanity Check: Verify if the found path covers all object pixels.
    # This holds true for the examples, suggesting they are simple, non-branching paths.
    # If this check fails, it might indicate a more complex object structure.
    if set(path_coords) != object_pixels:
         # print(f"Warning: BFS path length ({len(path_coords)}) differs from object size ({len(object_pixels)}). Structure might be complex. Reversing colors along the found path anyway.")
         pass # Proceed even if not all pixels are covered, reversing along the primary path.

    # 4. Extract the sequence of colors along the determined path
    path_colors = [input_grid_np[r, c] for r, c in path_coords]

    # 5. Reverse the order of this color sequence
    reversed_colors = path_colors[::-1]

    # 6. Update the output grid: Iterate through the path coordinates and assign
    #    the corresponding color from the reversed sequence.
    for i, (r, c) in enumerate(path_coords):
        output_grid[r, c] = reversed_colors[i]

    # 7. Convert the final numpy array back to a list of lists and return
    return output_grid.tolist()
```
