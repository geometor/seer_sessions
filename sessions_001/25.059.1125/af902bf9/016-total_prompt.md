# af902bf9 • 016 • example_3 • investigate_coder

---

## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 4 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 4 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 4
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 4
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7F4C2318B450>

**output:**
```
0 0 0 0 0 0 0 0 0 0
0 4 0 4 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0
0 4 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 4
0 0 0 0 0 2 2 2 2 0
0 0 0 0 0 2 2 2 2 0
0 0 0 0 4 0 0 0 0 4
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7F4C1A589950>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves a grid of colored pixels. The primary colors involved are yellow (4), white (0), and red (2). The transformation seems to involve a selective replacement of white (0) pixels with red (2) pixels based on the positions of yellow (4) pixels. It seems to be about creating areas.

**YAML Block (Facts):**


```yaml
objects:
  - type: pixel
    properties:
      color: [0, 2, 4]  # White, Red, Yellow
      position: [row, col]
  - type: grid
    properties:
      dimensions: [10, 10]

actions:
  - name: replace_color
    parameters:
      source_color: 0  # White
      target_color: 2  # Red
    conditions:
     - "Based on proximity and arrangement of color 4 (yellow) pixels."

relationships:
  - type: proximity
    description: "Red pixels appear to fill areas defined or influenced by the position of yellow pixels"
```


**Natural Language Program:**

1.  **Identify Yellow Anchors:** Locate all yellow (4) pixels within the input grid. These act as anchor points for the transformation.

2.  **Horizontal Expansion (Conditional):** If a yellow pixel in first half rows and has an adjacent yellow pixel on either side (left and right), a red pixel is placed on top of the 0 in between.

3.  **Vertical Expansion (Conditional):** If a yellow pixel is in the second half of rows and has and adjacent yellow pixel below, create a 2x4 red area in between the yellow pixels.

In summary the input yellow pixels create a red area below or above based on their vertical position in the grid and spatial relationship with each other.

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
