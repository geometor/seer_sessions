# 1-3aa6fb7a • 004 • example_2 - CODE

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

<PIL.Image.Image image mode=RGB size=448x448 at 0x7AA69764A200>

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

<PIL.Image.Image image mode=RGB size=448x448 at 0x7AA6976497B0>
Okay, let's analyze the transformation between the input and output grids.

**YAML Block: Observations**

```yaml
input_grid:
  objects:
    - color: 8 (azure)
      positions: [(1, 1), (2, 1), (2, 2), (3, 4), (3, 5), (4, 5)]
      shape: Two separate L-shapes (one inverted)

output_grid:
  objects:
    - color: 8 (azure)
      positions: [(1, 1), (2, 1), (2, 2), (3, 4), (3, 5), (4, 5)]
    - color: 1 (blue)
      positions: [(1,2), (4,4)]
```

**Natural Language Program: Transformation Rule**

Here's a step-by-step description of the transformation:

1.  **Identify Azure Objects:** In the input grid, we can identify two distinct objects of color 8 (azure). Both are composed by 3 cells and shaped like 'L'.

2.  **Change specific cells:**
    *   Locate the azure object in the top-left part of the grid. If there is a white cell (0) to the right of the top cell of the object, change this cell to blue (1).
    *   Locate the azure object in the bottom-right part of the grid. If there is a white cell (0) to the left of the bottom cell of the object, change this cell to blue (1).

3.  **Preserve:** The rest of the grid, remains the same.

**Informal predicates and actions**

*   **Predicates:**
    *   `is_azure(cell)`: Checks if a cell is colored azure (8).
    *   `is_white(cell)`: Checks if a cell is colored white (0).
    *   `top_left_object(grid)`: Checks if object is in top-left position.
    *   `bottom_right_object(grid)`: Checks if object is in bottom-right position.
    *   `to_the_right_of(cell1, cell2)`: Checks if `cell2` is directly to the right of `cell1`.
    *   `to_the_left_of(cell1, cell2)`: Checks if `cell2` is directly to the left of `cell1`.

*   **Actions:**
    *   `change_color(cell, new_color)`: Changes the color of a cell.
    *   `find_object(grid, color)`: Returns a list of cells composing an object of a specific color.

```python
"""
The transformation rule identifies two azure (8) L-shaped objects in the input grid.
It changes the color of the white cell (0) to the right of the top cell of the top-left object to blue (1).
It also changes the color of the white cell (0) to the left of the bottom cell of the bottom-right object to blue (1).
The rest of the grid remains unchanged.
"""

import numpy as np

def find_objects(grid, color):
    """Finds connected regions of the specified color."""
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    def dfs(row, col, current_object):
        """Depth-first search to find connected cells."""
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or visited[row, col]
            or grid[row, col] != color
        ):
            return
        visited[row, col] = True
        current_object.append((row, col))
        dfs(row + 1, col, current_object)
        dfs(row - 1, col, current_object)
        dfs(row, col + 1, current_object)
        dfs(row, col - 1, current_object)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and not visited[row, col]:
                current_object = []
                dfs(row, col, current_object)
                objects.append(current_object)
    return objects

def get_top_cell(obj):
    """Returns the cell with the smallest row value (top-most)."""
    return min(obj, key=lambda cell: cell[0])

def get_bottom_cell(obj):
    """Returns the cell with the largest row value."""
    return max(obj, key=lambda cell:cell[0])
def transform(input_grid):
    """Transforms the input grid according to the specified rule."""
    output_grid = np.copy(input_grid)
    azure_objects = find_objects(input_grid, 8)

    # Sort objects based on top-left corner's row, then column
    azure_objects.sort(key=lambda obj: (get_top_cell(obj)[0], get_top_cell(obj)[1]))

    if len(azure_objects) >= 2:

        top_left_object = azure_objects[0]
        bottom_right_object = azure_objects[-1] #select the object in the bottom-right

        #process top-left object
        top_cell = get_top_cell(top_left_object)
        right_cell = (top_cell[0], top_cell[1] + 1)

        if (
            0 <= right_cell[0] < output_grid.shape[0]
            and 0 <= right_cell[1] < output_grid.shape[1]
            and output_grid[right_cell] == 0
        ):
            output_grid[right_cell] = 1

        #process bottom-right
        bottom_cell = get_bottom_cell(bottom_right_object)
        left_cell = (bottom_cell[0], bottom_cell[1]-1)

        if (
            0 <= left_cell[0] < output_grid.shape[0]
            and 0 <= left_cell[1] < output_grid.shape[1]
            and output_grid[left_cell] == 0
            ):
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

<PIL.Image.Image image mode=RGB size=448x448 at 0x7AA697635300>

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

<PIL.Image.Image image mode=RGB size=448x448 at 0x7AA697635390>
Okay, let's analyze this second example.

**YAML Block: Observations**

```yaml
input_grid:
  objects:
    - color: 8 (azure)
      positions: [(0, 4), (0, 5), (1, 5), (2, 2), (3, 2), (3, 3), (5, 4), (6, 3), (6, 4)]
      shape: Three separate L-shapes.

output_grid:
  objects:
    - color: 8 (azure)
      positions:  [(0, 4), (0, 5), (1, 5), (2, 2), (3, 2), (3, 3), (5, 4), (6, 3), (6, 4)]
    - color: 1 (blue)
      positions: [(1,4), (2,3), (5,3)]
```

**Natural Language Program: Transformation Rule**

Here's a step-by-step description of the transformation:

1.  **Identify Azure Objects:** The input grid contains three distinct objects of color 8 (azure). Each object is composed of 3 cells and forms an "L" shape.

2.  **Change specific cells based on position:**
    *   **Top-Right Object:** Consider the object in the top-right. Change the color of the white cell (0) to the left of *the bottom cell* of this object to blue (1).
    *   **Middle-Left Object**: Consider the L-shaped object positioned in the middle-left area. Change the color of the white (0) cell at the right of *the top cell* to blue (1).
    *   **Bottom-Right Object:** Find the L-shaped object in the bottom area of the grid. Change the color of the white cell (0) at the left of *the top cell* to blue (1).

3.  **Preservation:**  All other cells in the grid, including the azure objects, remain unchanged.

**Informal predicates and actions**

*   **Predicates:**
    *   `is_azure(cell)`: Checks if a cell is colored azure (8).
    *   `is_white(cell)`: Checks if a cell is colored white (0).
    *   `top_right_object(grid)`: Locates an object in the top-right.
    *  `middle_left_object(grid)`: Locates an object in the middle-left.
    *   `bottom_object(grid)`: Locates an object at bottom of grid
    *   `to_the_right_of(cell1, cell2)`: Checks if `cell2` is directly to the right of `cell1`.
    *   `to_the_left_of(cell1, cell2)`: Checks if `cell2` is directly to the left of `cell1`.
    *  `top_cell(object)`: Returns the highest cell of object.
    *  `bottom_cell(object)`: Returns the lowest cell of object.

*   **Actions:**
    *   `change_color(cell, new_color)`: Changes the color of a cell.

```python
import numpy as np

def find_objects(grid, color):
    """Finds connected regions of the specified color."""
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    def dfs(row, col, current_object):
        """Depth-first search to find connected cells."""
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or visited[row, col]
            or grid[row, col] != color
        ):
            return
        visited[row, col] = True
        current_object.append((row, col))
        dfs(row + 1, col, current_object)
        dfs(row - 1, col, current_object)
        dfs(row, col + 1, current_object)
        dfs(row, col - 1, current_object)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and not visited[row, col]:
                current_object = []
                dfs(row, col, current_object)
                objects.append(current_object)
    return objects

def get_top_cell(obj):
    """Returns the cell with the smallest row value (top-most)."""
    return min(obj, key=lambda cell: cell[0])

def get_bottom_cell(obj):
    """Returns the cell with the largest row value."""
    return max(obj, key=lambda cell:cell[0])

def transform(input_grid):
    """Transforms the input grid according to the specified rule."""
    output_grid = np.copy(input_grid)
    azure_objects = find_objects(input_grid, 8)
    azure_objects.sort(key=lambda obj: (get_top_cell(obj)[0], get_top_cell(obj)[1]))

    if len(azure_objects) >= 3:
        top_right_object = azure_objects[-1]  # Select the object in the top-right
        middle_left_object = azure_objects[1] #Select the object in the middle
        bottom_object = azure_objects[0] #select the object in the bottom

        # Top-right object: Change cell to the left of the bottom cell
        bottom_cell = get_bottom_cell(top_right_object)
        left_of_bottom = (bottom_cell[0], bottom_cell[1] - 1)
        if (
            0 <= left_of_bottom[0] < output_grid.shape[0]
            and 0 <= left_of_bottom[1] < output_grid.shape[1]
            and output_grid[left_of_bottom] == 0
        ):
            output_grid[left_of_bottom] = 1

        # Middle-left object: Change cell to the right of the top cell.
        top_cell = get_top_cell(middle_left_object)
        right_of_top = (top_cell[0], top_cell[1] + 1)
        if (
            0 <= right_of_top[0] < output_grid.shape[0]
            and 0 <= right_of_top[1] < output_grid.shape[1]
            and output_grid[right_of_top] == 0
            ):
            output_grid[right_of_top]=1

        # Bottom object: Change the cell to the left of the top cell.
        top_cell = get_top_cell(bottom_object)
        left_of_top = (top_cell[0], top_cell[1] -1)

        if (
             0 <=  left_of_top[0] < output_grid.shape[0]
            and 0 <= left_of_top[1] < output_grid.shape[1]
            and output_grid[left_of_top] == 0
        ):
            output_grid[left_of_top] = 1

    return output_grid
```

**INSTRUCTIONS**

- generate a Python module to represent the natural language program 
- follow the template below
- all common math and science libraries are available
- create docstring only at top - but comment the workflow in the function
- use helper functions for common operations like finding objects, counting,
  measuring, moving, etc. 

remember - we are working iteratively - so this code will inform your future
self as we converge on the solution

*template:*

```python
"""
{ natural language description of the transformation rule }
"""

{ imports }

def transform(input_grid):
    # initialize output_grid

    # change output pixels 

    return output_grid

```
