
Previous Code:
```python
import numpy as np
from collections import deque

"""
Identifies blue (1) objects in the input grid and determines whether to change their color to red (2) based on two conditions:
1. Whether the blue object encloses any white (0) pixels.
2. Whether the blue object is adjacent (8-way connectivity) to any original red (2) object.

The transformation rule is:
- If a blue object encloses white pixels AND is NOT adjacent to any red object, it changes to red.
- If a blue object does NOT enclose white pixels AND IS adjacent to at least one red object, it changes to red.
- Otherwise, the blue object remains blue.
- Original red objects and all other pixels remain unchanged.
"""

def find_objects(grid, color):
    """
    Finds all contiguous objects of a specified color in the grid.

    Args:
        grid (np.ndarray): The input grid.
        color (int): The color of the objects to find.

    Returns:
        dict: A dictionary where keys are object IDs (starting from 1)
              and values are lists of (row, col) tuples for pixels
              belonging to that object.
    """
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    objects = {}
    object_id = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                object_id += 1
                obj_pixels = []
                q = deque([(r, c)])
                visited[r, c] = True
                while q:
                    row, col = q.popleft()
                    obj_pixels.append((row, col))
                    # Check 8 neighbors
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = row + dr, col + dc
                            if 0 <= nr < rows and 0 <= nc < cols and \
                               grid[nr, nc] == color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                if obj_pixels:
                    objects[object_id] = obj_pixels
    return objects

def get_all_object_pixels(objects_dict):
    """
    Gets a set of all pixel coordinates from an objects dictionary.

    Args:
        objects_dict (dict): Dictionary returned by find_objects.

    Returns:
        set: A set of (row, col) tuples.
    """
    all_pixels = set()
    for pixels in objects_dict.values():
        all_pixels.update(pixels)
    return all_pixels

def is_adjacent(obj_pixels, target_pixels_set, grid_shape):
    """
    Checks if any pixel in obj_pixels is adjacent (8-way) to any pixel
    in target_pixels_set.

    Args:
        obj_pixels (list): List of (row, col) tuples for the object.
        target_pixels_set (set): Set of (row, col) tuples for target adjacent pixels.
        grid_shape (tuple): (rows, cols) of the grid.

    Returns:
        bool: True if adjacent, False otherwise.
    """
    rows, cols = grid_shape
    for r, c in obj_pixels:
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    if (nr, nc) in target_pixels_set:
                        return True
    return False

def encloses_white_pixels(obj_pixels, grid):
    """
    Checks if a blue object encloses white (0) pixels.

    Determines this by checking if any white pixel adjacent to the object
    cannot reach the grid border via other white pixels.

    Args:
        obj_pixels (list): List of (row, col) tuples for the blue object.
        grid (np.ndarray): The input grid.

    Returns:
        bool: True if the object encloses white pixels, False otherwise.
    """
    rows, cols = grid.shape
    obj_pixels_set = set(obj_pixels)
    
    # 1. Find all white pixels reachable from the border
    reachable_white = np.zeros_like(grid, dtype=bool)
    q = deque()
    
    # Add border white pixels to queue
    for r in range(rows):
        if grid[r, 0] == 0: q.append((r, 0)); reachable_white[r, 0] = True
        if grid[r, cols-1] == 0: q.append((r, cols-1)); reachable_white[r, cols-1] = True
    for c in range(cols):
        if grid[0, c] == 0: q.append((0, c)); reachable_white[0, c] = True
        if grid[rows-1, c] == 0: q.append((rows-1, c)); reachable_white[rows-1, c] = True
        
    # Perform BFS for reachable white pixels (4-way is sufficient)
    while q:
        r, c = q.popleft()
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and \
               grid[nr, nc] == 0 and not reachable_white[nr, nc]:
               reachable_white[nr, nc] = True
               q.append((nr, nc))

    # 2. Find white pixels adjacent (8-way) to the blue object
    adjacent_white_pixels = set()
    for r, c in obj_pixels:
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                # Check bounds and if it's a white pixel NOT part of the object itself
                if 0 <= nr < rows and 0 <= nc < cols and \
                   grid[nr, nc] == 0 and (nr, nc) not in obj_pixels_set:
                   adjacent_white_pixels.add((nr, nc))

    # 3. Check if any adjacent white pixel is NOT reachable from the border
    for r, c in adjacent_white_pixels:
        if not reachable_white[r, c]:
            # Found an enclosed white pixel adjacent to the object
            return True
            
    # If we checked all adjacent white pixels and all were reachable, it doesn't enclose.
    return False


def transform(input_grid):
    """
    Transforms the input grid by changing specific blue objects to red based on enclosure and adjacency rules.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find original red objects and their pixels
    red_objects = find_objects(input_grid, 2)
    all_red_pixels = get_all_object_pixels(red_objects)

    # Find blue objects
    blue_objects = find_objects(input_grid, 1)

    # Iterate through each blue object
    for obj_id, blue_obj_pixels in blue_objects.items():
        # Determine if the object encloses white pixels
        encloses_white = encloses_white_pixels(blue_obj_pixels, input_grid)

        # Determine if the object is adjacent to any original red object
        adjacent_to_red = is_adjacent(blue_obj_pixels, all_red_pixels, (rows, cols))

        # Apply the transformation rule
        change_to_red = False
        if encloses_white and not adjacent_to_red:
            change_to_red = True
        elif not encloses_white and adjacent_to_red:
            change_to_red = True

        # If the condition is met, change the object's color in the output grid
        if change_to_red:
            for r, c in blue_obj_pixels:
                output_grid[r, c] = 2 # Change to red

    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
2 2 2 0 0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 1 1 1 0 1 0 1
2 2 2 0 0 0 0 0 1 0 1 0 1 1 1
0 0 0 0 0 0 0 0 1 0 1 0 1 0 1
0 0 0 0 0 0 0 0 1 0 1 0 1 0 1
0 1 0 1 0 0 0 0 0 0 0 0 0 0 0
0 1 0 1 0 1 0 1 0 0 0 0 0 0 0
0 1 1 1 0 1 0 1 0 0 0 0 0 0 0
0 0 0 0 0 1 1 1 0 0 1 1 1 1 0
0 0 0 0 0 1 0 1 0 0 0 0 0 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0 1 0
0 0 0 0 0 0 0 0 0 0 1 1 1 1 0
0 1 1 1 1 0 0 0 0 0 0 0 0 0 0
0 0 1 0 1 0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
2 2 2 0 0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 2 2 2 0 1 0 1
2 2 2 0 0 0 0 0 2 0 2 0 1 1 1
0 0 0 0 0 0 0 0 2 0 2 0 1 0 1
0 0 0 0 0 0 0 0 2 0 2 0 1 0 1
0 2 0 2 0 0 0 0 0 0 0 0 0 0 0
0 2 0 2 0 1 0 1 0 0 0 0 0 0 0
0 2 2 2 0 1 0 1 0 0 0 0 0 0 0
0 0 0 0 0 1 1 1 0 0 2 2 2 2 0
0 0 0 0 0 1 0 1 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0 0 2 2 2 2 0
0 1 1 1 1 0 0 0 0 0 0 0 0 0 0
0 0 1 0 1 0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
2 2 2 0 0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 1 1 1 0 1 0 1
2 2 2 0 0 0 0 0 1 0 1 0 1 1 1
0 0 0 0 0 0 0 0 1 0 1 0 1 0 1
0 0 0 0 0 0 0 0 1 0 1 0 1 0 1
0 1 0 1 0 0 0 0 0 0 0 0 0 0 0
0 1 0 1 0 1 0 1 0 0 0 0 0 0 0
0 1 1 1 0 1 0 1 0 0 0 0 0 0 0
0 0 0 0 0 1 1 1 0 0 1 1 1 1 0
0 0 0 0 0 1 0 1 0 0 0 0 0 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0 1 0
0 0 0 0 0 0 0 0 0 0 1 1 1 1 0
0 2 2 2 2 0 0 0 0 0 0 0 0 0 0
0 0 2 0 2 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 36
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 32.0

## Example 2:
Input:
```
2 0 2 0 0 0 0 0 0 0 0 0 0 1 0 1 0 0
2 2 2 0 0 0 0 0 0 0 0 0 0 1 1 1 0 0
2 0 2 0 0 0 0 0 0 0 0 0 0 1 0 1 0 0
0 0 0 0 0 1 1 1 1 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 1 1 1 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0 1 1 0 0 0 0 0
1 1 1 1 1 1 1 0 0 0 0 0 1 1 1 0 0 0
0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 1 0 0 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 1 1 1 1 0 1 0 0 0
0 0 1 1 1 0 0 0 0 1 0 0 1 0 1 1 1 1
0 0 1 0 1 0 0 0 0 0 0 0 0 0 1 0 0 0
0 0 1 0 1 0 0 0 0 0 0 0 0 0 1 1 1 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0
```
Expected Output:
```
2 0 2 0 0 0 0 0 0 0 0 0 0 2 0 2 0 0
2 2 2 0 0 0 0 0 0 0 0 0 0 2 2 2 0 0
2 0 2 0 0 0 0 0 0 0 0 0 0 2 0 2 0 0
0 0 0 0 0 2 2 2 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0 1 1 0 0 0 0 0
2 2 2 2 2 2 2 0 0 0 0 0 1 1 1 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2 2 2 2 0 1 0 0 0
0 0 1 1 1 0 0 0 0 2 0 0 2 0 1 1 1 1
0 0 1 0 1 0 0 0 0 0 0 0 0 0 1 0 0 0
0 0 1 0 1 0 0 0 0 0 0 0 0 0 1 1 1 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0
```
Transformed Output:
```
2 0 2 0 0 0 0 0 0 0 0 0 0 1 0 1 0 0
2 2 2 0 0 0 0 0 0 0 0 0 0 1 1 1 0 0
2 0 2 0 0 0 0 0 0 0 0 0 0 1 0 1 0 0
0 0 0 0 0 1 1 1 1 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 1 1 1 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0 1 1 0 0 0 0 0
1 1 1 1 1 1 1 0 0 0 0 0 1 1 1 0 0 0
0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 1 0 0 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 1 1 1 1 0 1 0 0 0
0 0 1 1 1 0 0 0 0 1 0 0 1 0 1 1 1 1
0 0 1 0 1 0 0 0 0 0 0 0 0 0 1 0 0 0
0 0 1 0 1 0 0 0 0 0 0 0 0 0 1 1 1 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0
```
Match: False
Pixels Off: 42
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 25.925925925925924

## Example 3:
Input:
```
2 2 2 0 0 0 0 0 0 0 0 0 0 1 0 1 0 0
2 0 2 0 0 0 0 0 0 0 0 0 0 1 1 1 0 0
2 2 2 0 0 0 0 0 0 0 0 0 0 1 0 1 0 0
0 0 0 0 0 0 0 0 1 1 1 0 0 0 0 0 0 0
0 0 1 1 1 0 0 0 1 0 1 0 0 0 0 0 0 0
0 0 0 0 1 0 0 0 1 0 1 0 0 0 0 0 0 0
0 0 1 1 1 0 0 0 1 1 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 0 1 0 0 0 1 1 1 0 0 0 1 1 1 0
0 1 1 1 1 0 0 0 1 0 1 0 0 0 1 0 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 1 1 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 0 0 1 0 0 1 0 0 1 0 0 0 0
0 0 0 0 1 0 0 1 0 0 1 1 1 1 0 0 0 0
0 0 0 0 1 1 1 1 0 0 1 0 0 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0 1 0 0 1 0 0 0 0
```
Expected Output:
```
2 2 2 0 0 0 0 0 0 0 0 0 0 1 0 1 0 0
2 0 2 0 0 0 0 0 0 0 0 0 0 1 1 1 0 0
2 2 2 0 0 0 0 0 0 0 0 0 0 1 0 1 0 0
0 0 0 0 0 0 0 0 2 2 2 0 0 0 0 0 0 0
0 0 1 1 1 0 0 0 2 0 2 0 0 0 0 0 0 0
0 0 0 0 1 0 0 0 2 0 2 0 0 0 0 0 0 0
0 0 1 1 1 0 0 0 2 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 2 0 0 0 1 1 1 0 0 0 2 2 2 0
0 2 2 2 2 0 0 0 1 0 1 0 0 0 2 0 2 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 2 2 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 2 0 0 1 0 0 1 0 0 0 0
0 0 0 0 2 0 0 2 0 0 1 1 1 1 0 0 0 0
0 0 0 0 2 2 2 2 0 0 1 0 0 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0 1 0 0 1 0 0 0 0
```
Transformed Output:
```
2 2 2 0 0 0 0 0 0 0 0 0 0 1 0 1 0 0
2 0 2 0 0 0 0 0 0 0 0 0 0 1 1 1 0 0
2 2 2 0 0 0 0 0 0 0 0 0 0 1 0 1 0 0
0 0 0 0 0 0 0 0 2 2 2 0 0 0 0 0 0 0
0 0 1 1 1 0 0 0 2 0 2 0 0 0 0 0 0 0
0 0 0 0 1 0 0 0 2 0 2 0 0 0 0 0 0 0
0 0 1 1 1 0 0 0 2 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 2 0 0 0 1 1 1 0 0 0 2 2 2 0
0 2 2 2 2 0 0 0 1 0 1 0 0 0 2 0 2 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 2 2 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 2 0 0 1 0 0 1 0 0 0 0
0 0 0 0 2 0 0 2 0 0 1 1 1 1 0 0 0 0
0 0 0 0 2 2 2 2 0 0 1 0 0 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0 1 0 0 1 0 0 0 0
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0
