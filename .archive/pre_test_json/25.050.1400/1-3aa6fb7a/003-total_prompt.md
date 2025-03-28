# 1-3aa6fb7a • 003 • example_2 - NLP

---

**input**
```
0 0 0 0 0 0 0
0 8 0 0 0 0 0
0 8 8 0 0 0 0
0 0 0 0 8 8 0
0 0 0 0 0 8 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=448x448 at 0x7EC90230F040>

**output**
```
0 0 0 0 0 0 0
0 8 1 0 0 0 0
0 8 8 0 0 0 0
0 0 0 0 8 8 0
0 0 0 0 1 8 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=448x448 at 0x7EC90230FB50>
**Natural Language Program:**

1. **Identify Color-8 Regions:** Find all contiguous regions of color 8 in the input grid. Consider cells to be part of the same region if they are 8-connected (horizontally, vertically, or diagonally).

2. **Process Each Region:** For each identified region of color 8, perform the following steps:
   a. **Find Top-Most Cell:** Locate the cell within the region that has the smallest row index. If there are multiple cells with the same smallest row index, choose the one with the smallest column index among them.
   b. **Find Bottom-Most Cell:** Locate the cell within the region that has the largest row index. If there are multiple cells with the same largest row index, choose the one with the smallest column index among them.
   c. **Modify Right of Top-Most:** Check the cell immediately to the right of the identified "top-most" cell. If this cell is within the grid boundaries (not outside the grid) and its current color is not 8, change its color to 1.
   d. **Modify Left of Bottom-Most:** Check the cell immediately to the left of the identified "bottom-most" cell. If this cell is within the grid boundaries (not outside the grid) and its current color is not 8, change its color to 1.

3. **Output Result:** After processing all color-8 regions, the modified grid becomes the output grid.

**YAML Block:**

```yaml
task_context: "ARC puzzle transformation"
transformation_rule: "For each connected component of color 8, modify the cell to the right of the topmost cell and the cell to the left of the bottommost cell to color 1, if they are within grid boundaries and not already color 8."
objects:
  - color_8_regions: "Connected components of cells with color 8"
predicates:
  - top_most_cell: "Cell in a region with the smallest row index (and smallest column index in case of ties)"
  - bottom_most_cell: "Cell in a region with the largest row index (and smallest column index in case of ties)"
actions:
  - identify_regions: "Find connected regions of color 8"
  - find_top_bottom_cells: "Locate the top-most and bottom-most cells within each region"
  - modify_cell_right: "Change color of the cell to the right of the top-most cell to 1 if conditions are met"
  - modify_cell_left: "Change color of the cell to the left of the bottom-most cell to 1 if conditions are met"
```
```python
"""
For each connected component of color 8, modify the cell to the right of the topmost cell and the cell to the left of the bottommost cell to color 1, if they are within grid boundaries and not already color 8.
"""

import numpy as np

def find_regions(grid, color):
    # Use DFS to find connected regions of the specified color
    visited = np.zeros_like(grid, dtype=bool)
    regions = []

    def dfs(row, col, current_region):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        current_region.append((row, col))
        # Check 8-connected neighbors
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                dfs(row + dr, col + dc, current_region)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and not visited[row, col]:
                current_region = []
                dfs(row, col, current_region)
                regions.append(current_region)
    return regions

def find_top_bottom_cells(region):
    # Find top-most and bottom-most cells in a region
    top_most = min(region, key=lambda x: (x[0], x[1]))
    bottom_most = max(region, key=lambda x: (x[0], x[1])) # corrected to use max, not min
    return top_most, bottom_most

def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find all regions of color 8
    regions = find_regions(output_grid, 8)

    # Process each region
    for region in regions:
        # Find top-most and bottom-most cells
        top_most, bottom_most = find_top_bottom_cells(region)

        # Modify cell to the right of top-most
        right_cell = (top_most[0], top_most[1] + 1)
        if right_cell[1] < cols and output_grid[right_cell] != 8:
            output_grid[right_cell] = 1

        # Modify cell to the left of bottom-most
        left_cell = (bottom_most[0], bottom_most[1] - 1)
        if left_cell[1] >= 0 and output_grid[left_cell] != 8:
            output_grid[left_cell] = 1

    return output_grid
```

**input**
```
0 0 0 0 8 8 0
0 0 0 0 0 8 0
0 0 8 0 0 0 0
0 0 8 8 0 0 0
0 0 0 0 0 0 0
0 0 0 0 8 0 0
0 0 0 8 8 0 0
```

<PIL.Image.Image image mode=RGB size=448x448 at 0x7EC90230EA40>

**output**
```
0 0 0 0 8 8 0
0 0 0 0 1 8 0
0 0 8 1 0 0 0
0 0 8 8 0 0 0
0 0 0 0 0 0 0
0 0 0 1 8 0 0
0 0 0 8 8 0 0
```

<PIL.Image.Image image mode=RGB size=448x448 at 0x7EC90230F3A0>
**Instructions**

- Describe in natural language the step-by-step transformation observed between the input and output grids.
- Focus on identifying objects, their properties (predicates), and the actions performed on them.
- Be as clear and concise as possible, providing a complete description of the transformation rule.
