# aedd82e4 • 014 • example_3 • investigate_coder

---

## Example 3

**input:**
```
2 2 0 0
0 2 0 0
2 2 0 2
0 0 0 0
0 2 2 2
```

<PIL.Image.Image image mode=RGB size=256x320 at 0x7DCBFC29BA60>

**output:**
```
2 2 0 0
0 2 0 0
2 2 0 1
0 0 0 0
0 2 2 2
```

<PIL.Image.Image image mode=RGB size=256x320 at 0x7DCBFC29BEB0>
Okay, here's my analysis of the provided example, formatted as a report:

**Perception of Elements:**

The task involves a grid of colored pixels. The primary colors observed are red (2) and white (0). The transformation seems to involve a very localized change: a single red pixel changes to blue (1). The location of this change is specific, targeting a red pixel that appears isolated among other colors within the grid.

**YAML Block - Facts:**


```yaml
objects:
  - type: grid
    properties:
      rows: 5
      columns: 4
      cells:
        values: [0, 1, 2]  # white, blue, red
  - type: pixel
    properties:
      color:
        - white
        - red
        - blue
      location: [row, column]

actions:
  - name: change_color
    agent: unknown
    target: pixel
    precondition:
      color: red
      context: "isolated, surrounded by or adjacent to white pixels in specific pattern"
    postcondition:
      color: blue

relationships:
  - type: adjacency
    properties:
    pixels can be adjacent horizontally, vertically

```


**Natural Language Program:**

1.  **Identify Target:** Locate the red (2) pixel in the input grid that is in the following configuration: it is at coordinates (2,3), i.e. row 3, last column.
2. **Change Color:** If such configuration is present, recolor the red pixel from red (2) to blue (1).

Essentially the rule is:
Find the red pixel at row 3, last column and change it's color to blue.

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
