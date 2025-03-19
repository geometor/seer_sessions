# 4c5c2cf0 • 008 • example_1 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 2 0 0 0 0 0 0 0
0 0 0 2 2 0 2 0 0 0 0 0 0 0
0 0 0 0 0 2 2 0 0 0 0 0 0 0
0 0 0 0 2 2 0 0 0 0 0 0 0 0
0 0 0 2 0 0 4 0 4 0 0 0 0 0
0 0 0 0 0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 4 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=896x896 at 0x744068D7AF50>

**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 2 0 2 0 0 2 0 0
0 0 0 2 2 0 2 0 2 0 2 2 0 0
0 0 0 0 0 2 2 0 2 2 0 0 0 0
0 0 0 0 2 2 0 0 0 2 2 0 0 0
0 0 0 2 0 0 4 0 4 0 0 2 0 0
0 0 0 0 0 0 0 4 0 0 0 0 0 0
0 0 0 2 0 0 4 0 4 0 0 2 0 0
0 0 0 0 2 2 0 0 0 2 2 0 0 0
0 0 0 0 0 2 2 0 2 2 0 0 0 0
0 0 0 2 2 0 2 0 2 0 2 2 0 0
0 0 0 2 0 0 2 0 2 0 0 2 0 0
```

<PIL.Image.Image image mode=RGB size=896x896 at 0x744068DB7BD0>
Okay, I've reviewed the input and output grids for `train_1`. Here's my analysis:

**Perception of Task Elements:**

The task involves manipulating colored pixels within a grid. The primary colors observed are white (0), red (2), and yellow (4). The input grid contains isolated and connected regions of red and yellow pixels, all surrounded by white pixels. The output grid appears to be a modified version of the input, with some notable changes in the arrangement and potentially the quantity of colored pixels. The main change is that the output adds red to the edge of yellow.

**YAML Documentation of Facts:**


```yaml
objects:
  - type: pixel
    properties:
      color:
        - white (0)
        - red (2)
        - yellow (4)
      position: [row, column]
  - type: region
    properties:
      color: [red, yellow]
      pixels: list of pixel positions

actions:
  - name: add_pixel
    description: Adds a pixel of a specific color at a given position.
  - name: extend_region
    description: Expands an existing color by one

relationships:
  - type: adjacency
    description: Two pixels are adjacent if they share a side (not diagonal).
```


**Natural Language Program:**

1.  **Identify Regions:** Locate all contiguous regions of red (2) and yellow (4) pixels in the input grid. A region is defined as a group of pixels of the same color that are adjacent to each other (horizontally or vertically, not diagonally).
2.  **Yellow Focus:** Specifically focus on all yellow (4) regions
3.  **Yellow Expansion:** Create a copy of all of the yellow pixels
4.  **Red Border:** Around each yellow pixel, check for white adjacent cells.
5. **Fill:** Change the color of the adjacent cell to be red (2).

In essence, the transformation rule seems to create a red outline around the existing yellow shapes.

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
