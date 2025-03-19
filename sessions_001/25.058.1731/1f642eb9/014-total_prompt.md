# 1f642eb9 • 014 • example_3 • investigate_coder

---

## train_3

**input:**
```
0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 0 0 0 6
3 0 0 8 8 8 0 0 0 0
0 0 0 8 8 8 0 0 0 0
2 0 0 8 8 8 0 0 0 0
0 0 0 8 8 8 0 0 0 2
0 0 0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7C36039E6450>

**output:**
```
0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 8 6 0 0 0 6
3 0 0 3 8 8 0 0 0 0
0 0 0 8 8 8 0 0 0 0
2 0 0 2 8 8 0 0 0 0
0 0 0 7 8 2 0 0 0 2
0 0 0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7C360398B950>
Okay, let's analyze this ARC-AGI task example.

**Perception of Elements:**

The task involves 2D grids (10x10) of colored pixels, represented by integers 0-9. The input grid appears to have a central "blob" of azure (8) pixels, with single, isolated pixels of other colors surrounding it. The output grid seems to be a modified version of the input, with some of the azure pixels changed to match the colors of the surrounding pixels. Specifically, it looks like the colors of the surrounding pixels have "replaced" some of the azure pixels adjacent to them. There is a mirroring of colors at the edges of shape '8'.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    dimensions: 10x10
    elements: pixels
    description: 2D array of colored pixels

  - type: blob
    color: azure (8)
    shape: irregular
    location: central
    description: A contiguous region of azure pixels

  - type: isolated_pixels
    colors: [yellow (4), magenta (6), green (3), red (2), orange (7)]
    locations: varied, surrounding the blob
    description: Single pixels of various colors, not connected to each other
```


**Natural Language Program:**

1.  **Identify the azure (8) blob:** Locate the contiguous region of azure pixels in the input grid.
2.  **Identify surrounding pixels:** Find all single pixels that have colors and are not connected to anything on at least two sides.
3. Identify adjacent 8 pixels. For the pixels identified find the closest adjacent 8's.
4.  **Propagate/Mirror Colors**: Working from left to right, top to bottom. If an isolated pixel has a value different than 8, it will mirror its value to the adjacent 8 on its right, and the isolated pixel above will mirror to the 8 pixel below. If an isolated pixel of color is adjacent to an '8' along the shape's diagonal corners, it is assigned the value of the isolated color pixel.

This program captures the core transformation: isolated pixels' colors influencing/replacing adjacent azure pixels within the central blob, with a sense of "propagation" or mirroring of those colors along the shapes border.

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
