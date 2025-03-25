
Previous Code:
```python
"""
The program identifies connected components of non-zero colored pixels in the input grid, extracts them, and arranges them in a 2x2 block in the output grid in column major order. The relative 2D shape of each component is preserved. Background (zero-colored) pixels are discarded, and a new 2x2 block is created.
"""

import numpy as np

def get_connected_components(grid):
    """
    Finds connected components of non-zero pixels in a grid.
    """
    visited = np.zeros_like(grid, dtype=bool)
    components = []

    def dfs(row, col, component):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] == 0):
            return
        visited[row, col] = True
        component.append((row, col))
        dfs(row + 1, col, component)
        dfs(row - 1, col, component)
        dfs(row, col + 1, component)
        dfs(row, col - 1, component)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] != 0 and not visited[r, c]:
                component = []
                dfs(r, c, component)
                components.append((grid[r,c],component)) # store color with component
    return components

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    components = get_connected_components(input_grid)
    
    # Sort components based on their first appearance in column-major order.
    sorted_components = sorted(components, key=lambda x: (x[1][0][1], x[1][0][0]))
    
    output_grid = np.zeros((4, 4), dtype=int)
    
    out_row = 0
    out_col = 0
    
    for color, component in sorted_components:
      
        first_row = component[0][0]
        first_col = component[0][1]
      
        
        for r,c in component:
          output_grid[out_row + (r - first_row)  , out_col + (c- first_col) ] = input_grid[r,c]
          
        out_col += 2
        if out_col >= 4:
            out_col = 0
            out_row += 2

    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 8 0 0 0
0 0 0 0 0 0 0 0 0 8 0 0 0
0 0 1 1 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0 0 0 0
0 0 0 0 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
1 1 8 8
1 0 0 8
4 0 0 2
4 4 2 2
```
Transformed Output:
```
1 1 4 0
1 0 4 4
8 8 2 0
0 2 2 0
```
Match: False
Pixels Off: 11
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 137.5

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 8 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1 0 0 0 0
0 0 0 0 0 0 0 1 1 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0 0 0
0 0 0 3 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
8 8 2 2
8 0 0 2
3 0 0 1
3 3 1 1
```
Transformed Output:
```
2 2 3 0
0 2 3 3
8 8 1 0
8 1 1 0
```
Match: False
Pixels Off: 15
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 93.75
