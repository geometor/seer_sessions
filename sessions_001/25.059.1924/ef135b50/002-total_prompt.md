# ef135b50 • 002 • example_3 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
2 2 2 0 0 0 0 0 0 0
2 2 2 0 0 0 0 2 2 0
2 2 2 0 0 0 0 2 2 0
0 0 0 0 0 0 0 2 2 0
0 0 0 2 2 0 0 2 2 0
0 0 0 2 2 0 0 2 2 0
0 0 0 2 2 0 0 0 0 0
0 0 0 2 2 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x716635BEBED0>

**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
2 2 2 0 0 0 0 0 0 0
2 2 2 9 9 9 9 2 2 0
2 2 2 9 9 9 9 2 2 0
0 0 0 0 0 0 0 2 2 0
0 0 0 2 2 9 9 2 2 0
0 0 0 2 2 9 9 2 2 0
0 0 0 2 2 0 0 0 0 0
0 0 0 2 2 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x716635BE9350>

## train_2

**input:**
```
2 2 0 0 0 0 0 0 0 0
2 2 0 0 0 0 0 0 0 0
2 2 0 0 0 0 0 2 2 2
2 2 0 0 0 0 0 2 2 2
0 0 0 0 0 0 0 2 2 2
0 0 0 2 2 0 0 2 2 2
0 0 0 2 2 0 0 0 0 0
0 0 0 2 2 0 0 0 0 0
0 0 0 2 2 0 2 2 2 2
0 0 0 0 0 0 2 2 2 2
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x716635BE9850>

**output:**
```
2 2 0 0 0 0 0 0 0 0
2 2 0 0 0 0 0 0 0 0
2 2 9 9 9 9 9 2 2 2
2 2 9 9 9 9 9 2 2 2
0 0 0 0 0 0 0 2 2 2
0 0 0 2 2 9 9 2 2 2
0 0 0 2 2 0 0 0 0 0
0 0 0 2 2 0 0 0 0 0
0 0 0 2 2 9 2 2 2 2
0 0 0 0 0 0 2 2 2 2
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x71663D5B21D0>

## train_3

**input:**
```
0 0 0 0 0 0 2 2 2 2
2 2 2 2 0 0 2 2 2 2
2 2 2 2 0 0 0 0 0 0
2 2 2 2 0 2 2 2 0 0
0 0 0 0 0 2 2 2 0 0
0 0 0 0 0 2 2 2 0 0
0 0 0 0 0 2 2 2 0 2
2 2 2 2 0 2 2 2 0 2
2 2 2 2 0 2 2 2 0 2
2 2 2 2 0 0 0 0 0 2
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x71663D5B3150>

**output:**
```
0 0 0 0 0 0 2 2 2 2
2 2 2 2 9 9 2 2 2 2
2 2 2 2 0 0 0 0 0 0
2 2 2 2 9 2 2 2 0 0
0 0 0 0 0 2 2 2 0 0
0 0 0 0 0 2 2 2 0 0
0 0 0 0 0 2 2 2 9 2
2 2 2 2 9 2 2 2 9 2
2 2 2 2 9 2 2 2 9 2
2 2 2 2 0 0 0 0 0 2
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x71663D5B23D0>
<PIL.Image.Image image mode=RGB size=2048x1360 at 0x71663D5B3B50>Okay, let's analyze the provided input-output examples to understand the transformation rule.

**Perception of Elements:**

The primary elements are grids containing pixels of different colors. The colors used are consistently white (0), red (2), and maroon (9). The transformation seems to involve selectively replacing some red pixels with maroon pixels. The positions of the replacements seem related to the shapes formed by the red pixels. Specifically, it appears to be filling areas within enclosed red regions.

**YAML Fact Documentation:**


```yaml
objects:
  - name: grid
    type: 2D array
    description: Contains pixels of different colors.
  - name: pixel
    type: cell
    properties:
      color:
        type: integer
        values: [0, 2, 9]
        mapping:
          0: white
          2: red
          9: maroon

actions:
  - name: fill_enclosed_area
    description: Replaces red pixels with maroon pixels within enclosed regions formed by red pixels.
    parameters:
        - object

relationships:
  - type: enclosure
    description: Red pixels form boundaries that enclose other red pixels.
    subject: red pixel
    object: red pixel

```


**Natural Language Program:**

1.  **Identify Red Objects:** Locate all contiguous regions of red (value 2) pixels in the input grid.
2.  **Identify White Spaces:** Locate any white pixels in between the red objects.
3.  **Fill Internal Regions:** For each red object identified, if an area of internal 0 (White) pixels is completely enclosed by red pixels, then keep them white. If an internal area is filled with red (2) pixels and there is no 0 (white) pixel in it, then, change color to 9 (maroon).
4.  Copy all other pixels, white and red, to output.

In simple words. All the red pixels enclosed in red boundaries become maroon.


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
