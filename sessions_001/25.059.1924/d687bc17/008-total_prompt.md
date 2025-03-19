# d687bc17 • 008 • refine_coder

---

Previous Code:
```python
"""
Preserves a frame of blue (1) pixels and duplicates interior pixels of other colors directly below their original positions.
"""

import numpy as np

def find_frame(grid):
    # Find the bounding box of the blue (1) pixels.
    rows, cols = np.where(grid == 1)
    if len(rows) == 0:  # No blue pixels, no frame
        return None
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return (min_row, max_row, min_col, max_col)

def duplicate_interior_pixels(input_grid, frame):
    # Duplicate interior pixels (non-blue) within the frame.
    output_grid = np.copy(input_grid)
    min_row, max_row, min_col, max_col = frame

    for r in range(min_row + 1, max_row):
        for c in range(min_col + 1, max_col):
            if input_grid[r, c] != 1:
                # Find the next available row below within the frame
                for next_row in range(r + 1, max_row + 1):
                    if output_grid[next_row,c] == 1:
                       output_grid[next_row, c] = input_grid[r, c]
                       break  # Only one duplicate per pixel
    return output_grid

def transform(input_grid):
    # Find the frame.
    frame = find_frame(input_grid)
    if frame is None:
        return input_grid  # No frame, return original grid

    # Duplicate interior pixels.
    output_grid = duplicate_interior_pixels(input_grid, frame)

    return output_grid
```

Train Set Results:
Okay, let's analyze the results of the provided code on the training examples and refine the natural language program accordingly.

**General Assessment and Strategy**

The initial code focuses on identifying a "frame" of blue pixels and duplicating the non-blue pixels within that frame to the row directly below. This approach works for the first example, but fails on subsequent examples. The core issue is that the concept of a "frame" is too restrictive and doesn't generalize to the broader pattern. The new examples indicate that the blue pixels define a boundary, and interior non-blue pixels get duplicated *downwards* until they hit a blue pixel or another non-blue pixel (or edge of the grid). The duplication occurs for empty cells (white).

The strategy should involve these steps:

1.  **Re-evaluate Object Identification:** Instead of a "frame," we should identify "boundary" pixels (blue) and "movable" pixels (non-blue).
2.  **Re-define Action:** The action is not simple duplication, but a downward "drop" or "fill" of movable pixels within the boundary.
3. **Iteratively check for empty spots:** look down each column within the blue boundary.

**Example Analysis and Metrics**

To better understand the transformations, let's represent them using numpy.

```python
import numpy as np

def show_grid(grid, label):
    print(f'-- {label} --')
    print(grid)

# Example 1:
input_grid1 = np.array([
    [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
    [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
    [6, 6, 1, 1, 1, 1, 1, 1, 1, 1, 6, 6],
    [6, 6, 1, 6, 6, 6, 6, 6, 6, 1, 6, 6],
    [6, 6, 1, 6, 6, 6, 6, 6, 6, 1, 6, 6],
    [6, 6, 1, 6, 6, 6, 6, 6, 6, 1, 6, 6],
    [6, 6, 1, 1, 1, 1, 1, 1, 1, 1, 6, 6],
    [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
    [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
])
output_grid1 = np.array([
    [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
    [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
    [6, 6, 1, 1, 1, 1, 1, 1, 1, 1, 6, 6],
    [6, 6, 1, 6, 6, 6, 6, 6, 6, 1, 6, 6],
    [6, 6, 1, 6, 6, 6, 6, 6, 6, 1, 6, 6],
    [6, 6, 1, 6, 6, 6, 6, 6, 6, 1, 6, 6],
    [6, 6, 1, 1, 1, 1, 1, 1, 1, 1, 6, 6],
    [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
    [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
])
show_grid(input_grid1, 'input 1')
show_grid(output_grid1, 'output 1')

# Example 2:
input_grid2 = np.array([
[1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 3, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 1],
[1, 1, 1, 1, 1, 1, 1]
])

output_grid2 = np.array([
[1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 3, 0, 0, 1],
[1, 0, 0, 3, 0, 0, 1],
[1, 1, 1, 1, 1, 1, 1]
])
show_grid(input_grid2, 'input 2')
show_grid(output_grid2, 'output 2')

# Example 3
input_grid3 = np.array([
    [1, 1, 1, 1, 1, 1],
    [1, 5, 5, 5, 5, 1],
    [1, 5, 5, 1, 5, 1],
    [1, 5, 1, 5, 5, 1],
    [1, 1, 1, 1, 1, 1]
])

output_grid3 = np.array([
    [1, 1, 1, 1, 1, 1],
    [1, 5, 5, 5, 5, 1],
    [1, 5, 5, 1, 5, 1],
    [1, 5, 1, 5, 5, 1],
    [1, 1, 1, 1, 1, 1]
])

show_grid(input_grid3, "input 3")
show_grid(output_grid3, "output 3")
```

**YAML Facts**

```yaml
objects:
  - name: boundary
    color: blue (1)
    description: Defines the outer limits within which movable pixels operate.  Pixels move *within* the boundary created by the blue.
    behavior: Static, defines the operational area.

  - name: movable
    color: non-blue (not 1)
    description: Pixels that are subject to movement.
    behavior: Moves downwards within the boundary, filling empty spaces until blocked.

  - name: empty_space
    color: white (0)
    description: Represents cells available for movable pixels to occupy.
    behavior: Becomes occupied by the color of movable pixels above it.

actions:
  - name: drop_fill
    description: Movable pixels move downwards within the boundary defined by blue pixels, filling empty spaces.
    trigger: Iterating through columns within the boundary, from top to bottom.
    constraints: Movement stops when a movable pixel encounters a blue pixel, another non-blue, non-white, pixel, or the edge of the boundary.
```

**Natural Language Program**

1.  **Identify the Boundary:** Find all blue (1) pixels. These pixels form a closed boundary, but the boundary doesn't have to be rectangular.

2.  **Iterate Through Columns:** For each column within the horizontal bounds of the blue pixels:

3.  **Drop Fill:** Starting from the top row and moving downwards within the boundary:
    *   If a non-blue, non-white pixel is found, "drop" or copy that pixel's color value downwards, filling empty(white) pixels below, one at a time.

4.  **Stopping Condition:** Stop dropping a pixel's color when:
    *   A blue (1) pixel is encountered.
    *   Another non-blue, non-white, pixel is encountered.
    *   The bottom edge of the boundary (or grid) is reached.

5. If the input does not contain any blue pixels - return the input unchanged.

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
{{ natural language description of the transformation rule }}
"""

{{ imports }}

def transform(input_grid):
    # initialize output_grid

    # change output pixels 

    return output_grid

```
