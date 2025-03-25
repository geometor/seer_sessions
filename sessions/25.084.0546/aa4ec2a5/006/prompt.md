
Previous Code:
```python
"""
1.  **Identify Blue Regions:** Find all contiguous regions (objects) of blue (1) pixels within the input grid.
2.  **Create Red Outline:** For each identified blue region:
    *   Examine the pixels immediately surrounding the blue region.
    *   If a surrounding pixel is yellow (4) or is part of the input image boundary, change it to red (2).
3.  **Create Light Blue Inner Border:**
    *   For each identified blue region, find its inner border pixels (blue pixels adjacent to non-blue pixels). Change the inner border to light blue(8).
4.  **Fill Central Area with Gray:** Replace all remaining blue (1) pixels within each original blue region with gray (5).
5. **Preserve other colors** Pixels not part of the above transformations should remain unchanged
"""

import numpy as np

def find_objects(grid, color):
    """Finds contiguous regions of the specified color."""
    mask = (grid == color)
    rows, cols = grid.shape
    labeled_grid = np.zeros_like(grid)
    label_count = 0

    def dfs(r, c, label):
        """Depth-first search to label connected components."""
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r, c] != color or labeled_grid[r, c] != 0:
            return
        labeled_grid[r, c] = label
        dfs(r + 1, c, label)
        dfs(r - 1, c, label)
        dfs(r, c + 1, label)
        dfs(r, c - 1, label)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and labeled_grid[r, c] == 0:
                label_count += 1
                dfs(r, c, label_count)

    return labeled_grid, label_count

def get_neighbors(grid, r, c):
    """Gets the valid neighbors of a cell (up, down, left, right)."""
    rows, cols = grid.shape
    neighbors = []
    if r > 0:
        neighbors.append((r - 1, c))
    if r < rows - 1:
        neighbors.append((r + 1, c))
    if c > 0:
        neighbors.append((r, c - 1))
    if c < cols - 1:
        neighbors.append((r, c + 1))
    return neighbors

def get_border(grid, labeled_array, object_label):
    """Gets the outer border pixels of a labeled object."""
    border_pixels = []
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if labeled_array[r, c] == object_label:
                for nr, nc in get_neighbors(grid, r, c):
                    if labeled_array[nr, nc] != object_label:
                        border_pixels.append((r, c))
                        break  # Stop checking neighbors once a border is found
    return border_pixels

def get_outer_border(input_grid, labeled_array, object_label):
    """
    Find the pixels that immediately surround the current blue object, *and* are not part of the object.
    """
    outer_border = []
    rows, cols = input_grid.shape
    object_pixels = []

    # first, find all pixels of this object
    for r in range(rows):
        for c in range(cols):
            if labeled_array[r,c] == object_label:
                object_pixels.append((r,c))

    # now find surrounding pixels, only if not part of the object
    for r, c in object_pixels:
        for nr, nc in get_neighbors(input_grid, r, c):
            if labeled_array[nr, nc] != object_label:
                outer_border.append((nr,nc))
    return outer_border
    

def transform(input_grid):
    """Transforms the input grid according to the observed rules."""
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # 1. Identify Blue Regions
    labeled_array, num_blue_objects = find_objects(input_grid, 1)

    for i in range(1, num_blue_objects + 1):  # Iterate through each blue object
        # 2. Create Red Outline
        
        outer_border = get_outer_border(input_grid, labeled_array, i)
        for r, c in outer_border:
            if input_grid[r,c] == 4 or r == 0 or r == rows-1 or c == 0 or c == cols-1:
                output_grid[r, c] = 2

        # 3. Create Light Blue Inner Border
        
        blue_border_pixels = get_border(input_grid, labeled_array, i) # get border of the original shape
        for r, c in blue_border_pixels:
           output_grid[r,c] = 8

        # 4. Fill Central Area with Gray
        for r in range(rows):
            for c in range(cols):
                if labeled_array[r, c] == i and output_grid[r,c] == 1: # still blue in the output
                    output_grid[r, c] = 5

    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 1 1 1 1 1 1 1 4 4
4 4 4 1 1 1 1 4 4 4 4 4 4 4 4 4 1 4 4 4 1 1 1 4 4
4 4 4 1 1 1 1 1 1 1 4 4 4 4 4 4 1 4 4 4 1 1 1 4 4
4 4 4 1 1 1 1 4 4 1 4 4 4 4 4 4 1 4 4 4 1 1 1 4 4
4 4 4 1 1 1 1 4 4 1 4 4 4 4 4 4 1 1 1 1 1 1 1 4 4
4 4 4 4 4 4 1 1 1 1 4 4 4 4 4 4 1 1 1 1 1 1 1 4 4
4 4 4 4 4 4 1 1 1 1 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 1 1 1 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 1 1 1 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 1 1 1 1 1 1 1 1 1 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 1 1 1 1 1 1 1 1 1 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 1 1 1 1 1 1 1 1 1 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 1 1 1 1 1 1 1 1 1 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 1 1 1 1 1 1 1 1 1 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
```
Expected Output:
```
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2 2 2 2 2 2 4
4 4 2 2 2 2 2 2 4 4 4 4 4 4 4 2 8 8 8 8 8 8 8 2 4
4 4 2 8 8 8 8 2 2 2 2 4 4 4 4 2 8 6 6 6 8 8 8 2 4
4 4 2 8 8 8 8 8 8 8 2 4 4 4 4 2 8 6 6 6 8 8 8 2 4
4 4 2 8 8 8 8 6 6 8 2 4 4 4 4 2 8 6 6 6 8 8 8 2 4
4 4 2 8 8 8 8 6 6 8 2 4 4 4 4 2 8 8 8 8 8 8 8 2 4
4 4 2 2 2 2 8 8 8 8 2 4 4 4 4 2 8 8 8 8 8 8 8 2 4
4 4 4 4 4 2 8 8 8 8 2 4 4 4 4 2 2 2 2 2 2 2 2 2 4
4 4 4 4 4 2 2 2 2 2 2 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 2 2 2 2 2 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 2 1 1 1 2 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 2 1 1 1 2 2 2 2 2 2 2 4 4 4 4 4
4 4 4 4 4 4 4 4 4 2 1 1 1 1 1 1 1 1 1 2 4 4 4 4 4
4 4 4 4 4 4 4 4 4 2 1 1 1 1 1 1 1 1 1 2 4 4 4 4 4
4 4 4 4 4 4 4 4 4 2 1 1 1 1 1 1 1 1 1 2 4 4 4 4 4
4 4 4 4 4 4 4 4 4 2 1 1 1 1 1 1 1 1 1 2 4 4 4 4 4
4 4 4 4 4 4 4 4 4 2 1 1 1 1 1 1 1 1 1 2 4 4 4 4 4
4 4 4 4 4 4 4 4 4 2 2 2 2 2 2 2 2 2 2 2 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
```
Transformed Output:
```
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2 2 2 2 4 4
4 4 4 2 2 2 2 4 4 4 4 4 4 4 4 2 8 8 8 8 8 8 8 2 4
4 4 2 8 8 8 8 2 2 2 4 4 4 4 4 2 8 2 2 2 8 5 8 2 4
4 4 2 8 5 5 5 8 8 8 2 4 4 4 4 2 8 2 4 2 8 5 8 2 4
4 4 2 8 5 5 8 2 2 8 2 4 4 4 4 2 8 2 2 2 8 5 8 2 4
4 4 2 8 8 8 8 2 2 8 2 4 4 4 4 2 8 8 8 8 5 5 8 2 4
4 4 4 2 2 2 8 8 8 8 2 4 4 4 4 2 8 8 8 8 8 8 8 2 4
4 4 4 4 4 2 8 8 8 8 2 4 4 4 4 4 2 2 2 2 2 2 2 4 4
4 4 4 4 4 4 2 2 2 2 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 2 2 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 2 8 8 8 2 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 2 8 5 8 2 2 2 2 2 2 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 2 8 5 5 8 8 8 8 8 8 2 4 4 4 4 4
4 4 4 4 4 4 4 4 4 2 8 5 5 5 5 5 5 5 8 2 4 4 4 4 4
4 4 4 4 4 4 4 4 4 2 8 5 5 5 5 5 5 5 8 2 4 4 4 4 4
4 4 4 4 4 4 4 4 4 2 8 5 5 5 5 5 5 5 8 2 4 4 4 4 4
4 4 4 4 4 4 4 4 4 2 8 8 8 8 8 8 8 8 8 2 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 2 2 2 2 2 2 2 2 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
```
Match: False
Pixels Off: 89
Size Correct: True
Color Palette Correct: False
Color Count Correct: False
Score: 61.913043478260875

## Example 2:
Input:
```
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 1 4 4 4 1 1 1 1 1 1 1 4 4
4 1 1 1 1 1 1 1 4 4 1 4 4 4 1 4 4 4 4 1 1 4 4
4 1 1 1 1 1 1 1 4 4 1 1 1 1 1 4 4 4 4 1 1 4 4
4 1 1 1 1 1 1 1 4 4 1 1 1 1 1 4 4 4 4 1 1 4 4
4 1 1 1 1 1 1 1 4 4 1 1 1 1 1 4 4 4 4 1 1 4 4
4 1 1 1 1 4 4 4 4 4 1 1 1 1 1 1 1 1 1 1 1 4 4
4 1 1 1 1 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 1 1 1 1 1 1 4 4 4 1 1 1 1 1 4 4 4 4 4
4 4 4 4 1 1 1 1 1 1 1 1 1 1 1 1 1 1 4 4 4 4 4
4 4 4 4 1 1 1 1 1 1 1 1 1 1 1 1 1 1 4 4 4 4 4
4 4 4 4 1 1 1 1 1 1 1 1 1 1 1 1 1 1 4 4 4 4 4
4 4 4 4 1 1 1 1 1 1 1 1 1 1 1 1 1 1 4 4 4 4 4
4 4 4 4 1 1 1 1 1 1 1 1 1 1 1 1 1 1 4 4 4 4 4
4 4 4 4 1 1 1 1 1 1 1 1 1 1 1 1 1 1 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 1 1 1 1 1 1 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 1 1 1 1 1 1 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 1 1 1 1 1 1 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 1 1 1 1 1 1 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 1 1 1 1 1 1 4 4 4 4 4
4 4 4 4 1 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 1 1 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
```
Expected Output:
```
4 4 4 4 4 4 4 4 4 2 2 2 4 2 2 2 2 2 2 2 2 2 4
2 2 2 2 2 2 2 2 2 2 8 2 4 2 8 8 8 8 8 8 8 2 4
2 1 1 1 1 1 1 1 2 2 8 2 2 2 8 6 6 6 6 8 8 2 4
2 1 1 1 1 1 1 1 2 2 8 8 8 8 8 6 6 6 6 8 8 2 4
2 1 1 1 1 1 1 1 2 2 8 8 8 8 8 6 6 6 6 8 8 2 4
2 1 1 1 1 1 1 1 2 2 8 8 8 8 8 6 6 6 6 8 8 2 4
2 1 1 1 1 2 2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 2 4
2 1 1 1 1 2 4 4 4 2 2 2 2 2 2 2 2 2 2 2 2 2 4
2 2 2 2 2 2 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 2 2 2 2 2 2 2 2 4 2 2 2 2 2 2 2 4 4 4 4
4 4 4 2 1 1 1 1 1 1 2 2 2 1 1 1 1 1 2 4 4 4 4
4 4 4 2 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 4 4 4 4
4 4 4 2 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 4 4 4 4
4 4 4 2 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 4 4 4 4
4 4 4 2 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 4 4 4 4
4 4 4 2 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 4 4 4 4
4 4 4 2 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 4 4 4 4
4 4 4 2 2 2 2 2 2 2 2 2 1 1 1 1 1 1 2 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 2 1 1 1 1 1 1 2 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 2 1 1 1 1 1 1 2 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 2 1 1 1 1 1 1 2 4 4 4 4
4 4 4 2 2 2 4 4 4 4 4 2 1 1 1 1 1 1 2 4 4 4 4
4 4 2 2 1 2 4 4 4 4 4 2 2 2 2 2 2 2 2 4 4 4 4
4 4 2 1 1 2 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 2 2 2 2 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
```
Transformed Output:
```
4 4 4 4 4 4 4 4 4 4 2 4 4 4 2 2 2 2 2 2 2 4 4
4 2 2 2 2 2 2 2 4 2 8 2 4 2 8 8 8 8 8 8 8 2 4
2 8 8 8 8 8 8 8 2 2 8 2 2 2 8 2 2 2 2 8 8 2 4
2 8 5 5 5 5 5 8 2 2 8 8 8 8 8 2 4 4 2 8 8 2 4
2 8 5 5 5 5 5 8 2 2 8 5 5 5 8 2 4 4 2 8 8 2 4
2 8 5 5 5 8 8 8 2 2 8 5 5 5 8 2 2 2 2 8 8 2 4
2 8 5 5 8 2 2 2 4 2 8 8 8 8 8 8 8 8 8 8 8 2 4
2 8 8 8 8 2 4 4 4 4 2 2 2 2 2 2 2 2 2 2 2 4 4
4 2 2 2 2 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 2 2 2 2 2 2 4 4 4 2 2 2 2 2 4 4 4 4 4
4 4 4 2 8 8 8 8 8 8 2 2 2 8 8 8 8 8 2 4 4 4 4
4 4 4 2 8 5 5 5 5 5 8 8 8 5 5 5 5 8 2 4 4 4 4
4 4 4 2 8 5 5 5 5 5 5 5 5 5 5 5 5 8 2 4 4 4 4
4 4 4 2 8 5 5 5 5 5 5 5 5 5 5 5 5 8 2 4 4 4 4
4 4 4 2 8 5 5 5 5 5 5 5 5 5 5 5 5 8 2 4 4 4 4
4 4 4 2 8 5 5 5 5 5 5 5 5 5 5 5 5 8 2 4 4 4 4
4 4 4 2 8 8 8 8 8 8 8 8 5 5 5 5 5 8 2 4 4 4 4
4 4 4 4 2 2 2 2 2 2 2 2 8 5 5 5 5 8 2 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 2 8 5 5 5 5 8 2 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 2 8 5 5 5 5 8 2 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 2 8 5 5 5 5 8 2 4 4 4 4
4 4 4 4 2 4 4 4 4 4 4 2 8 8 8 8 8 8 2 4 4 4 4
4 4 4 2 8 2 4 4 4 4 4 4 2 2 2 2 2 2 4 4 4 4 4
4 4 2 8 8 2 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 2 2 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
```
Match: False
Pixels Off: 209
Size Correct: True
Color Palette Correct: False
Color Count Correct: False
Score: 129.81366459627333

## Example 3:
Input:
```
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 1 1 1 4 4 4 4 4 4 4 4 4
4 4 4 1 1 1 4 4 4 4 4 4 4 4 4
4 4 4 1 1 1 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 1 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 1 1 1 1 1 4 4 4 4 4 4
4 4 4 4 1 4 4 1 1 1 1 4 4 4 4
4 4 4 4 1 1 1 1 1 1 1 4 4 4 4
4 4 4 4 1 1 1 1 1 1 1 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
```
Expected Output:
```
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 2 2 2 2 2 4 4 4 4 4 4 4 4
4 4 2 1 1 1 2 4 4 4 4 4 4 4 4
4 4 2 1 1 1 2 4 4 4 4 4 4 4 4
4 4 2 1 1 1 2 4 4 4 4 2 2 2 4
4 4 2 2 2 2 2 4 4 4 4 2 1 2 4
4 4 4 4 4 4 4 4 4 4 4 2 2 2 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 2 2 2 2 2 2 2 4 4 4 4 4
4 4 4 2 8 8 8 8 8 2 2 2 4 4 4
4 4 4 2 8 6 6 8 8 8 8 2 4 4 4
4 4 4 2 8 8 8 8 8 8 8 2 4 4 4
4 4 4 2 8 8 8 8 8 8 8 2 4 4 4
4 4 4 2 2 2 2 2 2 2 2 2 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
```
Transformed Output:
```
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 2 2 2 4 4 4 4 4 4 4 4 4
4 4 2 8 8 8 2 4 4 4 4 4 4 4 4
4 4 2 8 5 8 2 4 4 4 4 4 4 4 4
4 4 2 8 8 8 2 4 4 4 4 4 2 4 4
4 4 4 2 2 2 4 4 4 4 4 2 8 2 4
4 4 4 4 4 4 4 4 4 4 4 4 2 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 2 2 2 2 2 4 4 4 4 4 4
4 4 4 2 8 8 8 8 8 2 2 4 4 4 4
4 4 4 2 8 2 2 8 5 8 8 2 4 4 4
4 4 4 2 8 8 8 5 5 5 8 2 4 4 4
4 4 4 2 8 8 8 8 8 8 8 2 4 4 4
4 4 4 4 2 2 2 2 2 2 2 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
```
Match: False
Pixels Off: 29
Size Correct: True
Color Palette Correct: False
Color Count Correct: False
Score: 38.666666666666686
