# 11852cab • 016 • example_3 • investigate_coder

---

## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 8 0 8 0 8 0 0
0 0 0 0 4 0 0 0 0 0
0 0 0 8 0 1 0 8 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 8 0 8 0 8 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7A608C3125D0>

**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 8 0 8 0 8 0 0
0 0 0 0 4 0 4 0 0 0
0 0 0 8 0 1 0 8 0 0
0 0 0 0 4 0 4 0 0 0
0 0 0 8 0 8 0 8 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7A608C3131B0>
Okay, let's analyze this input-output example.

**Perception of Task Elements:**

The task involves a grid of colored pixels. The colors are represented by integers 0-9. The primary colors involved in the transformation appear to be azure (8), yellow (4), and blue (1). White (0) seems to represent the background or empty space. The core change seems to involve a duplication of yellow (4) pixels in relation to the blue(1) pixel, specifically in the vertical direction.

**YAML Block (Facts):**


```yaml
objects:
  - type: pixel
    properties:
      color:
        - white (0)
        - azure (8)
        - yellow (4)
        - blue (1)
      position: [row, column]

actions:
  - name: duplicate
    object: yellow pixel
    condition: vertical adjacency to blue pixel

relationships:
  - type: adjacency
    objects: [pixel, pixel]
    directions: [vertical, horizontal, diagonal]
```


**Natural Language Program:**

1.  **Identify Key Pixels:** Locate the single blue (1) pixel within the grid.
2.  **Locate vertically adjacent pixels:** Find all of the yellow pixels that are vertically adjacent to existing yellow pixels.
3. **Duplicate Yellow:** If there are two yellow pixels arranged vertically on opposite sides of the blue one, leave them. If yellow pixels are arranged vertically adjacent only on one side of the blue pixel, replicate the single vertical line of yellow pixels onto the opposite side of the blue pixel, such that it becomes symmetrical about the blue pixel.
4.  **Preserve Other Pixels:** All other pixels, including azure (8) and white (0), remain unchanged.

In short, the transformation duplicates yellow pixels vertically based on their adjacencies, creating symmetry around the blue pixel.

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
