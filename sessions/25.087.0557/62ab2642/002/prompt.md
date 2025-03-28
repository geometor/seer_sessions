
Previous Code:
```python
import copy
from collections import deque

"""
Identify all distinct connected objects composed of gray (5) pixels in the input grid.
If there are fewer than two gray objects, return the input grid unchanged.
Otherwise, determine the leftmost gray object (the one containing the pixel with the minimum column index) and the rightmost gray object (the one containing the pixel with the maximum column index).
Find all white (0) pixels that are adjacent (including diagonals) to any pixel of the leftmost gray object. Change these white pixels to orange (7) in the output grid.
Find all white (0) pixels that are adjacent (including diagonals) to any pixel of the rightmost gray object. Change these white pixels to azure (8) in the output grid.
If a white pixel is adjacent to both the leftmost and rightmost objects, it should be changed to azure (8) (azure takes precedence).
All other pixels retain their original color.
"""

def find_objects(grid, color):
    """
    Finds all connected objects of a specific color in the grid.

    Args:
        grid: The input grid (list of lists).
        color: The color of the objects to find.

    Returns:
        A list of objects, where each object is a list of (row, col) tuples.
    """
    height = len(grid)
    width = len(grid[0])
    visited = set()
    objects = []

    for r in range(height):
        for c in range(width):
            if grid[r][c] == color and (r, c) not in visited:
                obj = []
                q = deque([(r, c)])
                visited.add((r, c))
                while q:
                    row, col = q.popleft()
                    obj.append((row, col))
                    # Check 8 neighbors (including diagonals)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = row + dr, col + dc
                            if 0 <= nr < height and 0 <= nc < width and \
                               grid[nr][nc] == color and (nr, nc) not in visited:
                                visited.add((nr, nc))
                                q.append((nr, nc))
                if obj:
                    objects.append(obj)
    return objects

def get_object_bounds(obj):
    """
    Calculates the minimum and maximum column index for an object.

    Args:
        obj: A list of (row, col) tuples representing an object.

    Returns:
        A tuple (min_col, max_col). Returns (float('inf'), float('-inf')) if obj is empty.
    """
    if not obj:
        return float('inf'), float('-inf')
    min_c = min(c for r, c in obj)
    max_c = max(c for r, c in obj)
    return min_c, max_c

def transform(input_grid):
    """
    Transforms the input grid based on the described rules.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the output grid.
    """
    output_grid = copy.deepcopy(input_grid)
    height = len(input_grid)
    width = len(input_grid[0])
    
    # Find all gray objects
    gray_objects = find_objects(input_grid, 5)

    # If less than two objects, return the original grid
    if len(gray_objects) < 2:
        return output_grid

    # Find the leftmost and rightmost objects
    min_col_overall = float('inf')
    max_col_overall = float('-inf')
    leftmost_object = None
    rightmost_object = None

    object_bounds = []
    for obj in gray_objects:
        min_c, max_c = get_object_bounds(obj)
        object_bounds.append({'object': obj, 'min_c': min_c, 'max_c': max_c})
        if min_c < min_col_overall:
            min_col_overall = min_c
            leftmost_object = obj
        if max_c > max_col_overall:
            max_col_overall = max_c
            # Need to find the object whose max_c is max_col_overall
            # It might not be the same one that set the current max_col_overall if multiple objects share the max column

    # Re-iterate to definitively find the rightmost object based on max_col_overall
    for bounds in object_bounds:
        if bounds['max_c'] == max_col_overall:
            rightmost_object = bounds['object']
            break # Assuming only one truly rightmost object matters if columns tie

    # Find neighbors to color orange (leftmost)
    orange_neighbors = set()
    if leftmost_object:
        for r_obj, c_obj in leftmost_object:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = r_obj + dr, c_obj + dc
                    if 0 <= nr < height and 0 <= nc < width and input_grid[nr][nc] == 0:
                        orange_neighbors.add((nr, nc))

    # Find neighbors to color azure (rightmost)
    azure_neighbors = set()
    if rightmost_object:
        for r_obj, c_obj in rightmost_object:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = r_obj + dr, c_obj + dc
                    if 0 <= nr < height and 0 <= nc < width and input_grid[nr][nc] == 0:
                        azure_neighbors.add((nr, nc))

    # Apply color changes (orange first, then azure to handle precedence)
    for r, c in orange_neighbors:
        output_grid[r][c] = 7
        
    for r, c in azure_neighbors:
        output_grid[r][c] = 8

    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
5 0 0 5 0
5 0 0 5 0
5 0 5 5 5
5 5 5 0 0
0 0 5 0 0
0 0 5 5 5
0 0 0 5 0
5 5 5 5 0
0 5 0 0 0
0 5 0 0 0
0 5 5 5 0
0 0 0 5 0
0 5 5 5 5
5 5 0 0 0
0 5 0 0 0
```
Expected Output:
```
5 0 0 5 0
5 0 0 5 0
5 0 5 5 5
5 5 5 0 0
0 0 5 0 0
0 0 5 5 5
0 0 0 5 8
5 5 5 5 8
0 5 8 8 8
0 5 8 8 8
0 5 5 5 8
0 0 0 5 8
0 5 5 5 5
5 5 0 0 0
7 5 0 0 0
```
Transformed Output:
```
5 0 0 5 0
5 0 0 5 0
5 0 5 5 5
5 5 5 0 0
0 0 5 0 0
0 0 5 5 5
0 0 0 5 0
5 5 5 5 0
0 5 0 0 0
0 5 0 0 0
0 5 5 5 0
0 0 0 5 0
0 5 5 5 5
5 5 0 0 0
0 5 0 0 0
```
Match: False
Pixels Off: 11
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 29.333333333333314

## Example 2:
Input:
```
0 0 5 0 0 5 0 0 0
0 0 5 5 5 5 0 0 0
5 5 5 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0
0 5 0 0 0 5 5 5 5
0 5 5 5 5 5 0 0 0
5 5 0 0 0 5 5 5 5
0 0 0 0 0 5 0 0 0
5 5 5 5 5 5 0 0 0
0 0 0 0 0 5 0 0 0
```
Expected Output:
```
0 0 5 7 7 5 8 8 8
0 0 5 5 5 5 8 8 8
5 5 5 8 8 8 8 8 8
0 5 8 8 8 8 8 8 8
0 5 8 8 8 5 5 5 5
0 5 5 5 5 5 0 0 0
5 5 0 0 0 5 5 5 5
0 0 0 0 0 5 0 0 0
5 5 5 5 5 5 0 0 0
0 0 0 0 0 5 0 0 0
```
Transformed Output:
```
0 0 5 0 0 5 0 0 0
0 0 5 5 5 5 0 0 0
5 5 5 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0
0 5 0 0 0 5 5 5 5
0 5 5 5 5 5 0 0 0
5 5 0 0 0 5 5 5 5
0 0 0 0 0 5 0 0 0
5 5 5 5 5 5 0 0 0
0 0 0 0 0 5 0 0 0
```
Match: False
Pixels Off: 24
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 53.33333333333334

## Example 3:
Input:
```
0 5 0 0 5 0 0 0 0 5 0 0
0 5 0 0 5 5 5 0 0 5 0 0
0 5 5 5 5 0 5 0 0 5 0 0
0 0 5 0 0 0 5 5 5 5 0 0
5 5 5 0 0 0 5 0 0 5 5 5
0 0 0 0 0 0 5 0 0 0 0 0
0 0 0 5 5 5 5 0 0 0 0 0
5 5 5 5 0 0 5 0 0 0 0 0
0 0 0 5 0 0 5 5 5 0 0 0
0 0 0 5 0 0 0 0 5 0 0 0
```
Expected Output:
```
0 5 7 7 5 0 0 0 0 5 0 0
0 5 7 7 5 5 5 0 0 5 0 0
0 5 5 5 5 0 5 0 0 5 0 0
0 0 5 0 0 0 5 5 5 5 0 0
5 5 5 0 0 0 5 8 8 5 5 5
0 0 0 0 0 0 5 8 8 8 8 8
0 0 0 5 5 5 5 8 8 8 8 8
5 5 5 5 0 0 5 8 8 8 8 8
0 0 0 5 0 0 5 5 5 8 8 8
0 0 0 5 0 0 0 0 5 8 8 8
```
Transformed Output:
```
0 5 0 0 5 0 0 0 0 5 0 0
0 5 0 0 5 5 5 0 0 5 0 0
0 5 5 5 5 0 5 0 0 5 0 0
0 0 5 0 0 0 5 5 5 5 0 0
5 5 5 0 0 0 5 0 0 5 5 5
0 0 0 0 0 0 5 0 0 0 0 0
0 0 0 5 5 5 5 0 0 0 0 0
5 5 5 5 0 0 5 0 0 0 0 0
0 0 0 5 0 0 5 5 5 0 0 0
0 0 0 5 0 0 0 0 5 0 0 0
```
Match: False
Pixels Off: 27
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 45.0
