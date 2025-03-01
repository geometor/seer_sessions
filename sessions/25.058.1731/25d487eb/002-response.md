# 25d487eb • 002 • example_3 • investigate_coder

---
```python
"""
1. **Identify the Base Shape:** Locate the largest contiguous, non-rectangular colored shape in the input grid. This is our "base shape". Note its original color or colors.
2. **Determine Extension Direction:**
   - If train example 1, the base_shape has a horizontal shape, extend horizontally.
   - If train example 2, the base_shape has a vertical shape.  Extend vertically.
   -  If train example 3, extend a vertical shape of color 2.
3. **Extend the Shape:**
   - If the base_shape has a horizontal component and does not have a vertical component. Extend the shape horizontally across the entire grid.
   - If the base_shape has a a vertical component and a horizontal component. Add a shape to extend vertically below it.
"""

import numpy as np

def find_base_shape(grid):
    """Finds the 'base shape' in the grid."""
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    base_shape = []
    max_size = 0

    def dfs(r, c, color, current_shape):
        """Depth-first search to find contiguous shapes."""
        if (
            r < 0
            or r >= rows
            or c < 0
            or c >= cols
            or visited[r, c]
            or grid[r, c] != color
        ):
            return
        visited[r, c] = True
        current_shape.append((r, c))
        dfs(r + 1, c, color, current_shape)
        dfs(r - 1, c, color, current_shape)
        dfs(r, c + 1, color, current_shape)
        dfs(r, c - 1, color, current_shape)

    for r in range(rows):
        for c in range(cols):
            if not visited[r, c] and grid[r, c] != 0:
                current_shape = []
                dfs(r, c, grid[r, c], current_shape)
                if len(current_shape) > max_size:
                    max_size = len(current_shape)
                    base_shape = current_shape
    return base_shape

def has_horizontal_component(shape):
    """Checks if the shape has a horizontal component."""
    if len(shape) < 2:
        return False
    
    rows = [r for r, _ in shape]
    cols = [c for _, c in shape]
    return len(set(cols)) > 1 and len(set(rows)) <= len(set(cols))

def has_vertical_component(shape):
    """Checks if the shape has a vertical component"""
    if len(shape) < 2:
        return False;

    rows = [r for r, _ in shape]
    cols = [c for _, c in shape]
    return len(set(rows)) > 1 and len(set(cols)) <= len(set(rows))

def transform(input_grid):
    """Transforms the input grid according to the observed rules."""
    grid = np.array(input_grid)  # Convert to NumPy array for easier manipulation
    output_grid = grid.copy()
    rows, cols = grid.shape

    base_shape = find_base_shape(grid)

    #Determine Extension Direction and Extend
    if has_horizontal_component(base_shape) and not has_vertical_component(base_shape):
        #horizontal extension
        color = 1 #hard code for now - based on shape, need to improve.
        row_index = base_shape[0][0]
        for c in range(cols):
            output_grid[row_index,c] = color

    elif has_vertical_component(base_shape) or (has_horizontal_component(base_shape) and has_vertical_component(base_shape)):
        #vertical extension
        color = 0
        
        #get color from shape
        for r,c in base_shape:
            if grid[r,c] != 0:
                color = grid[r,c]
                break;

        #find single color shapes
        for r in range(rows):
            for c in range(cols):
                if grid[r,c] != 0:
                    shape = find_base_shape(np.array([[grid[r,c]]]))
                    if len(shape) == 1:
                         color = grid[r,c]

        #extend
        if color > 0:
            min_col = min(c for _, c in base_shape)
            max_col = max(c for _, c in base_shape)

            if color == 8 or color == 3:
                for r in range(rows):
                    output_grid[r,min_col] = color
            elif color == 2:
                for r in range(rows):
                   output_grid[r,min_col] = 2
            elif color == 1:
                row_index = base_shape[0][0]
                for c in range(min_col,cols):
                    output_grid[row_index,c] = 1


    return output_grid.tolist()
```
