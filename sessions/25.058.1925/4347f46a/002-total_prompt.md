# 4347f46a • 002 • example_3 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 0 3 3 3 3 3 3 3 0 0 0
0 0 0 0 0 0 3 3 3 3 3 3 3 0 0 0
0 0 0 0 0 0 3 3 3 3 3 3 3 0 0 0
0 0 0 0 0 0 3 3 3 3 3 3 3 0 0 0
0 0 0 0 0 0 3 3 3 3 3 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 6 6 6 6 6 6 0 0 0 7 7 7 0
0 0 6 6 6 6 6 6 6 0 0 0 7 7 7 0
0 0 6 6 6 6 6 6 6 0 0 0 7 7 7 0
0 0 6 6 6 6 6 6 6 0 0 0 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=1024x1152 at 0x78E5F264F850>

**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 8 0 0 8 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 0 3 3 3 3 3 3 3 0 0 0
0 0 0 0 0 0 3 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 3 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 3 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 3 3 3 3 3 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 6 6 6 6 6 6 0 0 0 7 7 7 0
0 0 6 0 0 0 0 0 6 0 0 0 7 0 7 0
0 0 6 0 0 0 0 0 6 0 0 0 7 0 7 0
0 0 6 6 6 6 6 6 6 0 0 0 7 0 7 0
0 0 0 0 0 0 0 0 0 0 0 0 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=1024x1152 at 0x78E5F264D150>

## train_2

**input:**
```
0 0 0 0 0 0 0
0 2 2 2 2 2 0
0 2 2 2 2 2 0
0 2 2 2 2 2 0
0 2 2 2 2 2 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=448x512 at 0x78E5F264F9D0>

**output:**
```
0 0 0 0 0 0 0
0 2 2 2 2 2 0
0 2 0 0 0 2 0
0 2 0 0 0 2 0
0 2 2 2 2 2 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=448x512 at 0x78E5F214A6D0>

## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 5 5 5 5 0 0
0 0 5 5 5 5 5 5 5 5 0 0
0 0 5 5 5 5 5 5 5 5 0 0
0 0 5 5 5 5 5 5 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 4 4 0 0 0 0 0
0 4 4 4 4 4 4 0 0 0 0 0
0 4 4 4 4 4 4 0 0 0 0 0
0 4 4 4 4 4 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=768x704 at 0x78E5F214ABD0>

**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 5 5 5 5 0 0
0 0 5 0 0 0 0 0 0 5 0 0
0 0 5 0 0 0 0 0 0 5 0 0
0 0 5 5 5 5 5 5 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 4 4 0 0 0 0 0
0 4 0 0 0 0 4 0 0 0 0 0
0 4 0 0 0 0 4 0 0 0 0 0
0 4 4 4 4 4 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=768x704 at 0x78E5F214A650>
<PIL.Image.Image image mode=RGB size=2320x2354 at 0x78E5F9F6F550>Okay, here's a breakdown of my observations and a proposed natural language program for the transformation:

**Perception of Elements:**

*   **Objects:** The primary objects are rectangular blocks of uniform color.
*   **Background:** The background is consistently white (color 0).
*   **Object Properties:** Objects are defined by their color and rectangular shape. They have a solid fill in the input.
*   **Transformation:** The transformation involves "hollowing out" the filled rectangles, leaving only their outer border. The border thickness appears to be one pixel.
*    The color of the border is maintained.

**YAML Fact Documentation:**


```yaml
objects:
  - type: rectangle
    properties:
      color: varied (non-white)
      fill: solid
    transformation:
      action: hollow
      result: border_only
      border_thickness: 1
      color: maintained

background:
    color: white

```


**Natural Language Program:**

1.  **Identify** all contiguous rectangular regions of non-white pixels in the input grid. These are the objects.
2.  For each identified rectangular object:
    *   **Retain** the pixels forming the outer border of the rectangle. The border is one pixel thick.
    *    **Change** the color all the pixels that composed the solid inner to match the background.
    *   **Keep** the original color of border pixels.
3.  All other pixels (the background) remain unchanged.

Essentially the program says - iterate the objects, replace their insides with
the background color.

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
