# e73095fd • 012 • example_3 • investigate_coder

---

## train_3

**input:**
```
0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0 5 5 5 5 5 0
5 5 5 5 5 5 5 5 5 5 5 5 0 0 0 5 0
0 0 0 0 0 5 0 0 0 0 0 5 0 0 0 5 5
0 0 0 5 5 5 5 0 0 0 0 5 0 0 0 5 0
5 5 5 5 0 0 5 0 0 0 0 5 5 5 5 5 0
0 0 0 5 0 0 5 0 0 0 0 0 5 0 0 0 0
0 0 0 5 0 0 5 0 0 0 0 0 5 0 0 0 0
0 0 0 5 5 5 5 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 5 0 0 0 0 5 5 5 5 0 0 0
5 5 5 5 5 5 5 5 5 5 5 0 0 5 0 0 0
0 0 0 0 0 5 0 0 0 0 5 0 0 5 0 0 0
0 0 0 0 0 5 0 0 0 0 5 5 5 5 0 0 0
0 0 0 0 0 5 0 0 0 0 0 0 5 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=1088x960 at 0x716635B76250>

**output:**
```
0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0 5 5 5 5 5 0
5 5 5 5 5 5 5 5 5 5 5 5 4 4 4 5 0
0 0 0 0 0 5 0 0 0 0 0 5 4 4 4 5 5
0 0 0 5 5 5 5 0 0 0 0 5 4 4 4 5 0
5 5 5 5 4 4 5 0 0 0 0 5 5 5 5 5 0
0 0 0 5 4 4 5 0 0 0 0 0 5 0 0 0 0
0 0 0 5 4 4 5 0 0 0 0 0 5 0 0 0 0
0 0 0 5 5 5 5 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 5 0 0 0 0 5 5 5 5 0 0 0
5 5 5 5 5 5 5 5 5 5 5 4 4 5 0 0 0
0 0 0 0 0 5 0 0 0 0 5 4 4 5 0 0 0
0 0 0 0 0 5 0 0 0 0 5 5 5 5 0 0 0
0 0 0 0 0 5 0 0 0 0 0 0 5 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=1088x960 at 0x716635B76AD0>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves a grid of pixels, with two primary colors observed: gray (5) and white (0). The transformation seems to involve a selective replacement of some gray (5) pixels with yellow (4) pixels. The shape formed by the gray pixels appears to be significant. The white pixels seem to act like a background and don't directly participate into the core transformation.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    properties:
      rows: 15
      columns: 17
      cells: pixels
      colors: [0, 5, 4]  # white, gray, yellow

  - type: shape
    properties:
      color: 5 # gray
      connectivity: contiguous

  - type: pixel
    properties:
       color: int
       position: (row, col)

actions:
  - name: replace_color
    properties:
      source_color: 5
      target_color: 4
      location: "specific gray pixels"

relationships:
  - type: inside
    subject: pixel
    object: shape
  - type: adjacent
    subject: pixel
    object: pixel
```


**Natural Language Program:**

1.  **Identify the Shape:** Find the contiguous region(s) of gray (5) pixels within the input grid.
2.  **Selective Replacement:** Within the identified gray shape, replace some of the gray (5) pixels with yellow (4) pixels. The positions that are replace appear to be the pixels that form, more or less, a 3x2 block. The replacement seems to be happening at gray "corners".

The core of the rule is the *selective* replacement, it is difficult to know the precise geometrical relationship that triggers it without seeing other examples. However, the described program *should* suffice for a starting point.

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
