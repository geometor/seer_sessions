
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
Here's an analysis of the provided examples and results, along with a strategy for improving the natural language program and the subsequent code.

**General Assessment**

The code performs a reasonable initial attempt at the transformation, identifying blue objects and attempting to create outlines and inner fills. However, the matching results are poor, with many pixels differing between the transformed output and expected output across all three examples. The strategy to resolve is:

1.  **Detailed Error Analysis**: We need to pinpoint precisely *where* the code's logic deviates from the expected output. This will be done through pixel-by-pixel comparison and by visualizing the intermediate steps (like the labeled regions) within the provided `transform` function.
2.  **Refine Object Definition**: The definition of the objects could be leading to edge cases not being covered properly.
3.  **Border and Fill Logic Adjustment**: The conditions for applying red outlines, light blue inner borders, and gray fills are not completely accurate, and need adjustments based on a careful review of the failing examples. The concept of adjacent pixels (including diagonals) may be essential.
4. **Multiple Object Handling**: Although working for multiple objects, we need to ensure that objects of the same color are not merged improperly.

**Gather Metrics**

I'll use manual analysis of the provided information rather than `tool_code` as I don't have the ability to execute it in this environment, but I'll show the process I would take if the code was runnable.

**Example 1 Analysis:**
*   **Pixels Off:** 89
*   **Size Correct:** True
*   **Color Palette Correct:** False
*   **Color Count Correct:** False
*   **Observations**:
    *   The top-left blue object is outlined correctly where adjacent to yellow or the grid edge.
    *   The top-left blue object's inner border is mostly correct.
    *   The gray fill in the center is mostly incorrect - not all pixels within the former blue object changed.
    *   The lower-right blue object is not detected correctly - it appears that only pixels adjacent to '4' yellow pixels are detected.
    *   The code is failing to convert some interior pixels of the first blue object to grey, and failing to perform the operations for the isolated lower-right blue area.

**Example 2 Analysis:**
*    **Pixels Off:** 209
*   **Size Correct**: True
*   **Color Palette Correct**: False
*    **Observations:**
    *   Very poor match
    *   The red outline is incorrect in many places, appearing inside the original shape
    *   The inner border and fill have many errors
    *   There is some extra red on some of the top row not related to any blue object.

**Example 3 Analysis:**
*   **Pixels Off**: 29
*   **Size Correct**: True
*   **Color Palette Correct**: False

*    **Observations:**
    *    Better match than example 2, worse than example 1.
    *    The top left shape is not rendered correctly.

**YAML Block - Facts**


```yaml
objects:
  - type: contiguous_region
    initial_color: blue (1)
    properties:
      - outer_border:
          color: red (2)
          condition: adjacent to yellow (4) or grid boundary
      - inner_border:
          color: light_blue (8)
          condition: blue (1) pixels adjacent to any non-blue pixel
      - interior:
          color: gray (5)
          condition: all remaining blue (1) pixels within the original region

actions:
  - name: identify_objects
    description: Locate all contiguous regions of blue (1) pixels.
  - name: create_outer_border
    description: Change pixels surrounding a blue object to red (2) if they are yellow (4) or are at the input grid boundary
  - name: create_inner_border
    description: Change the blue (1) border pixels of each object to light_blue (8) .
  - name: fill_interior
    description: Change all remaining blue (1) pixels inside each object to gray (5).
```


**Natural Language Program**

1.  **Identify Blue Objects:** Find all contiguous regions (objects) of blue (1) pixels in the input grid. Consider pixels adjacent if they share an edge *or a corner* (8-way connectivity, not just 4-way).

2.  **Create Red Outer Border:** For each blue object, examine the pixels immediately surrounding it (8-way connectivity). If a surrounding pixel is yellow (4), *or* if the surrounding pixel is outside the bounds of the input grid, change that surrounding pixel to red (2).

3.  **Create Light Blue Inner Border:** For each blue object, identify its inner border. A pixel is part of the inner border if it is blue (1) and is 8-way adjacent to any pixel that is *not* blue (1). Change these inner border pixels to light blue (8).

4.  **Fill Interior with Gray:**  After creating the borders, change all remaining blue (1) pixels within each original blue object to gray (5).

5. **Preserve All Other Colors**: Ensure all other original pixels in the input remain at their input color.

