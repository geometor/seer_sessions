# c444b776 • 012 • refine_coder

---

Previous Code:
```python
"""
1.  **Identify the Reflection Axis:** Examine the input grid to determine the axis of reflection. This can be:
    *   A **vertical line** of a single color that divides the grid into two symmetrical halves.
    *   A **horizontal line** of a single color that divides the grid into two symmetrical halves.
2.  **Reflect Across Axis:** For each cell not part of the reflection axis, find its corresponding position on the opposite side of the axis. The distance to the axis should be the same for both the original cell and its reflected counterpart. Copy the color of the original cell to the reflected position in the output grid.
3.  **Maintain Axis:** The reflection axis itself remains unchanged in the output grid.
"""

import numpy as np

def find_vertical_reflection_axis(grid):
    """Finds a vertical reflection axis if it exists."""
    rows, cols = grid.shape
    for j in range(cols):
        is_axis = True
        for i in range(rows):
            for k in range(1, min(j + 1, cols - j)):
                if j - k >= 0 and j + k < cols and grid[i, j - k] != grid[i, j + k]:
                    is_axis = False
                    break
            if not is_axis:
                break
        if is_axis:
            return j, "vertical"
    return -1, None

def find_horizontal_reflection_axis(grid):
    """Finds a horizontal reflection axis if it exists."""
    rows, cols = grid.shape
    for i in range(rows):
        is_axis = True
        for j in range(cols):
            for k in range(1, min(i + 1, rows - i)):
                if i - k >= 0 and i + k < rows and grid[i - k, j] != grid[i + k, j]:
                    is_axis = False
                    break
            if not is_axis:
                break
        if is_axis:
            return i, "horizontal"
    return -1, None

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find reflection axis
    v_axis_col, v_axis_type = find_vertical_reflection_axis(input_grid)
    h_axis_row, h_axis_type = find_horizontal_reflection_axis(input_grid)

    # Reflect based on detected axis
    if v_axis_type == "vertical":
        for i in range(rows):
            for j in range(cols):
                if j != v_axis_col:
                    distance = v_axis_col - j
                    new_col = v_axis_col + distance
                    if 0 <= new_col < cols:
                         output_grid[i, new_col] = input_grid[i, j]
    elif h_axis_type == "horizontal":
        for i in range(rows):
            for j in range(cols):
                if i != h_axis_row:
                    distance = h_axis_row - i
                    new_row = h_axis_row + distance
                    if 0 <= new_row < rows:
                        output_grid[new_row, j] = input_grid[i, j]

    return output_grid
```

Train Set Results:
Okay, let's analyze the results of running the provided code on the training examples and strategize how to improve the natural language program and the code.

**General Assessment and Strategy**

The initial code and natural language program focused on finding a single, full-grid reflection axis (either vertical or horizontal).  The results clearly show this approach is too simplistic and doesn't handle all cases.  Specifically, it fails when:

1.  **No full-grid axis exists:**  Some examples have reflections, but the "axis" isn't a single line spanning the entire grid. It might be a partial line, or the reflection might only apply to a subset of the objects.
2.  **Multiple reflections or transformations:** The current logic assumes a single reflection. There might be multiple reflections, or even different kinds of transformations altogether.
3. **Object Based Reflection:** The reflection is not always about whole grid but specific objects withing the grid.

To address these issues, the strategy should shift from a whole-grid approach to an object-based approach:

1.  **Object Identification:**  First, we need to identify individual objects within the grids. An "object" can be defined as a contiguous region of pixels of the same color.
2.  **Object Property Analysis:** For each object, we should analyze its properties, such as its shape, size, position, and color.
3.  **Transformation Detection:**  Compare objects between the input and output grids to identify transformations. This includes not only reflections but also potentially rotations, translations, color changes, or even creation/deletion of objects.
4.  **Localized Reflection:**  If a reflection is detected, determine the *local* reflection axis for that specific object, rather than assuming a global axis for the entire grid.
5. **Multiple Transformations:** Allow for possibility of multiple transformation rule for the objects in the grid.

**Metrics and Observations**

To support this, let's gather detailed metrics on a per-example basis.

**Example 1: (Correct)**
*   **Input:** 6x5, vertical green line in the center.
*   **Output:** Matches input (reflection is correct).
* **Code assessment:** Succeeded. Vertical reflection around center column correctly transforms I/O

**Example 2: (Incorrect)**
*   **Input:** 15x15, two mirrored red triangles next to a vertical black line.
*   **Output:** Input grid but with a duplicate black line.
* **Code assessment:** Failed. I believe the reflection happened across the black line which is at `input_grid[:,7]` but it should not have duplicated the black line in the reflected output.

**Example 3: (Incorrect)**

*   **Input:** 14x15, complex symmetrical shapes around a vertical axis.
*   **Output:** Mostly blank with duplicated lines.
* **Code assessment:** Failed. Similar issue as example 2, a vertical axis is found at `input_grid[:, 6]` and the black line is duplicated and there are many other errors. The expected output has some objects disappearing, which suggests we are not correctly identifying the reflected components.

**Example 4: (Incorrect)**
*   **Input:** 10x10 input grid with horizontal blue line at `input_grid[4, :]` and two yellow symmetrical shapes above and below.
*   **Output:** Has the blue line and has only one of the yellow shapes.
* **Code assessment:** Failed. A horizontal axis is found at `input_grid[4, :]`. This is a clear case of *partial reflection*, where only part of the grid is reflected.  The reflection is correct, but it's not a full-grid reflection.

**Example 5: (Incorrect)**
* **Input:** 20x20 grid with orange horizontal line at `input_grid[9,:]` with two shapes above and below.
* **Output:** has the orange line and has the shapes above and below, but the one below is missing pixels.
* **Code assessment:** Failed. The reflection happened but the objects are not correctly identified causing incorrect reflection.

**YAML Facts**

```yaml
examples:
  - id: example_1
    input_objects:
      - shape: line
        color: green
        orientation: vertical
        position: center
    output_objects:
      - shape: line
        color: green
        orientation: vertical
        position: center
    transformations:
      - type: full_grid_reflection
        axis: vertical
        axis_position: center

  - id: example_2
    input_objects:
      - shape: triangle
        color: red
        count: 2
        relation: mirrored across vertical axis
    output_objects:
       - shape: triangle
         color: red
         count: 2
         relation: mirrored across vertical axis
    transformations:
      - type: object_reflection
        axis: vertical
        axis_color: black

  - id: example_3
    input_objects:
        - shape: complex
          color: various
          relation: symmetrical across vertical axis
    output_objects: []
    transformations:
      - type: object_reflection #and deletion
        axis: vertical

  - id: example_4
    input_objects:
        - color: yellow
          count: 2
        - color: blue
          count: 1
    output_objects:
        - color: yellow
          count: 1
        - color: blue
          count: 1
    transformations:
      - type: partial_reflection
        axis: horizontal

  - id: example_5
    input_objects:
        - color: mixed
          count: 2
        - color: orange
          count: 1
    output_objects:
        - color: mixed
          count: 2
        - color: orange
          count: 1
    transformations:
        - type: partial_reflection
          axis: horizontal
```

**Natural Language Program**

1.  **Object Identification:** Identify distinct objects in the input grid. An object is a contiguous block of pixels of the same color.
2.  **Iterate through Objects:** For each object in the input grid:
3.  **Look for Reflection:** Check if a mirrored counterpart of the object exists in the output grid. "Mirrored" means the counterpart has the same shape and size but is potentially flipped (reflected) across a vertical or horizontal axis.
4. **Local Axis:** If a mirrored counterpart is found, determine the *local* axis of reflection. The axis could be a line of a specific color within the object, adjacent to the object, or even an imaginary line. The axis does not need to extend across the entire grid.
5. **Partial Reflection:** If only some objects have mirrored counterparts, perform the reflection only for those objects.
6. **Object Disappearance/Appearance:** If the Input has no mirrored objects in Output, the object disappears.
7. **Axis Persistence:** If an axis is part of the identified objects, it should remain unchanged.

This revised natural language program is a significant improvement because it handles object-specific reflections and partial reflections, which the original program did not. It also considers the idea that objects can be created or deleted. It is also much better at describing the *context* of the transformation.

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
