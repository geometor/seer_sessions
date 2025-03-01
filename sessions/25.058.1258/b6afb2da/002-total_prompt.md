# b6afb2da • 002 • example_2 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 0 0 0 0 0
0 5 5 5 5 0 0 0 0 0
0 5 5 5 5 0 0 0 0 0
0 5 5 5 5 0 5 5 5 5
0 0 0 0 0 0 5 5 5 5
0 0 0 0 0 0 5 5 5 5
0 0 0 0 0 0 5 5 5 5
0 0 0 0 0 0 5 5 5 5
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7E120E3C5C70>

**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 1 4 4 1 0 0 0 0 0
0 4 2 2 4 0 0 0 0 0
0 4 2 2 4 0 0 0 0 0
0 1 4 4 1 0 1 4 4 1
0 0 0 0 0 0 4 2 2 4
0 0 0 0 0 0 4 2 2 4
0 0 0 0 0 0 4 2 2 4
0 0 0 0 0 0 1 4 4 1
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7E120E52F570>

## train_2

**input:**
```
5 5 5 5 5 5 0 0 0 0
5 5 5 5 5 5 0 0 0 0
5 5 5 5 5 5 0 0 0 0
5 5 5 5 5 5 0 0 0 0
5 5 5 5 5 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 5 5 5 5 5
0 0 0 0 5 5 5 5 5 5
0 0 0 0 5 5 5 5 5 5
0 0 0 0 5 5 5 5 5 5
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7E120E52F890>

**output:**
```
1 4 4 4 4 1 0 0 0 0
4 2 2 2 2 4 0 0 0 0
4 2 2 2 2 4 0 0 0 0
4 2 2 2 2 4 0 0 0 0
1 4 4 4 4 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 4 4 4 4 1
0 0 0 0 4 2 2 2 2 4
0 0 0 0 4 2 2 2 2 4
0 0 0 0 1 4 4 4 4 1
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7E120E3C6170>
<PIL.Image.Image image mode=RGB size=1340x1330 at 0x7E120DD8A7B0>Okay, here's my analysis of the provided input-output examples, focusing on elements, a YAML fact block, and a natural language program describing the transformation.

**Perception of Elements:**

The task involves transforming grids containing filled rectangles of a single color (gray, color 5) into grids with outlined rectangles.  The outlining appears to replace the outer layer of the original filled rectangle. The fill color (interior) of the outlined rectangle is red (color 2), the four corners are blue (color 1) and the edges excluding the corners are yellow (color 4). The background is white (color 0).

**YAML Fact Block:**


```yaml
facts:
  - object: rectangle
    properties:
      - color: gray (5)
      - state: filled
      - shape: rectangular
    actions:
      - transformed: outlined
    relationships:
      - contains: background (0)
      - becomes: outlined_rectangle

  - object: outlined_rectangle
    properties:
      - fill_color: red (2)
      - corner_color: blue (1)
      - edge_color: yellow (4)
      - shape: rectangular
    relationships:
      - replaces: rectangle

  - object: background
    properties:
      - color: white (0)
    relationships:
        - surrounds: rectangle, outlined_rectangle
```


**Natural Language Program:**

1.  **Identify Rectangles:** Locate all contiguous rectangular regions of gray (color 5) pixels within the input grid. These are the "filled rectangles."

2.  **Outline and Fill:** For each identified filled rectangle:
    *   Replace the outermost layer of gray pixels to form an outline, according to this color code
    * The corner pixels of the outline are changed to blue (color 1).
    *   The non-corner edge pixels of the outline are changed to yellow (color 4).
    *   The remaining interior pixels (those not part of the outline) are changed to red (color 2).

3.  **Background:** All other pixels, which are not part of any identified rectangle, remain unchanged (white, color 0).

In simpler term: The program detects filled grey rectangles and replaces each solid grey rectangle with an outlined, three-colored version, consisting of blue corners, yellow edges, and a red interior.

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
