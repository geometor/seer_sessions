# a3325580 • 026 • example_4 • investigate_coder

---

## train_4

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0
0 0 8 0 0 0 6 0 0 0
0 0 8 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7CE41B8FCB50>

**output:**
```
8
8
8
```

<PIL.Image.Image image mode=RGB size=64x192 at 0x7CE41B8FFBD0>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The input is a 10x10 grid containing several colored objects: a vertical line of azure (8), a vertical line of magenta (6), and a horizontal rectangle of yellow (4). The output is a 3x1 grid containing only azure (8). This suggests a selection or filtering process based on color, shape, or position. The most prominent object in the input is the vertical azure line, which is perfectly reproduced in the output.

**YAML Block (Facts):**


```yaml
objects:
  - type: line
    color: azure (8)
    orientation: vertical
    length: 3
    position: (2,3) # Column, Row of top-most pixel
  - type: line
    color: magenta (6)
    orientation: vertical
    length: 2
    position: (6,4)
  - type: rectangle
    color: yellow (4)
    orientation: horizontal
    width: 2
    height: 1
    position: (4,8)
  - type: background
    color:  white(0)

actions:
  - type: select
    target: object with color azure (8) and line and vertical
  - type: extract
    target: selected object
  
relations:
  - relation: above
    object1: azure line
    object2: yellow rectangle
  - relation: left_of
    object1: azure line
    object2: magenta line
```


**Natural Language Program:**

1.  **Identify** all objects within the input grid.
2.  **Select** the object that is a vertical line and colored azure (8).
3.  **Extract** the selected azure line.
4.  **Output** the extracted line as the result.

In essence, the program isolates and outputs the vertical azure line present in the input grid.

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
