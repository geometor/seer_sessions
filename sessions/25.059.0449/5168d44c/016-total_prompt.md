# 5168d44c • 016 • example_3 • investigate_coder

---

## train_3

**input:**
```
0 0 3 0 0 0 0
0 2 2 2 0 0 0
0 2 3 2 0 0 0
0 2 2 2 0 0 0
0 0 3 0 0 0 0
0 0 0 0 0 0 0
0 0 3 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=448x448 at 0x7440707181D0>

**output:**
```
0 0 3 0 0 0 0
0 0 0 0 0 0 0
0 0 3 0 0 0 0
0 2 2 2 0 0 0
0 2 3 2 0 0 0
0 2 2 2 0 0 0
0 0 3 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=448x448 at 0x744070718350>
Okay, here's my analysis of the provided example, focusing on perception, structured facts, and a natural language program describing the transformation.

**Perception of Elements:**

The task involves a grid of colored pixels. The primary colors observed are green (3), red (2), and white (0).  The input and output grids have the same dimensions (7x7). The most notable change seems to be a vertical shift or re-arrangement of the colored components, while maintaining their relative positions. A red "cross" shape appears to be rotated by 180 degrees around its center. A green vertical line is copied below existing objects.

**YAML Block (Facts):**


```yaml
objects:
  - id: green_line
    type: line
    color: green
    orientation: vertical
    initial_positions: [[0,2], [2,2], [4,2], [6,2]]
  - id: red_cross
    type: shape
    color: red
    shape_type: cross
    initial_positions:  [[1,1], [1,2], [1,3], [2,1], [2,3], [3,1], [3,2], [3,3]]
relationships:
    - green_line is above red_cross
actions:
  - type: rotation
    object: red_cross
    center: [2,2]
    degrees: 180
  - type: copy
    object: green_line
    new_position: [location under other object]
```


**Natural Language Program:**

1.  **Identify Objects:** Find the vertical green line and the red cross-shaped object.
2.  **Rotate Red Cross** Rotate the Red cross by 180 degrees around its center point.
3.  **Copy Green line:** Copy the green line segments below other objects.
4.  **Combine**: combine the altered green segments and the rotated red object into an output grid, maintaining relative positions, filling remaining space with white.


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
