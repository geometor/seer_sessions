# 42a50994 • 022 • example_4 • investigate_coder

---

## train_4

**input:**
```
0 0 0 0 0 4 0 4 0
0 0 0 0 4 0 0 0 0
0 4 0 0 0 0 4 0 0
0 0 0 4 4 0 0 0 0
0 0 4 0 0 0 0 0 0
0 0 4 0 4 0 0 4 4
4 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 4 0 0
0 0 4 0 0 0 0 0 0
0 4 0 0 0 0 4 0 4
4 0 4 0 4 0 0 4 0
0 4 0 0 0 0 0 4 0
0 0 0 0 0 4 0 0 0
0 0 0 0 4 4 0 0 0
4 0 4 0 4 0 0 4 4
0 0 4 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=576x1088 at 0x7B4C05BB8E50>

**output:**
```
0 0 0 0 0 4 0 0 0
0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 4 4 0 0 0 0
0 0 4 0 0 0 0 0 0
0 0 4 0 0 0 0 4 4
0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0
0 4 0 0 0 0 4 0 4
4 0 4 0 0 0 0 4 0
0 4 0 0 0 0 0 4 0
0 0 0 0 0 4 0 0 0
0 0 0 0 4 4 0 0 0
0 0 4 0 4 0 0 4 4
0 0 4 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=576x1088 at 0x7B4BFE15CA50>
Okay, let's analyze this input-output pair.

**Perception of Elements:**

*   The input and output are grids of the same dimensions (17x9).
*   The grids contain only two colors: white (0) and yellow (4).
*   The transformation seems to involve removing some of the yellow pixels. It looks like a filter is applied.
*    Yellow pixels that have 3 or more directly adjacent neighbor with color yellow, survive, other wise, the pixels with color yellow are changed to white.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    properties:
      dimensions: 17x9
      colors: [0, 4]  # 0: white, 4: yellow
      name: input_grid

  - type: grid
    properties:
      dimensions: 17x9
      colors: [0, 4]
      name: output_grid

  - type: pixel
    properties:
        color: int # 0, or 4
        neighbors:
            type: list
            description: "list of adjacent pixels"

actions:
  - name: filter_yellow_pixels
    description: Removes yellow pixels based on neighbor count.
    input: input_grid
    output: output_grid
    rule: "Yellow pixels are removed if they do not have a at least 3 yellow adjacent neighbor (up, down, left, or right)."

relationships:
  - type: element_of
    subject: pixel
    object: grid

  - type: adjacent_to
    subject: pixel
    object: pixel
    properties:
        cardinal_direction: bool # true of neighbor is directly to the up, down, left or right.
```


**Natural Language Program:**

1.  **Input:** A 17x9 grid (input\_grid) containing pixels of color 0 (white) and 4 (yellow).
2.  **Iterate:** Go through each pixel of the `input_grid`.
3.  **Conditional Check:** For each pixel:
    *   If the pixel is white (0), keep it white (0) in the `output_grid`.
    *    If a pixel is not yellow, go the the next pixel.
    *   If the pixel is yellow (4), count its adjacent yellow neighbors (up, down, left, and right - not diagonal).
    *   If a yellow pixel has three, or more, yellow neighbors, keep it as yellow (4) in the output\_grid.
    *    If the yellow pixel has fewer than three yellow neighbor, change it to white (0) in the `output_grid`.
4.  **Output:** The modified 17x9 grid (`output_grid`).

In essence, the transformation filters out yellow pixels that are relatively isolated, keeping only those yellow pixels which have many yellow adjacent neighbors.

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
