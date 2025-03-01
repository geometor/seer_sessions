# 7447852a • 002 • example_3 • investigate_coder

---

## train_1

**input:**
```
2 0 0 0 2 0 0 0 2 0
0 2 0 2 0 2 0 2 0 2
0 0 2 0 0 0 2 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x192 at 0x70A2ECD7AAD0>

**output:**
```
2 0 0 0 2 4 4 4 2 0
4 2 0 2 0 2 4 2 0 2
4 4 2 0 0 0 2 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x192 at 0x70A2ECD7A4D0>

## train_2

**input:**
```
2 0 0 0 2 0 0 0 2 0 0 0 2 0 0
0 2 0 2 0 2 0 2 0 2 0 2 0 2 0
0 0 2 0 0 0 2 0 0 0 2 0 0 0 2
```

<PIL.Image.Image image mode=RGB size=960x192 at 0x70A2ECD79850>

**output:**
```
2 0 0 0 2 4 4 4 2 0 0 0 2 0 0
4 2 0 2 0 2 4 2 0 2 0 2 4 2 0
4 4 2 0 0 0 2 0 0 0 2 4 4 4 2
```

<PIL.Image.Image image mode=RGB size=960x192 at 0x70A2ECD7ACD0>

## train_3

**input:**
```
2 0 0 0 2 0 0 0 2 0 0 0 2 0 0 0 2 0
0 2 0 2 0 2 0 2 0 2 0 2 0 2 0 2 0 2
0 0 2 0 0 0 2 0 0 0 2 0 0 0 2 0 0 0
```

<PIL.Image.Image image mode=RGB size=1152x192 at 0x70A2ECD7A3D0>

**output:**
```
2 0 0 0 2 4 4 4 2 0 0 0 2 0 0 0 2 4
4 2 0 2 0 2 4 2 0 2 0 2 4 2 0 2 0 2
4 4 2 0 0 0 2 0 0 0 2 4 4 4 2 0 0 0
```

<PIL.Image.Image image mode=RGB size=1152x192 at 0x70A2ECD7ADD0>
<PIL.Image.Image image mode=RGB size=2880x464 at 0x70A2ECD7AFD0>Okay, let's analyze this ARC task.

**Perception of Elements:**

*   **Input Grids:** The input grids consist of a repeating pattern of red (2) and white (0) pixels. The red pixels form a diagonal checkerboard-like pattern. The input grids are all 3 rows tall, and the width increases.
*   **Output Grids:** The output grids maintain the same dimensions as the input grids. They introduce yellow (4) pixels. The yellow pixels appear to "fill in" the white spaces between the red diagonals, but only in specific locations. Specifically, they appear to replace the white pixels that are horizontally adjacent to a red one in the original input *after* the first sequence of red pixels in each row.
* **Transformation:** The core transformation appears to be a conditional replacement of white pixels with yellow pixels based on their proximity to red pixels. It is crucial to note that there is a directional component: the yellow fills appear from left to right, stopping to be filled when there is another red cell.

**YAML Block (Facts):**


```yaml
objects:
  - name: grid
    properties:
      - type: 2D array
      - values: [0, 2, 4]
      - colors: {0: white, 2: red, 4: yellow}
  - name: pixel
    properties:
      - type: integer
      - value: element of grid

actions:
  - name: replace
    parameters:
      - source_color: 0
      - target_color: 4
      - condition: horizontally adjacent to 2 and after the first sequence of 2s.

relationships:
  - type: spatial
    description: pixels are arranged in a 2D grid.
  - type: adjacency
    description: horizontal adjacency is key to the transformation.
  - type: sequence
    description: Red pixels will be encountered.
```


**Natural Language Program:**

1.  **Iterate** through each row of the input grid.
2.  **Identify** sequences of red(2) pixels, if a sequence contains only 1 red pixel, this also constitutes a sequence.
3.  Within each row, **Locate** the white(0) pixels to the right of a sequence of red(2) pixels.
4.  **Replace** those white(0) pixels with yellow(4) pixels, until hitting the next red(2) pixel or end of row.
5.  **Repeat** for all rows, and preserve the red(2) pixels.

In simpler terms: "Fill the white spaces between the red diagonals with yellow, starting after the leftmost red pixel on each line." Or even more simply, "Change to yellow the white cells after sequences of reds within each row".

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
