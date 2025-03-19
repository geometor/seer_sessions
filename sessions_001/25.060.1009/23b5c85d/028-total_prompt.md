# 23b5c85d • 028 • example_5 • investigate_coder

---

## train_5

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 1 1 1 1 0 0 0 0 0 0
0 1 1 1 1 1 1 1 1 0 0 4 4 0 0
0 1 1 1 1 1 1 1 1 0 0 4 4 0 0
0 1 1 1 1 1 1 1 1 0 0 0 0 0 0
0 1 1 1 1 1 1 1 1 0 0 0 0 0 0
0 1 1 1 1 1 1 1 1 0 0 0 0 0 0
0 1 1 1 1 1 1 1 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 6 6 6 6 6 6 0 0 0 0
0 0 0 0 6 6 6 6 6 6 6 0 0 0 0
0 0 0 0 6 6 6 6 6 6 6 0 0 0 0
0 0 0 0 6 6 6 6 6 6 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=960x1152 at 0x7FC253D0FAD0>

**output:**
```
4 4
4 4
```

<PIL.Image.Image image mode=RGB size=128x128 at 0x7FC252BC77D0>
Okay, let's analyze this ARC-AGI task example.

**Perception of Elements:**

The input is a grid of colored pixels. There are distinct rectangular regions of blue (1), magenta (6), and yellow (4). The output is a much smaller grid containing only the yellow (4) pixels. It appears the task involves extracting a specific colored region.

**YAML Block (Facts):**


```yaml
objects:
  - type: rectangle
    color: blue
    id: blue_rect
  - type: rectangle
    color: magenta
    id: magenta_rect
  - type: rectangle
    color: yellow
    id: yellow_rect
  - type: grid
    id: input_grid
  - type: grid
    id: output_grid

properties:
  - object: blue_rect
    attribute: position
    value: (top-middle)
  - object: magenta_rect
    attribute: position
    value: (bottom-middle)
  - object: yellow_rect
    attribute: position
    value: (embedded within blue_rect, right side)
  - object: input_grid
    attribute: dimensions
    value: (18 x 15)
  - object: output_grid
    attribute: dimensions
    value: (2 x 2)
  - object: yellow_rect
     attribute: dimensions
     value: (2x2)

actions:
  - type: extraction
    agent: SEER
    target: yellow_rect
    source: input_grid
    destination: output_grid

relationships:
  - type: contains
    subject: input_grid
    object: blue_rect
  - type: contains
    subject: input_grid
    object: magenta_rect
  - type: contains
    subject: input_grid
    object: yellow_rect
  - type: spatial
    relation: "within"
    subject: yellow_rect
    object: blue_rect

```


**Natural Language Program:**

1.  **Identify** the rectangular region of yellow (4) pixels within the input grid.
2.  **Extract** this yellow region.
3.  **Output** the extracted yellow region as a new grid.

In essence, the transformation rule is to isolate and output the yellow sub-grid.

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
