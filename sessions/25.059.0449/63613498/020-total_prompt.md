# 63613498 • 020 • example_3 • investigate_coder

---

## train_3

**input:**
```
0 4 0 5 0 0 0 1 0 0
4 4 4 5 0 0 1 1 1 0
0 0 0 5 0 0 0 0 0 0
5 5 5 5 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 3 3 0 0
0 0 0 0 0 0 3 0 0 0
0 6 6 6 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7440707B2650>

**output:**
```
0 4 0 5 0 0 0 5 0 0
4 4 4 5 0 0 5 5 5 0
0 0 0 5 0 0 0 0 0 0
5 5 5 5 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 3 3 0 0
0 0 0 0 0 0 3 0 0 0
0 6 6 6 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7440707B33D0>
Okay, let's analyze this input-output example to understand the transformation.

**Perception of Elements:**

*   The input and output are grids of the same dimensions (10x10).
*   Each cell contains a single digit integer (0-9), representing colors.
*   There are distinct colored regions (objects) formed by contiguous blocks of the same color.
*   The colors present are white(0), yellow(4), grey(5), blue(1), green(3), and magenta(6).
*   Comparing Input and output, we can see a change related to blue(1) and grey(5) color.

**YAML Block (Facts):**


```yaml
objects:
  - id: 1
    color: yellow (4)
    shape: irregular
    position: top-left corner
  - id: 2
    color: grey (5)
    shape: irregular
    position: top, adjacent to yellow
  - id: 3
    color: blue (1)
    shape: horizontal line
    position: top-right, adjacent to grey
  - id: 4
    color: green (3)
    shape: vertical line/square
    position: middle-right
  - id: 5
    color: magenta (6)
    shape: L-shape
    position: bottom-left

actions:
  - type: replace
    target: blue(1)
    replacement: grey(5)
    condition: "all blue object"

relationships:
  - type: adjacency
    object1: yellow(4)
    object2: grey(5)
  - type: adjacency
    object1: grey(5)
    object2: blue(1)

```


**Natural Language Program:**

1.  Identify all the blue(1) colored pixels in the input grid.
2.  Change the blue(1) pixels to the grey(5) color.
3.  All the other pixels and objects will be kept without any change.
4.  Output is the final grid with the transformed object.

In essence, the transformation replaces all instances of blue (1) with grey (5). The positions and shapes of other colored regions remain unchanged.

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
