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

<PIL.Image.Image image mode=RGB size=448x448 at 0x720C51F12D40>

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

<PIL.Image.Image image mode=RGB size=448x448 at 0x720C51F13BB0>

*text:*
Okay, let's analyze the transformation between the input and output grids.

**YAML Description**

```yaml
observations:
  input_grid:
    objects:
      - color: 8
        shape: two separate 2x1 vertical shapes and two single 1x1 squares.
        position: 
          - One 2x1 shape at (1,1), (2,1)
          - One 1x1 shape at (2,2)
          - One 2x1 shape at (3,4), (4,4)
          - One 1x1 shape at (3,5)
    background_color: 0
    size: 7x7

  output_grid:
      - color: 8
        shape: same as input.
        position: same as input.
      - color: 1
        shape: 1x1.
        position: replaces single square objects of color 8.
    background_color: 0
    size: 7x7

```

**Natural Language Program**

Here's a step-by-step description of the transformation rule:

1.  **Identify Objects:** In the input grid, locate all the objects that are azure (color 8).
2.  **Categorize:** Identify if an object of colour 8 consists of 2 vertically stacked squares, or a single 1x1 square.
3.  **Conditional Replacement:** All single azure (color 8) square objects are replaced by blue (color 1).
4. **Preservation:** All other azure objects, and empty cells maintain their original color.

In essence, single-celled azure objects are replaced with blue, while others, bigger objects, are preserved, as well as the white background.


*text:*
```python
"""
Identifies single-celled azure (8) objects in the input grid and replaces them with blue (1) objects in the output grid. All other azure colored objects, and other cells, are preserved.
"""

import numpy as np

def get_objects(grid):
    """
    Finds contiguous objects of the same color in a grid.
    Returns a list of objects, where each object is a list of (row, col) coordinates.
    """
    visited = set()
    objects = []

    def dfs(row, col, color, current_object):
        if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] != color:
            return
        visited.add((row, col))
        current_object.append((row, col))
        dfs(row + 1, col, color, current_object)
        dfs(row - 1, col, color, current_object)
        dfs(row, col + 1, color, current_object)
        dfs(row, col - 1, color, current_object)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if (row, col) not in visited:
                current_object = []
                dfs(row, col, grid[row, col], current_object)
                if current_object:
                    objects.append(current_object)
    return objects

def transform(input_grid):
    """
    Transforms the input grid according to the rule: single-cell azure objects
    are replaced with blue, while multi-celled azure objects and background are preserved.
    """
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Get all objects in the grid
    objects = get_objects(input_grid)

    # Iterate through the objects
    for obj in objects:
        # Check if the object is azure (color 8) and has a size of 1
        if len(obj) == 1 and input_grid[obj[0][0], obj[0][1]] == 8:
            # Replace the single-cell azure object with blue (color 1)
            output_grid[obj[0][0], obj[0][1]] = 1

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

<PIL.Image.Image image mode=RGB size=448x448 at 0x720C51F12980>

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

<PIL.Image.Image image mode=RGB size=448x448 at 0x720C51F124D0>
**Instructions**

- Describe in natural language the step-by-step transformation observed between the input and output grids.
- Focus on identifying objects, their properties (predicates), and the actions performed on them.
- Be as clear and concise as possible, providing a complete description of the transformation rule.
