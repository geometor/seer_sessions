
Previous Code:
```python
"""
Add a vertical magenta (color 6) border on the left side of the grid. Then, starting from the left, replace orange (color 7) pixels with magenta (6) in a way that creates proximity to or fills in gaps around the red shapes, expanding until no more red shapes can be immediately filled.
"""

import numpy as np

def get_objects(grid):
    """Find contiguous regions of the same color."""
    objects = {}
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    def dfs(r, c, color, obj_id):
        if (r < 0 or r >= rows or c < 0 or c >= cols or
                visited[r, c] or grid[r, c] != color):
            return []

        visited[r, c] = True
        coords = [(r, c)]

        coords.extend(dfs(r + 1, c, color, obj_id))
        coords.extend(dfs(r - 1, c, color, obj_id))
        coords.extend(dfs(r, c + 1, color, obj_id))
        coords.extend(dfs(r, c - 1, color, obj_id))
        return coords

    obj_id = 0
    for r in range(rows):
        for c in range(cols):
            if not visited[r, c]:
                color = grid[r, c]
                coords = dfs(r, c, color, obj_id)
                if coords:
                    objects[obj_id] = {
                        'color': color,
                        'coords': coords
                    }
                    obj_id += 1
    return objects

def is_adjacent_to_color(grid, coord, target_color):
    """Checks if the given coordinate is adjacent to a cell of the target color."""
    rows, cols = grid.shape
    r, c = coord
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == target_color:
            return True
    return False

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    
    # Initialize output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Add Left Magenta Border
    for r in range(rows):
        output_grid[r, 0] = 6

    # Overlay/Fill with Magenta
    objects = get_objects(input_grid)  # Use input_grid to identify initial red regions.

    # Find initial red coordinates
    red_coords = []
    for obj_id, obj_data in objects.items():
      if obj_data['color'] == 2:
        red_coords.extend(obj_data['coords'])

    # Iteratively fill around Red
    
    visited = np.zeros_like(input_grid,dtype=bool)   
    queue = [(r,0) for r in range(rows)] # Start expanding from left border.
    for r,c in queue:
        visited[r,c] = True
        
    while queue:
      new_queue = []
      for r,c in queue:
        if output_grid[r,c] == 7:
          if any(is_adjacent_to_color(output_grid,(r+dr,c+dc),2) 
                for dr,dc in [(0,1),(0,-1),(1,0),(-1,0)]):
              output_grid[r,c] = 6
              
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and not visited[nr,nc]:
              visited[nr,nc]=True
              new_queue.append((nr,nc))
      queue = new_queue
    

    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
7 7 7 7 6 7 7 7 7 7 7 7 6 7
7 7 7 7 6 7 7 7 7 7 7 7 6 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 2 2 2 7 7 7 7 7 2 2 2
7 7 7 7 7 7 7 7 7 7 7 7 7 7
2 2 2 2 2 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 2 2 2 2 2 2 2
7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 2 2 2 2 2 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 2 2 2 2 2 2 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7
```
Expected Output:
```
7 7 7 7 6 7 7 7 7 7 7 7 6 7
7 7 7 7 6 7 7 7 7 7 7 7 6 7
7 7 6 6 6 6 6 7 7 7 6 6 6 6
7 7 6 2 2 2 6 7 7 7 6 2 2 2
6 6 6 6 6 6 6 7 7 7 6 7 7 7
2 2 2 2 2 6 6 7 7 7 6 7 7 7
7 7 7 7 7 6 6 7 7 7 6 7 7 7
7 7 7 7 7 6 6 6 6 6 6 6 6 6
7 7 7 7 7 6 6 2 2 2 2 2 2 2
7 6 6 6 6 6 6 6 7 7 7 7 7 7
7 6 2 2 2 2 2 6 7 7 7 7 7 7
7 6 7 7 6 6 6 6 6 6 6 6 7 7
7 6 7 7 6 2 2 2 2 2 2 6 7 7
7 6 7 7 6 7 7 7 7 7 7 6 7 7
```
Transformed Output:
```
6 7 7 7 6 7 7 7 7 7 7 7 6 7
6 7 7 6 6 6 7 7 7 7 7 6 6 6
6 7 6 6 6 6 6 7 7 7 6 6 6 6
6 6 6 2 2 2 6 6 7 6 6 2 2 2
6 6 6 6 6 6 6 7 7 7 6 6 6 6
6 2 2 2 2 6 6 7 7 7 7 6 6 6
6 6 6 6 6 6 7 6 6 6 6 6 6 6
6 6 6 6 6 7 6 6 6 6 6 6 6 6
6 7 6 6 6 6 6 2 2 2 2 2 2 2
6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 2 2 2 2 2 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 7 7
6 7 6 6 6 2 2 2 2 2 2 6 6 7
6 7 7 7 6 6 6 6 6 6 6 6 7 7
```
Match: False
Pixels Off: 71
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 72.44897959183673

## Example 2:
Input:
```
7 7 7 7 6 7 7 7 7 7 7 6 7
7 7 7 7 6 7 7 7 7 7 7 6 7
7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 2 2 2 2
7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7
7 2 2 2 2 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 2 2 2 2 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7
```
Expected Output:
```
7 7 7 7 6 7 7 7 7 7 7 6 7
7 7 7 7 6 7 7 7 7 7 7 6 7
7 7 7 7 6 7 7 7 7 7 7 6 7
7 7 7 7 6 7 7 7 6 6 6 6 7
7 7 7 7 6 7 7 7 6 2 2 2 2
7 7 7 7 6 7 7 7 6 7 7 7 7
7 7 7 7 6 7 7 7 6 7 7 7 7
7 7 7 7 6 7 7 7 6 7 7 7 7
6 6 6 6 6 6 7 7 6 7 7 7 7
6 2 2 2 2 6 7 7 6 7 7 7 7
6 7 7 7 7 6 7 7 6 7 7 7 7
6 7 7 7 7 6 7 7 6 7 7 7 7
6 7 7 6 6 6 6 6 6 7 7 7 7
6 7 7 6 2 2 2 2 6 7 7 7 7
6 7 7 6 7 7 7 7 6 7 7 7 7
6 7 7 6 7 7 7 7 6 7 7 7 7
```
Transformed Output:
```
6 7 7 7 6 7 7 7 7 7 7 6 7
6 7 7 7 6 7 7 7 7 7 7 6 7
6 7 7 7 7 7 7 7 7 6 6 6 6
6 7 7 7 7 7 7 7 6 6 6 6 6
6 7 7 7 7 7 7 6 6 2 2 2 2
6 7 7 7 7 7 7 7 6 6 6 6 6
6 7 7 7 7 7 7 7 7 6 6 6 6
6 6 6 6 6 7 7 7 7 7 7 7 7
6 6 6 6 6 6 7 7 7 7 7 7 7
6 2 2 2 2 6 6 7 7 7 7 7 7
6 6 6 6 6 6 7 7 7 7 7 7 7
6 6 6 6 6 6 6 6 7 7 7 7 7
6 7 7 6 6 6 6 6 6 7 7 7 7
6 7 6 6 2 2 2 2 6 6 7 7 7
6 7 7 6 6 6 6 6 6 7 7 7 7
6 7 7 7 6 6 6 6 7 7 7 7 7
```
Match: False
Pixels Off: 58
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 55.769230769230774

## Example 3:
Input:
```
7 7 6 7 7 7 7 2 2
7 7 6 7 7 7 7 2 7
7 2 2 2 7 7 7 7 7
7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7
7 7 7 2 2 2 2 7 7
7 7 7 7 7 7 7 7 7
2 2 2 2 2 2 7 7 7
```
Expected Output:
```
7 7 6 7 7 7 7 2 2
6 6 6 6 6 7 7 2 7
6 2 2 2 6 7 7 7 7
6 7 7 7 6 7 7 7 7
6 7 6 6 6 6 6 6 7
6 7 6 2 2 2 2 6 7
6 6 6 6 6 6 6 6 7
2 2 2 2 2 2 6 6 7
```
Transformed Output:
```
6 6 6 6 7 6 6 2 2
6 6 6 6 6 6 6 2 6
6 2 2 2 6 6 6 6 6
6 6 6 6 6 6 6 6 7
6 6 6 6 6 6 6 6 7
6 6 6 2 2 2 2 6 6
6 6 6 6 6 6 6 6 7
6 2 2 2 2 2 6 6 7
```
Match: False
Pixels Off: 22
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 61.111111111111114

## Example 4:
Input:
```
7 7 7 6 7
2 2 2 6 2
7 7 7 7 7
7 7 2 7 2
7 7 7 7 7
7 7 2 2 2
7 7 7 7 7
7 7 7 7 7
7 7 7 7 7
7 7 7 7 7
2 2 2 7 2
7 7 7 7 7
7 7 2 2 2
7 7 7 7 7
```
Expected Output:
```
7 7 7 6 7
2 2 2 6 2
7 7 7 6 7
7 7 2 6 2
7 6 6 6 6
7 6 2 2 2
7 6 7 7 7
7 6 7 7 7
7 6 7 7 7
6 6 6 6 7
2 2 2 6 2
7 6 6 6 6
7 6 2 2 2
7 6 7 7 7
```
Transformed Output:
```
6 6 6 6 7
6 2 2 6 2
6 6 6 6 7
6 6 2 6 2
6 6 6 6 6
6 6 2 2 2
6 6 6 6 6
6 7 6 6 6
6 6 6 7 6
6 6 6 6 7
6 2 2 6 2
6 6 6 6 6
6 6 2 2 2
6 6 6 6 6
```
Match: False
Pixels Off: 30
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 85.71428571428572

## Example 5:
Input:
```
6 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
6 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 2 2 2 2 7 7 7 7 7 7 2 2 2 2
7 7 2 2 2 2 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 2 2 2 2 2 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
```
Expected Output:
```
6 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 7
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 6 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 6 6 6 6 6
7 7 7 7 7 7 2 2 2 2 7 7 7 7 7 6 2 2 2 2
7 7 2 2 2 2 7 7 7 7 7 7 6 6 6 6 6 6 6 7
7 7 7 7 7 7 7 7 7 7 7 7 6 2 2 2 2 2 6 7
7 7 7 7 7 7 7 7 7 7 7 7 6 7 7 7 7 7 6 7
```
Transformed Output:
```
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 7 7
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 7
6 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 2 2 2 2 6 6 6 6 6 6 2 2 2 2
6 6 2 2 2 2 6 6 6 6 6 7 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 7 6 6 2 2 2 2 2 6 6
6 7 6 6 6 6 7 7 7 7 7 7 6 6 6 6 6 6 6 7
```
Match: False
Pixels Off: 75
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 93.75

## Example 6:
Input:
```
7 7 7 7 7 7 6 7 7 7 7 7 7 7 7 7
2 2 2 2 2 2 6 7 7 2 2 2 2 2 2 2
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 2 2 2 2 2 2 2 2 2 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
2 2 2 2 2 2 2 2 2 2 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 2 2 2 2 2 2 2 2 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
2 2 7 7 2 2 2 2 2 2 2 2 2 2 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
```
Expected Output:
```
7 7 7 7 7 7 6 7 7 7 7 7 7 7 7 7
2 2 2 2 2 2 6 7 7 2 2 2 2 2 2 2
7 7 7 7 7 7 6 7 7 7 7 7 7 7 7 7
7 7 7 6 6 6 6 6 6 6 6 6 6 6 7 7
7 7 7 6 2 2 2 2 2 2 2 2 2 6 7 7
7 7 7 6 7 7 7 7 7 7 7 7 7 6 7 7
6 6 6 6 6 6 6 6 6 6 6 7 7 6 7 7
2 2 2 2 2 2 2 2 2 2 6 7 7 6 7 7
7 7 7 7 7 7 7 7 7 7 6 7 7 6 7 7
7 7 7 7 7 7 6 6 6 6 6 6 6 6 6 6
7 7 7 7 7 7 6 2 2 2 2 2 2 2 2 6
7 7 7 7 7 7 6 7 7 7 7 7 7 7 7 6
7 7 7 6 6 6 6 6 6 6 6 6 6 6 6 6
2 2 7 6 2 2 2 2 2 2 2 2 2 2 6 6
7 7 7 6 7 7 7 7 7 7 7 7 7 7 6 6
```
Transformed Output:
```
6 6 6 6 6 6 6 7 6 6 6 6 6 6 6 6
6 2 2 2 2 2 6 6 6 2 2 2 2 2 2 2
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 7 6 6 2 2 2 2 2 2 2 2 2 6 6 7
6 6 6 6 6 6 6 6 6 6 6 6 6 6 7 7
6 6 6 6 6 6 6 6 6 6 6 6 6 7 7 7
6 2 2 2 2 2 2 2 2 2 6 6 7 7 7 7
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 7
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 7 7 7 7 6 6 2 2 2 2 2 2 2 2 6
6 6 7 7 6 6 6 6 6 6 6 6 6 6 6 6
6 7 6 6 6 6 6 6 6 6 6 6 6 6 6 7
6 2 6 6 2 2 2 2 2 2 2 2 2 2 6 6
6 7 6 6 6 6 6 6 6 6 6 6 6 6 6 7
```
Match: False
Pixels Off: 109
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 90.83333333333334
Here's an analysis of the provided examples and results, along with a strategy for improving the transformation rule:

**General Assessment:**

The initial natural language program and the resulting code have several issues, leading to significant discrepancies between the transformed outputs and the expected outputs. The core problems are:

1.  **Incorrect Magenta Border Placement:** The initial program stated a *vertical magenta border on the left side*. The code implements this, but most of the examples show this isn't universally true. Some expected outputs have magenta replacing existing orange on the *left side*, but not strictly as a new border. The first operation should thus be to *replace* orange pixels on the left border by magenta.
2.  **Overly Aggressive Magenta Fill:** The code's magenta fill is too aggressive and doesn't correctly interpret the "proximity to or fills in gaps around the red shapes" condition. It appears to expand magenta outwards from the starting line without careful consideration for adjacent red shapes. The propagation should be more controlled, stopping based on red object proximity.
3.  **Incorrect Queue Logic**: The queue logic doesn't seem to be working as intended, as the magenta filling is going past the red shapes, or not covering some areas adjacent to red.
4.  **Incorrect starting point for expansion:** The fill always starts at the left-most column, but should consider the context of the shapes.

**Strategy for Resolving Errors:**

1.  **Prioritize Replacement over Border Addition:** Instead of always adding a magenta border, the code should first replace the orange pixels on the left edge (column 0) with magenta.

2.  **Refine Magenta Propagation:** Implement a more precise rule for magenta propagation. The magenta color should only replace orange pixels, and this should happen iteratively, expanding one layer at a time, based on adjacency to *both* magenta and red pixels. The expansion should stop when no more orange pixels adjacent to the expanding magenta "front" *and* a red pixel can be found.

3.  **Revisit Queue Logic/Breadth-First Search (BFS):** The queue logic (likely intended for a BFS) needs careful review. It should correctly manage the expansion front, ensuring that only eligible orange pixels (adjacent to magenta *and* red) are replaced. The BFS will need to check in 4 directions.

4. **Object-Centric Approach.** The objects approach should be kept, and objects can be used to derive metrics and other measures.

**Metrics Gathering (using code execution):**

I'll use a simplified version of the code to verify sizes.



*code_execution:*
```python
import numpy as np

def get_grid_shape(grid_str):
    grid = np.array([list(map(int, row.split())) for row in grid_str.strip().split('\n')])
    return grid.shape

example_inputs = [
    """
7 7 7 7 6 7 7 7 7 7 7 7 6 7
7 7 7 7 6 7 7 7 7 7 7 7 6 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 2 2 2 7 7 7 7 7 2 2 2
7 7 7 7 7 7 7 7 7 7 7 7 7 7
2 2 2 2 2 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 2 2 2 2 2 2 2
7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 2 2 2 2 2 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 2 2 2 2 2 2 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7
""",
    """
7 7 7 7 6 7 7 7 7 7 7 6 7
7 7 7 7 6 7 7 7 7 7 7 6 7
7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 2 2 2 2
7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7
7 2 2 2 2 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 2 2 2 2 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7
""",
    """
7 7 6 7 7 7 7 2 2
7 7 6 7 7 7 7 2 7
7 2 2 2 7 7 7 7 7
7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7
7 7 7 2 2 2 2 7 7
7 7 7 7 7 7 7 7 7
2 2 2 2 2 2 7 7 7
""",
    """
7 7 7 6 7
2 2 2 6 2
7 7 7 7 7
7 7 2 7 2
7 7 7 7 7
7 7 2 2 2
7 7 7 7 7
7 7 7 7 7
7 7 7 7 7
7 7 7 7 7
2 2 2 7 2
7 7 7 7 7
7 7 2 2 2
7 7 7 7 7
""",
    """
6 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
6 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 2 2 2 2 7 7 7 7 7 7 2 2 2 2
7 7 2 2 2 2 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 2 2 2 2 2 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
""",
"""
7 7 7 7 7 7 6 7 7 7 7 7 7 7 7 7
2 2 2 2 2 2 6 7 7 2 2 2 2 2 2 2
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 2 2 2 2 2 2 2 2 2 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
2 2 2 2 2 2 2 2 2 2 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 2 2 2 2 2 2 2 2 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
2 2 7 7 2 2 2 2 2 2 2 2 2 2 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
"""
]

for i, input_grid_str in enumerate(example_inputs):
    shape = get_grid_shape(input_grid_str)
    print(f"Example {i+1} Shape: {shape}")


```

*code_execution_result:*
outcome: 1
```
Example 1 Shape: (14, 14)
Example 2 Shape: (16, 13)
Example 3 Shape: (8, 9)
Example 4 Shape: (14, 5)
Example 5 Shape: (8, 20)
Example 6 Shape: (15, 16)

```
**YAML Fact Documentation:**


```yaml
task:
  id: "7b60155d"
  description: >
    Replace orange pixels on the left edge with magenta.
    Propagate magenta color from the left, replacing orange pixels.
    Propagation requires adjacency to both existing magenta and red pixels.
    Stop when no more orange pixels meet the adjacency condition.
objects:
  - id: red_regions
    color: 2
    description: "Contiguous regions of red pixels. These act as propagation guides."
  - id: orange_regions
    color: 7
    description: "Regions of orange pixels that are potential candidates for replacement."
  - id: magenta_regions
    color: 6
    description: "Regions of magenta, initially the leftmost column (where orange) and expanding based on adjacency rules."
  - id: other_colors
    description: Colors different from 2, 7, or 6. No actions required.
actions:
  - id: replace_leftmost_orange
    description: "Replace any orange pixel in the first column (left edge) with magenta."
  - id: propagate_magenta
    description: "Expand magenta regions iteratively."
    conditions:
      - "Target pixel must be orange."
      - "Target pixel must be adjacent to an existing magenta pixel."
      - "Target pixel must be adjacent to a red pixel."
    stop_condition: "No more orange pixels satisfy the adjacency conditions."
```


**Natural Language Program:**

1.  **Initialize:** Replace any orange (7) pixels in the first column (index 0) of the input grid with magenta (6) pixels.

2.  **Iterative Propagation:** Perform the following steps iteratively until no changes occur:
    *   For each orange (7) pixel in the grid:
        *   Check if the pixel is adjacent (horizontally or vertically) to *both* a magenta (6) pixel *and* a red (2) pixel.
        *   If both adjacency conditions are met, change the orange pixel to magenta.

3.  **Termination:** The process stops when, during an iteration, no orange pixels are changed to magenta. The resulting grid is the final output.

