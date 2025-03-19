# 95990924 • 002 • example_3 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 5 0 0 0 0
0 0 0 0 5 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7F4C1A58B950>

**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 1 0 0 2 0 0 0
0 0 0 0 5 5 0 0 0 0
0 0 0 0 5 5 0 0 0 0
0 0 0 3 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7F4C1A5889D0>

## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 5 5 0 0 0 0 0 0
0 0 5 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 5 0 0
0 0 0 0 0 0 5 5 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7F4C1A58B5D0>

**output:**
```
0 0 0 0 0 0 0 0 0 0
0 1 0 0 2 0 0 0 0 0
0 0 5 5 0 0 0 0 0 0
0 0 5 5 0 0 0 0 0 0
0 3 0 0 4 0 0 0 0 0
0 0 0 0 0 1 0 0 2 0
0 0 0 0 0 0 5 5 0 0
0 0 0 0 0 0 5 5 0 0
0 0 0 0 0 3 0 0 4 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7F4C1A5893D0>

## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 5 5 0 0 0 0 0 0 0 0 0 0
0 0 0 5 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 5 5 0 0 0 0 0
0 0 0 0 0 0 0 0 5 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 5 0 0 0 0 0 0 0 0 0
0 0 0 0 5 5 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 5 5 0 0 0 0
0 0 0 0 0 0 0 0 0 5 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=960x960 at 0x7F4C1A58BDD0>

**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 2 0 0 0 0 0 0 0 0 0
0 0 0 5 5 0 0 0 0 0 0 0 0 0 0
0 0 0 5 5 0 0 1 0 0 2 0 0 0 0
0 0 3 0 0 4 0 0 5 5 0 0 0 0 0
0 0 0 0 0 0 0 0 5 5 0 0 0 0 0
0 0 0 0 0 0 0 3 0 0 4 0 0 0 0
0 0 0 1 0 0 2 0 0 0 0 0 0 0 0
0 0 0 0 5 5 0 0 0 0 0 0 0 0 0
0 0 0 0 5 5 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 4 0 1 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 5 5 0 0 0 0
0 0 0 0 0 0 0 0 0 5 5 0 0 0 0
0 0 0 0 0 0 0 0 3 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=960x960 at 0x7F4C1A58B150>
<PIL.Image.Image image mode=RGB size=2368x2000 at 0x7F4C1A58ABD0>Okay, let's analyze this ARC-AGI task.

**Perception of the Elements:**

The task involves 2D grids containing colored pixels. The primary object appears to be a 2x2 square of gray (color 5) pixels. The transformation adds colored pixels (blue, red, green, yellow - colors 1, 2, 3, and 4) around these gray squares. The positions of the added colors seem consistent relative to the gray squares.

**YAML Block (Facts):**


```yaml
objects:
  - name: gray_square
    type: shape
    color: gray (5)
    size: 2x2
    properties:
      - static: false # It seems to exist in both input and output but can have adjacent colored pixels.
  - name: blue_pixel
    type: shape
    color: blue (1)
    size: 1x1
  - name: red_pixel
    type: shape
    color: red (2)
    size: 1x1
  - name: green_pixel
    type: shape
    color: green (3)
    size: 1x1
  - name: yellow_pixel
    type: shape
    color: yellow (4)
    size: 1x1

actions:
  - name: add_colored_pixels
    description: Places colored pixels (1, 2, 3, 4) adjacent to the gray squares.

relationships:
  - description: Colored pixels are placed in a specific pattern around each gray square.
  - blue: Top-Left of the top-left pixel of the gray square
  - red: Top-Right of the top-right pixel of the gray square
  - green: Bottom-Left of the bottom-left pixel of the gray square
  - yellow: Bottom-Right of the bottom-right pixel of the gray square
```


**Natural Language Program:**

1.  **Identify** all 2x2 gray squares (color 5) within the input grid.
2.  **For each** identified gray square:
    *   Place a blue pixel (color 1) one position up and one position to the left from the gray square's top-left corner pixel.
    *   Place a red pixel (color 2) one position up and one position to the right from the gray square's top-right corner pixel.
    *   Place a green pixel (color 3) one position down and one position to the left from the gray square's bottom-left corner pixel.
    *   Place a yellow pixel (color 4) one position down and one position to the right from the gray square's bottom-right corner pixel.
3.  **Maintain** all existing pixels (including the gray square) from the input grid in their original positions. The only changes on the grid are addition of new pixels.

Essentially, the transformation "decorates" each 2x2 gray square with four colored pixels in a consistent pattern. The background (0 - white) is unchanged.

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
