
Previous Code:
```python
import numpy as np
from collections import deque

"""
Transforms the input grid by recoloring azure (8) objects based on their size rank.

1. Identifies all distinct connected components (objects) of azure (8) pixels.
2. Calculates the size (pixel count) and top-left coordinate for each object.
3. Sorts the objects based primarily on size (ascending) and secondarily on their 
   top-left coordinate (top-to-bottom, then left-to-right).
4. Determines a specific color sequence based on the total number of objects found (M).
   - M=4: [Green(3), Green(3), Orange(7), Orange(7)]
   - M=5: [Red(2), Blue(1), Red(2), Blue(1), Green(3)]
   - M=6: [Blue(1), Red(2), Red(2), Red(2), Green(3), Orange(7)]
5. Recolors each object in the output grid according to its rank in the sorted list, 
   using the determined color sequence.
"""

def find_objects(grid, color_code):
    """
    Finds all connected components of a specific color in the grid.

    Args:
        grid (np.ndarray): The input grid.
        color_code (int): The color code of the objects to find.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              with keys 'pixels' (set of (r, c) tuples), 'size' (int),
              and 'top_left' ((r, c) tuple).
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    
    # Define 8 neighbors (including diagonals)
    neighbors = [(-1, -1), (-1, 0), (-1, 1),
                 (0, -1),           (0, 1),
                 (1, -1), (1, 0), (1, 1)]

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color_code and not visited[r, c]:
                # Start BFS for a new object
                obj_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c # Track top-left

                while q:
                    row, col = q.popleft()
                    obj_pixels.add((row, col))
                    
                    # Update top-left coordinate
                    if row < min_r:
                        min_r, min_c = row, col
                    elif row == min_r and col < min_c:
                        min_c = col

                    # Explore neighbors
                    for dr, dc in neighbors:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color_code and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                objects.append({
                    'pixels': obj_pixels,
                    'size': len(obj_pixels),
                    'top_left': (min_r, min_c)
                })
                
    return objects

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    
    # 1. Identify all azure (8) objects
    azure_objects = find_objects(input_grid_np, 8)
    
    # 2. Get the number of objects
    M = len(azure_objects)
    
    if M == 0:
        return input_grid # No objects to transform

    # 3. Sort the objects by size (asc), then top-left row (asc), then top-left col (asc)
    sorted_objects = sorted(azure_objects, key=lambda obj: (obj['size'], obj['top_left'][0], obj['top_left'][1]))
    
    # 4. Determine the color sequence based on M
    color_sequence = []
    if M == 4:
        # Green, Green, Orange, Orange
        color_sequence = [3, 3, 7, 7]
    elif M == 5:
        # Red, Blue, Red, Blue, Green
        color_sequence = [2, 1, 2, 1, 3]
    elif M == 6:
        # Blue, Red, Red, Red, Green, Orange
        color_sequence = [1, 2, 2, 2, 3, 7]
    else:
        # Handle cases not seen in training data - maybe return input or raise error?
        # For now, let's just return the input if M is unexpected.
        print(f"Warning: Unexpected number of objects M={M}. No transformation applied.")
        return input_grid

    # 5. Create the output grid as a copy
    output_grid = np.copy(input_grid_np)
    
    # 6. Iterate through sorted objects and assign colors
    for i, obj in enumerate(sorted_objects):
        target_color = color_sequence[i]
        # 7. Recolor the pixels of the current object
        for r, c in obj['pixels']:
            output_grid[r, c] = target_color
            
    return output_grid.tolist() # Return as list of lists

```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 0 8 8 8 8 8 8 8 0 0 0 0 0
0 8 8 8 0 8 8 8 8 8 0 8 0 0 0 0 0
0 0 0 0 0 8 0 8 8 8 0 8 0 0 0 0 0
0 0 0 0 0 8 8 8 0 8 8 8 0 0 0 0 0
0 0 0 0 0 8 8 8 8 8 8 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 0
0 0 0 8 8 8 8 0 0 8 0 0 8 0 0 8 0
0 0 0 8 8 8 8 0 0 8 8 8 8 8 8 8 0
0 0 0 8 0 8 8 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 0 0 0 0 8 8 8 8 0 0
0 0 0 8 8 8 8 0 0 0 0 8 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 8 0 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 0 3 3 3 3 3 3 3 0 0 0 0 0
0 1 1 1 0 3 3 3 3 3 0 3 0 0 0 0 0
0 0 0 0 0 3 0 3 3 3 0 3 0 0 0 0 0
0 0 0 0 0 3 3 3 0 3 3 3 0 0 0 0 0
0 0 0 0 0 3 3 3 3 3 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 0
0 0 0 1 1 1 1 0 0 2 0 0 2 0 0 2 0
0 0 0 1 1 1 1 0 0 2 2 2 2 2 2 2 0
0 0 0 1 0 1 1 0 0 0 0 0 0 0 0 0 0
0 0 0 1 1 1 1 0 0 0 0 2 2 2 2 0 0
0 0 0 1 1 1 1 0 0 0 0 2 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 2 0 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 3 3 3 3 3 3 3 0 0 0 0 0
0 2 2 2 0 3 3 3 3 3 0 3 0 0 0 0 0
0 0 0 0 0 3 0 3 3 3 0 3 0 0 0 0 0
0 0 0 0 0 3 3 3 0 3 3 3 0 0 0 0 0
0 0 0 0 0 3 3 3 3 3 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 0
0 0 0 1 1 1 1 0 0 1 0 0 1 0 0 1 0
0 0 0 1 1 1 1 0 0 1 1 1 1 1 1 1 0
0 0 0 1 0 1 1 0 0 0 0 0 0 0 0 0 0
0 0 0 1 1 1 1 0 0 0 0 2 2 2 2 0 0
0 0 0 1 1 1 1 0 0 0 0 2 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 2 0 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 28
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 17.3374613003096

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 8 8 8 0 0 0 8 8 8 8 8 0
0 0 8 0 0 8 0 8 0 0 0 8 0 8 8 8 0
0 0 8 0 0 8 8 8 0 0 0 8 8 8 0 8 0
0 0 8 8 8 8 8 8 0 0 0 8 0 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 0
0 0 0 0 0 8 8 8 8 0 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 8 0 0 8 8 8 8 0 0
0 0 0 0 0 8 8 8 8 0 0 8 0 0 8 0 0
0 0 0 0 0 8 8 0 8 0 0 8 8 8 8 0 0
0 0 0 0 0 8 8 8 8 0 0 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 0 0 0 8 8 8 8 8 8 8 0
0 8 8 8 0 8 0 0 0 8 0 8 8 8 0 8 0
0 8 0 8 8 8 0 0 0 8 8 8 0 8 0 8 0
0 8 8 8 8 8 0 0 0 8 0 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 2 0 0 0 3 3 3 3 3 0
0 0 2 0 0 2 0 2 0 0 0 3 0 3 3 3 0
0 0 2 0 0 2 2 2 0 0 0 3 3 3 0 3 0
0 0 2 2 2 2 2 2 0 0 0 3 0 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 0
0 0 0 0 0 2 2 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 2 0 0 1 1 1 1 0 0
0 0 0 0 0 2 2 2 2 0 0 1 0 0 1 0 0
0 0 0 0 0 2 2 0 2 0 0 1 1 1 1 0 0
0 0 0 0 0 2 2 2 2 0 0 1 1 1 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 0 0 0 7 7 7 7 7 7 7 0
0 2 2 2 0 2 0 0 0 7 0 7 7 7 0 7 0
0 2 0 2 2 2 0 0 0 7 7 7 0 7 0 7 0
0 2 2 2 2 2 0 0 0 7 0 7 7 7 7 7 0
0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 2 0 0 0 3 3 3 3 3 0
0 0 2 0 0 2 0 2 0 0 0 3 0 3 3 3 0
0 0 2 0 0 2 2 2 0 0 0 3 3 3 0 3 0
0 0 2 2 2 2 2 2 0 0 0 3 0 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 0
0 0 0 0 0 2 2 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 2 0 0 1 1 1 1 0 0
0 0 0 0 0 2 2 2 2 0 0 1 0 0 1 0 0
0 0 0 0 0 2 2 0 2 0 0 1 1 1 1 0 0
0 0 0 0 0 2 2 2 2 0 0 1 1 1 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 0 0 0 7 7 7 7 7 7 7 0
0 2 2 2 0 2 0 0 0 7 0 7 7 7 0 7 0
0 2 0 2 2 2 0 0 0 7 7 7 0 7 0 7 0
0 2 2 2 2 2 0 0 0 7 0 7 7 7 7 7 0
0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 0
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0

## Example 3:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0
0 8 0 0 8 0 8 0 0 0 0 0 0 0 0 0
0 8 0 0 8 8 8 0 8 8 8 8 8 8 0 0
0 8 8 8 8 0 8 0 8 0 0 8 0 8 0 0
0 8 8 8 8 8 8 0 8 8 8 8 8 8 0 0
0 0 0 0 0 0 0 0 8 8 0 0 8 8 0 0
0 0 8 8 8 8 8 0 8 8 8 8 8 8 0 0
0 0 8 0 8 8 8 0 0 0 0 0 0 0 0 0
0 0 8 0 8 0 8 0 0 0 0 0 0 0 0 0
0 0 8 8 8 0 8 0 0 0 0 0 0 0 0 0
0 0 8 8 8 8 8 0 0 0 0 0 0 0 0 0
0 0 8 0 8 8 8 0 0 0 8 8 8 8 8 8
0 0 8 8 8 8 8 0 0 0 8 0 8 0 8 8
0 0 8 8 0 0 8 0 0 0 8 8 8 8 8 8
0 0 8 8 8 8 8 0 0 0 8 0 8 0 0 8
0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0
0 3 0 0 3 0 3 0 0 0 0 0 0 0 0 0
0 3 0 0 3 3 3 0 3 3 3 3 3 3 0 0
0 3 3 3 3 0 3 0 3 0 0 3 0 3 0 0
0 3 3 3 3 3 3 0 3 3 3 3 3 3 0 0
0 0 0 0 0 0 0 0 3 3 0 0 3 3 0 0
0 0 7 7 7 7 7 0 3 3 3 3 3 3 0 0
0 0 7 0 7 7 7 0 0 0 0 0 0 0 0 0
0 0 7 0 7 0 7 0 0 0 0 0 0 0 0 0
0 0 7 7 7 0 7 0 0 0 0 0 0 0 0 0
0 0 7 7 7 7 7 0 0 0 0 0 0 0 0 0
0 0 7 0 7 7 7 0 0 0 7 7 7 7 7 7
0 0 7 7 7 7 7 0 0 0 7 0 7 0 7 7
0 0 7 7 0 0 7 0 0 0 7 7 7 7 7 7
0 0 7 7 7 7 7 0 0 0 7 0 7 0 0 7
0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0
0 3 0 0 3 0 3 0 0 0 0 0 0 0 0 0
0 3 0 0 3 3 3 0 3 3 3 3 3 3 0 0
0 3 3 3 3 0 3 0 3 0 0 3 0 3 0 0
0 3 3 3 3 3 3 0 3 3 3 3 3 3 0 0
0 0 0 0 0 0 0 0 3 3 0 0 3 3 0 0
0 0 7 7 7 7 7 0 3 3 3 3 3 3 0 0
0 0 7 0 7 7 7 0 0 0 0 0 0 0 0 0
0 0 7 0 7 0 7 0 0 0 0 0 0 0 0 0
0 0 7 7 7 0 7 0 0 0 0 0 0 0 0 0
0 0 7 7 7 7 7 0 0 0 0 0 0 0 0 0
0 0 7 0 7 7 7 0 0 0 7 7 7 7 7 7
0 0 7 7 7 7 7 0 0 0 7 0 7 0 7 7
0 0 7 7 0 0 7 0 0 0 7 7 7 7 7 7
0 0 7 7 7 7 7 0 0 0 7 0 7 0 0 7
0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0
