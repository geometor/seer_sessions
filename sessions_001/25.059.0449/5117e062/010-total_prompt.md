# 5117e062 • 010 • example_2 • investigate_coder

---

## train_2

**input:**
```
0 0 0 0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 2 2 2 0 0 0
0 0 0 0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 0 0 0 0 0 0 0 0
0 0 3 8 0 0 0 0 0 0 0 0 0
0 0 0 3 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 0 1 0 0 0
0 0 0 0 0 0 0 1 1 1 0 0 0
0 0 0 0 0 0 0 1 1 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=832x832 at 0x744068E60AD0>

**output:**
```
0 3 3
3 3 0
0 3 3
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x744068E61950>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves a transformation of a larger grid (input) into a smaller grid (output). The input grid contains multiple colored objects (contiguous blocks of pixels of the same color), while the output grid seems to focus on a specific color (green, represented by the number 3). The output appears to be a zoomed-in, simplified, or cropped view of a section of the input. Specifically it is focusing on one object.

**YAML Block (Facts):**


```yaml
objects:
  - name: input_grid
    type: grid
    properties:
      - width: 13
      - height: 13
      - colors: [0, 1, 2, 3, 8]
  - name: output_grid
    type: grid
    properties:
      - width: 3
      - height: 3
      - colors: [0, 3]
  - name: green_object
    type: object
    properties:
      - color: 3
      - shape: irregular
      - location: near the center of the input_grid

actions:
  - name: extract
    description: Select a region of interest.
  - name: simplify
    description: keep only some colors
relationships:
  - type: contains
    from: input_grid
    to: green_object
  - type: represents
    from: output_grid
    to: green_object

```


**Natural Language Program:**

1.  **Identify the green object (color 3):** Locate the contiguous block of pixels with the value '3' in the input grid.
2.  **Define the object bounding box:**  Determine a minimal rectangle that contains only the object with color 3.
3.  **Extract:** Create the output using the bounding box.


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
