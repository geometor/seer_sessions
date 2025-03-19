# aba27056 • 002 • example_3 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 6 6 0 6 6 0
0 6 0 0 0 6 0
0 6 6 6 6 6 0
```

<PIL.Image.Image image mode=RGB size=448x448 at 0x7F4C2318BCD0>

**output:**
```
0 0 0 4 0 0 0
4 0 0 4 0 0 4
0 4 0 4 0 4 0
0 0 4 4 4 0 0
0 6 6 4 6 6 0
0 6 4 4 4 6 0
0 6 6 6 6 6 0
```

<PIL.Image.Image image mode=RGB size=448x448 at 0x7F4C1B6BFF50>

## train_2

**input:**
```
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 7 7 7 7 7
0 0 0 0 7 0 0 0 7
0 0 0 0 0 0 0 0 7
0 0 0 0 0 0 0 0 7
0 0 0 0 0 0 0 0 7
0 0 0 0 7 0 0 0 7
0 0 0 0 7 7 7 7 7
```

<PIL.Image.Image image mode=RGB size=576x576 at 0x7F4C1B74D150>

**output:**
```
4 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0
0 0 4 0 7 7 7 7 7
0 0 0 4 7 4 4 4 7
4 4 4 4 4 4 4 4 7
4 4 4 4 4 4 4 4 7
4 4 4 4 4 4 4 4 7
0 0 0 4 7 4 4 4 7
0 0 4 0 7 7 7 7 7
```

<PIL.Image.Image image mode=RGB size=576x576 at 0x7F4C1B6BFB50>

## train_3

**input:**
```
3 3 3 3 3 3
3 0 0 0 0 3
3 0 0 0 0 3
3 3 0 0 3 3
0 0 0 0 0 0
0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=384x384 at 0x7F4C1B6BFDD0>

**output:**
```
3 3 3 3 3 3
3 4 4 4 4 3
3 4 4 4 4 3
3 3 4 4 3 3
0 4 4 4 4 0
4 0 4 4 0 4
```

<PIL.Image.Image image mode=RGB size=384x384 at 0x7F4C1A588050>
<PIL.Image.Image image mode=RGB size=1536x1232 at 0x7F4C1B7DC4D0>Okay, here's my analysis of the provided input-output pairs, focusing on perception, object identification, and the transformation rule.

**Perception of Elements:**

The tasks involve 2D grids of single-digit integers (0-9), representing colors. The core task seems to be related to identifying connected regions of non-zero colors and applying a transformation, potentially involving the insertion of a new color (4 - yellow) based on some criteria related to shape of those regions and background pixels..

**YAML Fact Documentation:**


```yaml
facts:
  - type: grid
    description: Input and output are 2D grids of integers.
    elements: Integers 0-9, representing colors.
  - type: object
    description: Non-zero colored regions form connected components.
    properties:
      - color: Represented by the integer value.
      - shape: The outline or boundary of the connected component.
      - size: Number of pixels in the component.
  - type: background
    description: pixels with color 0.
  - type: transformation_color
    description: color with value of 4 (yellow).
  - type: transformation
    description: A new shape (object) consisting of the transformation color is "drawn", with a relationship to the existing non-zero colored objects.

```


**Natural Language Program:**

1.  **Identify Objects:** Locate all connected regions (objects) of non-zero pixels in the input grid.
2.  **Identify Background:** Locate all regions (objects) of pixels with zero value
3. **Outer Border Insertion**: For every background (color 0) pixel that is directly adjacent (not diagonal) to any non-zero pixel, change color to 4 (yellow). If non-zero pixel is already adjacent to existing 4 pixel, do not perform change
4. **Inner Border Insertion**: For every non-zero pixel that is directly adjacent (not diagonal) to any background (color 0) pixel, change color to 4 (yellow).
5.  **Output:** Return the modified grid.

Essentially, the transformation creates a "border" of color 4 around all original objects, both on their outside edge, and internal to any holes.

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
