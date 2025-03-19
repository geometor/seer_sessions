# af902bf9 • 010 • example_2 • investigate_coder

---

## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7F4C1B74C5D0>

**output:**
```
0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 4 0 0 0
0 0 2 2 2 2 0 0 0 0
0 0 2 2 2 2 0 0 0 0
0 0 2 2 2 2 0 0 0 0
0 0 2 2 2 2 0 0 0 0
0 4 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7F4C1A58B150>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves a grid of pixels, where each pixel has a color value (represented by numbers 0-9). The primary colors observed are white (0), yellow (4), and red (2).  The input grid seems to contain isolated yellow pixels, and the output grid introduces a red region in the center. The yellow pixels remain unchanged.

**YAML Block (Facts):**


```yaml
facts:
  - object: grid
    description: 2D array of pixels
    properties:
      - rows: 10
      - columns: 10
      - cell_values: [0, 2, 4]

  - object: yellow_pixels
    description: Individual pixels with the value 4.
    properties:
      - color: yellow
      - initial_positions: [(1,1), (1,6), (6,1), (6,6)] #row, col
    behavior:
      - remain_unchanged: true

  - object: red_rectangle
    description: A rectangular block of pixels with value 2.
    properties:
      - color: red
      - top_left_corner: (2,2) #row, col
      - bottom_right_corner: (5,5) #row, col
    behavior:
      - appears_in_output: true
```


**Natural Language Program:**

1.  **Identify Yellow Pixels:** Locate all pixels in the input grid with a value of 4 (yellow).
2.  **Preserve Yellow Pixels:** Copy the yellow pixels from their original locations in the input grid to the identical locations in the output grid.
3.  **Create Red Rectangle:** In the output grid, create a rectangular region of red (value 2) pixels. This rectangle has these bounding coordinates (row, col)
    - top-left: (2,2)
    - bottom-right: (5, 5)
4.  **Fill Remaining Pixels:** All other pixels in the output grid that are not yellow or part of the red rectangle should be set to white (value 0). In essence, leave those cells with their original value.

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
