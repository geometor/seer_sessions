# 97999447 • 002 • example_3 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=512x640 at 0x7F4C2318BCD0>

**output:**
```
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 2 5 2 5 2 5
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 6 5 6 5 6
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=512x640 at 0x7F4C1B701850>

## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=768x640 at 0x7F4C1B703C50>

**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 5 2 5 2 5 2 5 2 5
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 3 5 3 5 3 5 3 5 3 5 3
0 0 0 0 0 0 6 5 6 5 6 5
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=768x640 at 0x7F4C1A58A750>

## train_3

**input:**
```
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=512x448 at 0x7F4C2318BF50>

**output:**
```
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 8 5 8 5 8
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=512x448 at 0x7F4C1A5899D0>
<PIL.Image.Image image mode=RGB size=1920x1360 at 0x7F4C1A589B50>Okay, let's analyze the provided input-output examples to discern the transformation rule.

**Perception of Elements:**

The task involves 2D grids where each cell contains a single digit representing a color. The primary elements are:

*   **Input Grid:** The initial state of the grid.
*   **Output Grid:** The transformed state of the grid.
*   **Pixels:** Individual cells within the grids, represented by a digit (0-9) corresponding to a color.
*   **Objects:** Contiguous blocks of pixels of the same non-zero color.
*    **Background**:  Pixels of color 0 (white)

**YAML Block (Facts):**


```yaml
objects:
  - description: Non-zero colored pixels in the input grid.
    properties:
      color: The digit (1-9) representing the color.
      location: Row and column indices of the pixel.

actions:
  - name: Extend
    description:  Adds gray (5) pixels to the right of existing non-zero color pixels in the same row.

relationships:
   - type: spatial
     description: The extension occurs horizontally, to the right of the original objects.
   - type: color_change
     description: All added pixels are gray color (value 5)

```


**Natural Language Program:**

1.  **Identify Objects:** Locate all non-zero pixels in the input grid. Each non-zero pixel is an individual object.
2.  **Extend Horizontally:** For each identified object, add a gray (5) pixel to its immediate right within the same row. Repeat adding a grey pixel until the end of row.
3.  **Background:** The background (0 - white) pixels will remain unchanged.

In essence, the transformation takes each colored pixel in the input and extends it with grey color to the edge of the grid, in the same row.

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
