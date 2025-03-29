
Previous Code:
```python
import numpy as np
from collections import deque

"""
This program transforms an input grid based on the following rules:

1. Identify all contiguous objects composed of blue pixels (color 1). These are 'target objects'.
2. Identify all pixels that are not white (color 0) and not blue (color 1). These are 'source pixels'.
3. For each target object:
    a. Calculate the minimum Manhattan distance from any pixel within the target object to any source pixel.
    b. Find all source pixels that are at this minimum distance from *any* pixel in the target object.
    c. Among these closest source pixels, determine their colors.
    d. Select the color with the lowest numerical index among these closest source pixel colors.
    e. Recolor all pixels of the target object in the output grid with this selected color.
4. Pixels that are not part of a blue target object remain unchanged in the output grid.
5. If there are no source pixels, the grid remains unchanged.
"""

def find_objects(grid, target_color):
    """
    Finds all contiguous objects of a specific color in the grid.

    Args:
        grid (np.ndarray): The input grid.
        target_color (int): The color of the objects to find.

    Returns:
        list[set]: A list where each element is a set of (row, col) tuples
                   representing the coordinates of one object.
    """
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == target_color and not visited[r, c]:
                # Start BFS to find a new object
                current_object = set()
                q = deque([(r, c)])
                visited[r, c] = True
                current_object.add((r, c))

                while q:
                    curr_r, curr_c = q.popleft()

                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc

                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == target_color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            current_object.add((nr, nc))
                
                if current_object:
                    objects.append(current_object)
    return objects

def calculate_manhattan_distance(p1, p2):
    """Calculates Manhattan distance between two points."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def transform(input_grid):
    """
    Transforms the input grid by recoloring blue objects based on the nearest
    non-white, non-blue source pixel, using the minimum color index as a tie-breaker.

    Args:
        input_grid (list[list[int]]): The input grid.

    Returns:
        list[list[int]]: The transformed grid.
    """
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy()
    rows, cols = grid.shape

    # 1. Identify source pixels (non-white, non-blue)
    source_pixels = []
    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if color != 0 and color != 1:
                source_pixels.append(((r, c), color))

    # If no source pixels, return the original grid
    if not source_pixels:
        return output_grid.tolist()

    # 2. Identify target objects (blue color 1)
    target_objects = find_objects(grid, 1)

    # 3. Process each target object
    for obj_coords in target_objects:
        min_overall_distance = float('inf')
        potential_colors = [] # Stores colors of sources at min_overall_distance

        # a. Find the minimum distance between any pixel in this object and any source pixel
        for target_r, target_c in obj_coords:
            for source_pos, source_color in source_pixels:
                dist = calculate_manhattan_distance((target_r, target_c), source_pos)
                min_overall_distance = min(min_overall_distance, dist)

        # b. Find all source colors that are at this minimum distance
        for target_r, target_c in obj_coords:
            for source_pos, source_color in source_pixels:
                dist = calculate_manhattan_distance((target_r, target_c), source_pos)
                if dist == min_overall_distance:
                    potential_colors.append(source_color)
        
        # c. Determine the final color (minimum color index if tie)
        if potential_colors:
            final_color = min(potential_colors)

            # d. Recolor the object in the output grid
            for r, c in obj_coords:
                output_grid[r, c] = final_color

    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
1 1 0 0 1 1 0 0 0 0 0 0 0 0 0 0 0 0
1 0 1 0 1 0 1 0 0 0 0 0 0 0 0 0 0 0
0 1 1 0 0 1 1 0 0 0 0 0 0 0 2 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 3 0
1 1 0 0 0 0 0 0 1 1 0 0 0 0 0 3 2 0
1 0 1 0 0 0 0 0 1 0 1 0 0 0 0 0 0 0
0 1 1 0 0 0 0 0 0 1 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 1 0 0 1 1 0 0 0 0 0 0 0 0
0 0 0 0 1 0 1 0 1 0 1 0 0 0 0 0 0 0
0 0 0 0 0 1 1 0 0 1 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
2 2 0 0 3 3 0 0 0 0 0 0 0 0 0 0 0 0
2 0 2 0 3 0 3 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 3 3 0 0 0 0 0 0 0 2 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 3 0
3 3 0 0 0 0 0 0 3 3 0 0 0 0 0 3 2 0
3 0 3 0 0 0 0 0 3 0 3 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 3 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 0 0 2 2 0 0 0 0 0 0 0 0
0 0 0 0 3 0 3 0 2 0 2 0 0 0 0 0 0 0
0 0 0 0 0 3 3 0 0 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
2 2 0 0 2 2 0 0 0 0 0 0 0 0 0 0 0 0
2 0 2 0 2 0 2 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 2 2 0 0 0 0 0 0 0 2 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 3 0
3 3 0 0 0 0 0 0 3 3 0 0 0 0 0 3 2 0
3 0 3 0 0 0 0 0 3 0 3 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 3 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 0 0 3 3 0 0 0 0 0 0 0 0
0 0 0 0 3 0 3 0 3 0 3 0 0 0 0 0 0 0
0 0 0 0 0 3 3 0 0 3 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 12
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 5.555555555555557

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 1 0 1 1 0 0
0 0 0 0 0 1 0 0 1 0 0 0
0 2 4 0 0 0 0 0 0 0 0 0
0 3 0 0 0 1 1 0 0 0 0 0
0 0 0 0 0 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 0 4 4 0 0
0 0 0 0 0 2 0 0 4 0 0 0
0 2 4 0 0 0 0 0 0 0 0 0
0 3 0 0 0 3 3 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 4 0 4 4 0 0
0 0 0 0 0 4 0 0 4 0 0 0
0 2 4 0 0 0 0 0 0 0 0 0
0 3 0 0 0 3 3 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 3
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 5.0
