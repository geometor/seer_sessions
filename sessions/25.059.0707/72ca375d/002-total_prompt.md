# 72ca375d • 002 • example_3 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0
0 0 2 2 2 0 0 7 7 0
0 0 0 0 0 0 7 0 7 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 6 6 6 6 0 0 0
0 0 0 0 6 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7A43F5F5F950>

**output:**
```
6 6 6 6
0 6 6 0
```

<PIL.Image.Image image mode=RGB size=256x128 at 0x7A43F5EEC4D0>

## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 4 4 0 0 0 0 0 0
0 0 4 4 0 0 8 8 8 0
0 0 0 0 0 0 8 0 8 8
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7A43F5F7EDD0>

**output:**
```
4 4
4 4
```

<PIL.Image.Image image mode=RGB size=128x128 at 0x7A43F5F7F4D0>

## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0
0 0 3 0 0 5 0 0 5 0
0 0 3 0 0 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 0 0 0 0
8 8 8 8 0 8 8 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7A43F5F5C950>

**output:**
```
5 0 0 5
5 5 5 5
```

<PIL.Image.Image image mode=RGB size=256x128 at 0x7A43F5E76750>
<PIL.Image.Image image mode=RGB size=2048x848 at 0x7A43FD927450>Okay, here's my analysis of the provided examples, outlining my perception of the elements, a YAML block documenting facts, and a natural language program describing the transformation.

**Perception of Elements:**

The task involves identifying and extracting specific colored rectangular objects from a larger grid. The input grids contain multiple rectangles of different colors and sizes, surrounded by a background of white (0). The output grids contain *only* one of these rectangles, maintaining its original shape and color, but potentially changing its position and size (by removing padding of 0).

**YAML Block (Facts):**


```yaml
objects:
  - type: rectangle
    properties:
      - color: variable (red, orange, yellow, azure, green, gray, magenta)
      - size: variable (width, height)
      - position: variable (row, column)
  - type: background
    properties:
      - color: white (0)
      - size: fixed (10x10)

actions:
  - type: selection
    description: One rectangle is selected from the input grid based on unknown criteria.
  - type: extraction
    description: The selected rectangle is extracted, potentially resized by removal of padding.

relationships:
  - input_grid: Contains multiple rectangles and a background.
  - output_grid: Contains only the selected rectangle, possibly resized.
  - selection_criteria:  Unknown, but consistent across examples (e.g. the bottom-most, largest, specific color, unique color in the example, etc.)
```


**Natural Language Program:**

1.  **Identify Rectangles:** Scan the input grid and identify all contiguous blocks of non-zero pixels. Each block represents a rectangle. Record the color, size (width and height), and top-left corner position of each rectangle.

2.  **Select Target Rectangle**:
    *   In the first example, select the magenta (6) rectangle.
    *   In the second example, select the yellow (4) rectangle.
    *   In the third example, select the gray (5) rectangle.
    The selection appears to be made choosing a unique color on the input grid.

3.  **Extract and Resize:** Extract the selected rectangle. Remove any rows and columns along the edges of the extracted rectangle that consist entirely of '0' (white/background) pixels.

4. **Output** The output is the smallest possible sub-grid containing the chosen rectangle.

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
