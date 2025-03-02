# ba26e723 • 016 • example_3 • investigate_coder

---

## train_3

**input:**
```
4 0 4 0 4 0 4 0 4 0 4
4 4 4 4 4 4 4 4 4 4 4
0 4 0 4 0 4 0 4 0 4 0
```

<PIL.Image.Image image mode=RGB size=704x192 at 0x7CE41B95DD50>

**output:**
```
6 0 4 0 4 0 6 0 4 0 4
6 4 4 6 4 4 6 4 4 6 4
0 4 0 6 0 4 0 4 0 6 0
```

<PIL.Image.Image image mode=RGB size=704x192 at 0x7CE41B8C3DD0>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves a grid of colored pixels. The colors present are yellow (4), white (0), and magenta (6).  The input and output grids have the same dimensions (3x11). The transformation seems to involve a selective replacement of yellow (4) pixels with magenta (6) pixels.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    properties:
      dimensions: 3x11
      colors: [0, 4, 6]  # White, Yellow, Magenta

  - type: pixel
    properties:
      color:
        - 0 # White
        - 4 # Yellow
        - 6 # Magenta
      position:
        row: [0, 1, 2]
        column: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

actions:
  - type: replace_color
    agent: system
    input:
      original_color: 4 # Yellow
      new_color: 6    # Magenta
    condition: "Specific locations based on surrounding pixels"

relationships:
 - type: adjacency
   description: Pixels are adjacent horizontally and vertically.

```


**Natural Language Program:**

1.  **Identify Target Pixels:** Examine each yellow (4) pixel in the input grid.

2. **Check L and R neighbors**:
   * If a yellow pixel has another yellow pixel to its immediate left *and* to its immediate right, it becomes a magenta (6).
   * If a yellow pixel has a white pixel on its left *and* on its right, it will become magenta (6).

3.  **Otherwise:** All other pixels, keep their original value.

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
