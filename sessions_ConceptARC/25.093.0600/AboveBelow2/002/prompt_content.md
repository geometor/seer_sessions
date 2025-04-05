
Previous Code:
```python
import numpy as np
import collections

"""
Identify all distinct connected components (objects) of non-zero cells in the input grid using orthogonal adjacency.
Determine which objects touch the top border (row 0).
Iteratively identify objects that are orthogonally adjacent to any object already marked for removal (starting with the top-border objects).
Create the output grid by copying the input grid.
Set the color of all cells belonging to the identified objects (top-touching and their adjacent chains) to 0 in the output grid.
Return the modified output grid.
"""

def find_objects(grid):
    """
    Finds all connected components of non-zero cells in the grid.

    Args:
        grid: A numpy array representing the grid.

    Returns:
        A list of objects, where each object is a list of (row, col) tuples.
        A dictionary mapping each cell (row, col) to its object index.
    """
    rows, cols = grid.shape
    visited = set()
    objects = []
    object_map = {} # Maps (r, c) -> object_index

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and (r, c) not in visited:
                current_object_index = len(objects)
                current_object_cells = []
                q = collections.deque([(r, c)])
                visited.add((r, c))

                while q:
                    row, col = q.popleft()
                    current_object_cells.append((row, col))
                    object_map[(row, col)] = current_object_index

                    # Check orthogonal neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] != 0 and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            q.append((nr, nc))
                
                if current_object_cells:
                    objects.append(current_object_cells)
                    
    return objects, object_map

def get_object_adjacency(objects, object_map, grid_shape):
    """
    Determines which objects are orthogonally adjacent to each other.

    Args:
        objects: A list of objects (lists of cell coordinates).
        object_map: A dictionary mapping cell coordinates to object index.
        grid_shape: Tuple (rows, cols) of the grid.

    Returns:
        A dictionary where keys are object indices and values are sets of
        indices of adjacent objects.
    """
    rows, cols = grid_shape
    adjacency = collections.defaultdict(set)

    for obj_idx, cells in enumerate(objects):
        for r, c in cells:
            # Check orthogonal neighbors
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    neighbor_coord = (nr, nc)
                    if neighbor_coord in object_map:
                        neighbor_obj_idx = object_map[neighbor_coord]
                        if neighbor_obj_idx != obj_idx:
                            adjacency[obj_idx].add(neighbor_obj_idx)
                            # Adjacency is symmetric, but defaultdict handles this
                            # adjacency[neighbor_obj_idx].add(obj_idx) 
    return adjacency


def transform(input_grid):
    """
    Transforms the input grid by removing objects touching the top border
    and any objects connected to them via orthogonal adjacency.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed grid.
    """
    # Convert input to numpy array for easier processing
    input_arr = np.array(input_grid, dtype=int)
    rows, cols = input_arr.shape
    
    # Initialize output grid as a copy of the input
    output_arr = np.copy(input_arr)

    # 1. Identify all distinct connected components (objects)
    objects, object_map = find_objects(input_arr)
    if not objects: # Handle empty grid or grid with only 0s
        return output_arr.tolist()

    # 2. & 3. Identify objects touching the top border
    objects_to_remove_indices = set()
    initial_remove_queue = collections.deque()

    for i, obj_cells in enumerate(objects):
        for r, c in obj_cells:
            if r == 0:
                objects_to_remove_indices.add(i)
                initial_remove_queue.append(i)
                break # Once one cell touches the top, the whole object is marked

    # 4. Build adjacency map between objects
    adjacency = get_object_adjacency(objects, object_map, (rows, cols))

    # 5. Iteratively find adjacent objects to remove
    queue = initial_remove_queue
    processed_for_neighbors = set(initial_remove_queue) # Keep track of objects whose neighbors we've checked

    while queue:
        current_obj_idx = queue.popleft()
        
        # Find neighbors of the current object
        for neighbor_idx in adjacency.get(current_obj_idx, set()):
            # If the neighbor hasn't been marked for removal yet
            if neighbor_idx not in objects_to_remove_indices:
                objects_to_remove_indices.add(neighbor_idx)
                # Add to queue to process its neighbors later
                if neighbor_idx not in processed_for_neighbors:
                     queue.append(neighbor_idx)
                     processed_for_neighbors.add(neighbor_idx)

    # 6. & 7. Modify the output grid: Set cells of removed objects to 0
    for obj_idx in objects_to_remove_indices:
        for r, c in objects[obj_idx]:
            output_arr[r, c] = 0

    # 8. Return the modified grid as a list of lists
    return output_arr.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1
0 0 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1
0 2 2 2 0 0 2 2 2 0 0 0 0 2 2 2 0 0 0 0
0 2 2 2 0 0 2 2 2 0 0 0 0 2 2 2 0 0 0 0
0 2 2 2 0 0 2 2 2 0 0 0 0 2 2 2 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0 0 0 2 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 0 0 0 4 4 4 0 0 0 0 0 0 0 0
0 0 0 4 4 4 0 0 0 4 4 4 0 0 0 0 0 0 0 0
0 0 0 4 4 4 0 0 0 4 4 4 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 0 0 0 4 4 4 0 0 0 0 0 0 0 0
0 0 0 4 4 4 0 0 0 4 4 4 0 0 0 0 0 0 0 0
0 0 0 4 4 4 0 0 0 4 4 4 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 2 2 2 0 0 0 0 2 2 2 0 0 0 0
0 2 2 2 0 0 2 2 2 0 0 0 0 2 2 2 0 0 0 0
0 2 2 2 0 0 2 2 2 0 0 0 0 2 2 2 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0 0 0 2 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 0 0 0 4 4 4 0 0 0 0 0 0 0 0
0 0 0 4 4 4 0 0 0 4 4 4 0 0 0 0 0 0 0 0
0 0 0 4 4 4 0 0 0 4 4 4 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 33
Size Correct: True
Color Palette Correct: False
Color Count Correct: False
Score: 36.666666666666686

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 2 2 2 0 0
0 0 0 4 4 4 0 0 0 0 0 2 2 2 0 0
0 0 0 4 4 4 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 0
0 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2
0 0 0 0 0 0 2 2 2 0 0 0 2 2 2 2
0 0 0 0 0 0 2 2 2 0 0 0 2 2 2 2
0 0 0 0 0 0 2 2 2 0 0 0 2 2 2 2
2 2 2 0 0 0 0 0 0 0 0 0 2 2 2 2
2 2 2 0 0 0 0 0 0 0 0 0 2 2 2 2
2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 0
0 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2
0 0 0 0 0 0 2 2 2 0 0 0 2 2 2 2
0 0 0 0 0 0 2 2 2 0 0 0 2 2 2 2
0 0 0 0 0 0 2 2 2 0 0 0 2 2 2 2
2 2 2 0 0 0 0 0 0 0 0 0 2 2 2 2
2 2 2 0 0 0 0 0 0 0 0 0 2 2 2 2
2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 0
0 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2
0 0 0 0 0 0 2 2 2 0 0 0 2 2 2 2
0 0 0 0 0 0 2 2 2 0 0 0 2 2 2 2
0 0 0 0 0 0 2 2 2 0 0 0 2 2 2 2
2 2 2 0 0 0 0 0 0 0 0 0 2 2 2 2
2 2 2 0 0 0 0 0 0 0 0 0 2 2 2 2
2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 6
Size Correct: True
Color Palette Correct: False
Color Count Correct: False
Score: 7.5

## Example 3:
Input:
```
0 0 0 8 8 8 0
0 0 0 8 8 8 0
0 0 0 8 8 8 0
0 0 0 0 0 0 0
0 0 7 7 7 0 0
0 0 7 7 7 0 0
0 0 7 7 7 0 0
0 0 0 0 0 0 0
7 7 7 7 0 8 8
7 7 7 7 0 8 8
0 0 0 0 0 0 0
0 0 0 0 3 3 3
0 0 0 0 3 3 3
0 0 0 0 3 3 3
0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 3 3 3
0 0 0 0 3 3 3
0 0 0 0 3 3 3
0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 7 7 7 0 0
0 0 7 7 7 0 0
0 0 7 7 7 0 0
0 0 0 0 0 0 0
7 7 7 7 0 8 8
7 7 7 7 0 8 8
0 0 0 0 0 0 0
0 0 0 0 3 3 3
0 0 0 0 3 3 3
0 0 0 0 3 3 3
0 0 0 0 0 0 0
```
Match: False
Pixels Off: 21
Size Correct: True
Color Palette Correct: False
Color Count Correct: False
Score: 80.0

Test Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0
6 6 0 0 0 6 6 0 0 0
6 6 0 0 0 6 6 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 3 0 0 0 0
0 0 0 3 3 3 0 0 0 0
0 0 0 3 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 6 6 0 0 0 0 0
0 0 0 6 6 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 3 0 0 0 0
0 0 0 3 3 3 0 0 0 0
0 0 0 3 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 6 6 0 0 0 0 0
0 0 0 6 6 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0
6 6 0 0 0 6 6 0 0 0
6 6 0 0 0 6 6 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 3 0 0 0 0
0 0 0 3 3 3 0 0 0 0
0 0 0 3 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 6 6 0 0 0 0 0
0 0 0 6 6 0 0 0 0 0
```
Match: False
Pixels Off: 8
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 16.0

## Example 2:
Input:
```
0 0 0 0 0 0 0 2 2 2 2
0 2 2 2 0 0 0 2 2 2 2
0 2 2 2 0 0 0 2 2 2 2
0 2 2 2 0 0 0 2 2 2 2
0 2 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
3 3 0 0 0 0 0 0 0 0 0
3 3 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
3 3 0 0 0 0 0 0 0 0 0
3 3 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
3 3 0 0 0 0 0 0 0 0 0
3 3 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 12
Size Correct: True
Color Palette Correct: False
Color Count Correct: False
Score: 43.636363636363626

## Example 3:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 0 0 0 0 0 0 0 0
0 0 5 5 5 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 5 5 0
0 0 0 0 0 0 0 0 0 0 0 5 5 0
0 0 0 0 0 0 0 0 0 0 0 3 3 0
0 0 0 0 0 0 0 0 0 0 0 3 3 0
0 0 0 0 0 0 5 5 5 5 0 5 5 0
0 0 0 0 0 0 5 5 5 5 0 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 3 3 0
0 0 0 0 0 0 0 0 0 0 0 3 3 0
0 0 0 0 0 0 5 5 5 5 0 5 5 0
0 0 0 0 0 0 5 5 5 5 0 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 0 0 0 0 0 0 0 0
0 0 5 5 5 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 5 5 0
0 0 0 0 0 0 0 0 0 0 0 5 5 0
0 0 0 0 0 0 0 0 0 0 0 3 3 0
0 0 0 0 0 0 0 0 0 0 0 3 3 0
0 0 0 0 0 0 5 5 5 5 0 5 5 0
0 0 0 0 0 0 5 5 5 5 0 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 12
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 13.186813186813197
