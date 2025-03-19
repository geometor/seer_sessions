# 60b61512 • 002 • example_2 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 0 0 0 0 0
4 4 4 0 0 0 0 0 0
4 0 4 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0
0 0 0 0 0 4 4 0 0
0 0 0 0 0 0 4 4 0
0 0 0 0 0 4 0 4 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=576x576 at 0x7F0A59D62E90>

**output:**
```
0 0 0 0 0 0 0 0 0
4 4 4 0 0 0 0 0 0
4 7 4 0 0 0 0 0 0
7 7 4 0 0 0 0 0 0
0 0 0 0 0 4 4 7 0
0 0 0 0 0 7 4 4 0
0 0 0 0 0 4 7 4 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=576x576 at 0x7F0A59D17070>

## train_2

**input:**
```
0 0 0 0 0 0 0 0 0
4 4 4 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0
4 4 4 0 0 0 0 0 0
0 0 0 0 0 4 4 4 0
0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=576x576 at 0x7F0A59D16490>

**output:**
```
0 0 0 0 0 0 0 0 0
4 4 4 0 0 0 0 0 0
7 4 4 0 0 0 0 0 0
4 4 4 0 0 0 0 0 0
0 0 0 0 0 4 4 4 0
0 0 0 0 0 7 4 7 0
0 0 0 0 0 7 4 7 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=576x576 at 0x7F0A59D174D0>
<PIL.Image.Image image mode=RGB size=1212x1202 at 0x7F0A627D9DB0>Okay, let's analyze this ARC task.

**Perception of Elements:**

The task involves 2D grids where cells have integer values representing colors. The primary colors involved seem to be yellow (4) and orange (7). The background is white (0). The transformation seems to involve some interaction between adjacent yellow pixels, potentially changing some of them to orange.

**YAML Block (Facts):**


```yaml
objects:
  - type: pixel
    properties:
      color:
        - white (0)
        - yellow (4)
        - orange (7)
      position: [row, column]
  - type: grid
    properties:
      dimensions: [height, width]
      cells: list of pixels

actions:
  - name: change_color
    input: pixel, color
    output: modified pixel

relationships:
  - adjacency: pixels can be adjacent (horizontally or vertically)
```


**Natural Language Program:**

1. **Identify Yellow Clusters:** Locate all contiguous clusters of yellow (4) pixels in the input grid.  A cluster is defined as one or more yellow pixels that are directly adjacent to each other (horizontally or vertically, not diagonally).

2. **Inner vs. Outer:** Within each yellow cluster, determine "inner" and "outer" yellow pixels. An "outer" yellow pixel is one that is adjacent to at least one white (0) pixel. An "inner" yellow pixel is one that is *only* adjacent to other yellow pixels. If the element has 1 dimension of only 1 cell then all the pixels in this cluster should be considered outer.

3. **Conditional Color Change:** For each yellow cluster within an input, if an "inner" yellow pixel is detected then transform this "inner" pixel into orange (7). Do not change any outer pixels to orange.

4. **Output:** Create the output grid by applying the color changes to the original input grid.

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
