# 952a094c • 016 • example_3 • investigate_coder

---

## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 1 1 0 0 0
0 1 2 0 0 5 1 0 0 0
0 1 0 0 0 0 1 0 0 0
0 1 6 0 0 3 1 0 0 0
0 1 1 1 1 1 1 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7F4C1B703250>

**output:**
```
3 0 0 0 0 0 0 6 0 0
0 1 1 1 1 1 1 0 0 0
0 1 0 0 0 0 1 0 0 0
0 1 0 0 0 0 1 0 0 0
0 1 0 0 0 0 1 0 0 0
0 1 1 1 1 1 1 0 0 0
5 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7F4C1B701250>
Okay, here's my analysis of the provided input-output example, structured as a report:

**Perception of Elements:**

The task involves a grid of colored pixels. The primary colors involved are:

*   **Background:** White (0)
*   **Border/Frame:** Blue (1)
*   **Inner Objects:** Red (2), Green (3), Gray (5), Magenta (6)

The most prominent feature is a blue rectangular border enclosing other colored pixels within it. The inner pixels seem to be rearranged in the output.

**YAML Block (Facts):**


```yaml
objects:
  - id: background
    color: white
    role: background
  - id: border
    color: blue
    shape: rectangle
    role: encloses other objects
  - id: inner_objects
    colors: [red, green, gray, magenta]
    role: enclosed by border, rearranged in output

actions:
  - name: rearrangement
    description: Inner objects' positions change within the border.
    details: the location of inner objects is mirrored across both horizontal and vertical axis

relationships:
  - type: enclosure
    subject: border
    object: inner_objects
```


**Natural Language Program:**

1.  **Identify the rectangular blue border.** This border defines the active area for the transformation.
2. **Identify the inner objects that exist withing the border.** These are all colored cells in the border that have colors different than white and blue.
3.  **Mirror the location of inner object.** The mirrored locations are found by:
    - find the axis of symmetry for both horizontal and vertical direction by excluding outer blue border.
    - swap the location of the objects across the axis of symmetry.

In summary, the transformation involves mirroring the position of special color that reside within a rectangular blue border.

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
