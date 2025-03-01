# f25fbde4 • 004 • example_1 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 4 4 0 0 0 0 0
0 4 4 4 4 0 0 0 0
0 0 4 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=576x576 at 0x716635B762D0>

**output:**
```
0 0 4 4 4 4 0 0
0 0 4 4 4 4 0 0
4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4
0 0 4 4 4 4 0 0
0 0 4 4 4 4 0 0
```

<PIL.Image.Image image mode=RGB size=512x384 at 0x716635B76B50>
Okay, here's my analysis of the provided input-output example pair:

**Perception of Elements:**

The task involves a transformation of a 2D grid of pixels. The primary colors involved are white (0) and yellow (4). The input grid contains a cross-shaped object made of yellow pixels, centered within the grid. The output grid appears to be a filled square, encompassing the original cross shape, and also colored yellow. The output grid is smaller than the input grid.

**YAML Block - Facts:**


```yaml
objects:
  - name: cross
    color: yellow (4)
    shape: cross-like
    position: centered in the input grid
  - name: square
    color: yellow (4)
    shape: square
    position: centered in the output grid
    relation_to_cross: encompasses the original cross

actions:
  - name: fill
    description: The cross shape in the input is expanded to form a square in the output.
    affects: cross
    result: square

grid:
  input:
    dimensions: 9x9
  output:
    dimensions: 6x8

colors:
   0 : white
   4: yellow
```


**Natural Language Program:**

1.  **Identify the Object:** Locate the cross-shaped object composed of yellow (4) pixels in the input grid.
2.  **Determine Boundaries:** Find the outermost points (top, bottom, left, and right) of the cross shape.
3. **Create Bounding Box:** create a bounding rectangle using extreme points.
4.  **Fill the Bounding Box:** Change all pixels within the bounding box defined by these extreme points to yellow (4).
5. **Crop:** remove all white rows and columns on the edges.


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
