# 7447852a • 008 • example_1 • investigate_coder

---

## train_1

**input:**
```
2 0 0 0 2 0 0 0 2 0
0 2 0 2 0 2 0 2 0 2
0 0 2 0 0 0 2 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x192 at 0x70A2EC7D7D50>

**output:**
```
2 0 0 0 2 4 4 4 2 0
4 2 0 2 0 2 4 2 0 2
4 4 2 0 0 0 2 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x192 at 0x70A2EC681050>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves a transformation of a grid of colored pixels. The input grid consists of red (2) and white (0) pixels, while the output grid includes yellow (4) pixels in addition to red and white. The dimensions of the grid remain constant (3x10). The introduction of yellow pixels seems to be related to the arrangement of red pixels.

**YAML Block (Facts):**


```yaml
facts:
  - type: grid
    dimensions: 3x10
    input_colors: [red, white]
    output_colors: [red, white, yellow]
  - object: pixel
    properties:
      color: [red, white, yellow]
      position: [row, column]
  - observation: "yellow pixels appear in the output grid"
  - relationship: "The position of yellow pixels appears connected to the position of red pixels."
  - action: color change, position based

```


**Natural Language Program:**

1.  **Identify:** Locate all red (2) pixels in the input grid.
2.  **Check Neighbors:** For each red pixel, inspect its immediate neighbors *to the right* in same row.
    * If all the neighbors to the right that are in the same row are white, find the red pixels that are the next after those sequence of white pixels.
    * change those found red pixels to be yellow (4).
3. **Check Neighbors in Other Rows**:
    * For all newly created yellow pixels, color their adjacent neighbors in the row below to be that same color (4).

In summary, a red color in the input grid, where the next in same row is all white until a red pixel, those red pixels is changed to yellow, and yellow pixels make adjacent pixels in row below them to also be yellow.

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
