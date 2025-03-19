# a1570a43 • 002 • example_4 • investigate_coder

---

## train_1

**input:**
```
3 0 2 0 0 0 3
0 2 2 0 0 0 0
2 2 2 2 2 0 0
0 2 0 0 0 0 0
0 2 2 0 0 0 0
0 0 0 0 0 0 0
3 0 0 0 0 0 3
```

<PIL.Image.Image image mode=RGB size=448x448 at 0x7A174C5B8250>

**output:**
```
3 0 0 0 0 0 3
0 0 0 2 0 0 0
0 0 2 2 0 0 0
0 2 2 2 2 2 0
0 0 2 0 0 0 0
0 0 2 2 0 0 0
3 0 0 0 0 0 3
```

<PIL.Image.Image image mode=RGB size=448x448 at 0x7A174C5B8FD0>

## train_2

**input:**
```
0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 3 0
0 0 2 2 2 0 0 0 0
2 2 2 0 0 0 0 0 0
2 0 2 0 0 0 0 0 0
2 2 2 2 0 0 0 0 0
0 0 0 2 0 0 0 0 0
0 3 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=576x576 at 0x7A174C5B8BD0>

**output:**
```
0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 3 0
0 0 0 0 2 2 2 0 0
0 0 2 2 2 0 0 0 0
0 0 2 0 2 0 0 0 0
0 0 2 2 2 2 0 0 0
0 0 0 0 0 2 0 0 0
0 3 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=576x576 at 0x7A174C5BB950>

## train_3

**input:**
```
0 0 0 2 2 0 0 0 0 0
0 3 2 2 2 2 0 3 0 0
0 0 0 0 2 2 2 0 0 0
0 0 0 0 2 0 0 0 0 0
0 0 0 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x576 at 0x7A174C5BB650>

**output:**
```
0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 3 0 0
0 0 0 2 2 0 0 0 0 0
0 0 2 2 2 2 0 0 0 0
0 0 0 0 2 2 2 0 0 0
0 0 0 0 2 0 0 0 0 0
0 0 0 2 2 0 0 0 0 0
0 3 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x576 at 0x7A174C5BA4D0>

## train_4

**input:**
```
3 0 0 0 0 0 3 0
0 0 0 2 0 0 0 0
0 2 2 2 0 0 0 0
0 2 0 0 0 0 0 0
2 2 2 2 2 0 0 0
0 2 0 0 0 0 0 0
3 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=512x576 at 0x7A174C5B9250>

**output:**
```
3 0 0 0 0 0 3 0
0 0 0 0 2 0 0 0
0 0 2 2 2 0 0 0
0 0 2 0 0 0 0 0
0 2 2 2 2 2 0 0
0 0 2 0 0 0 0 0
3 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=512x576 at 0x7A174C5BB350>
<PIL.Image.Image image mode=RGB size=2336x1232 at 0x7A174C5BB4D0>Okay, let's analyze the provided input-output pairs to understand the transformation.

**Perception of Elements:**

The task involves 2D grids with integer values representing colors. The primary colors observed are red (2), green (3), and white/background (0). The core transformation seems to involve manipulating the red (2) pixels while preserving the green (3) and white (0) pixels. The shape formed by the red pixels appears to be an "arrow" or cross-like figure. The transformation seems to involve rotating this red shape. The green pixels act like fixed "anchors" or boundaries and do not move.

**YAML Block (Facts):**


```yaml
objects:
  - type: pixel
    properties:
      color:
        - 0  # Background/White
        - 2  # Red
        - 3  # Green
      position: [row, column]
  - type: shape
    properties:
      color: 2 #red
      form: arrow/cross
      pixels: list of pixel objects

actions:
  - name: rotate
    object: shape
    parameters:
      direction: clockwise
      angle: 90 degrees

relationships:
  - type: spatial
    description: Green pixels remain fixed.
    objects: [pixel, pixel]
  - type: transformation
    description: Red shape rotates around a central point
    objects: [shape, shape]
```


**Natural Language Program:**

1.  **Identify Objects:** Locate all pixels with the value 2 (red) and group them as a single shape. Identify pixels with the value 3 (green) and consider their locations as fixed.

2.  **Rotate Shape:** Rotate the red shape 90 degrees clockwise. The "center" of rotation appears to be implicitly defined within the red shape itself and shifts appropriately with each rotation.

3. **Preserve Other Pixels.** Keep all pixels with the value 0 (white/background) and 3 (green) in their original positions. The transformation only affects red objects.

4.  **Output:** Generate the new grid with the rotated red shape and the unchanged green and white pixels.

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
