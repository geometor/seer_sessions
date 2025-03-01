# 7ddcd7ec • 004 • example_1 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x70A2EC7D7D50>

**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 3
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x70A2EC7D7F50>
Okay, let's analyze this input-output pair.

**Perception of the Elements:**

The task involves a grid of pixels, initially mostly white (0) with a few green (3) pixels. The transformation seems to involve extending the green pixels diagonally downwards and to the right. The initial green pixels form a 2x2 square and a single isolated pixel. The transformation creates a diagonal line of green pixels originating from each initial green pixel, extending to the bottom-right edge of the grid.

**YAML Block (Facts):**


```yaml
objects:
  - type: pixel
    color: white (0)
    property: background
  - type: pixel
    color: green (3)
    property: foreground
  - type: grid
    property: container

actions:
  - type: extension
    direction: diagonal_down_right
    object: green pixel
    constraint: grid boundary

relationships:
  - green pixels are within the grid
  - extension starts from original green pixels
  - extension continues until grid boundary
```


**Natural Language Program:**

1.  **Identify** all green (3) pixels in the input grid.
2.  For each green pixel:
    *   **Extend** a diagonal line of green pixels downwards and to the right.
    *   Continue the extension until the edge of the grid is reached (either the bottom edge, the right edge, or both).
3. All other pixels should be set to 0.

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
