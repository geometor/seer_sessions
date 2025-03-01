# 1e0a9b12 • 002 • example_3 • investigate_coder

---

## train_1

**input:**
```
0 4 0 9
0 0 0 0
0 4 6 0
1 0 0 0
```

<PIL.Image.Image image mode=RGB size=256x256 at 0x7C36044BF5D0>

**output:**
```
0 0 0 0
0 0 0 0
0 4 0 0
1 4 6 9
```

<PIL.Image.Image image mode=RGB size=256x256 at 0x7C36044BF1D0>

## train_2

**input:**
```
0 0 0 0 0 9
0 0 0 8 0 0
0 0 0 0 0 0
4 0 0 0 0 0
4 0 7 8 0 0
4 0 7 0 0 0
```

<PIL.Image.Image image mode=RGB size=384x384 at 0x7C36044BF650>

**output:**
```
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
4 0 0 0 0 0
4 0 7 8 0 0
4 0 7 8 0 9
```

<PIL.Image.Image image mode=RGB size=384x384 at 0x7C360455DC50>

## train_3

**input:**
```
0 0 0 1 0
0 3 0 0 0
0 3 0 1 2
6 0 0 0 0
0 3 0 0 0
```

<PIL.Image.Image image mode=RGB size=320x320 at 0x7C36044BFAD0>

**output:**
```
0 0 0 0 0
0 0 0 0 0
0 3 0 0 0
0 3 0 1 0
6 3 0 1 2
```

<PIL.Image.Image image mode=RGB size=320x320 at 0x7C36039E61D0>
<PIL.Image.Image image mode=RGB size=1040x818 at 0x7C36044765D0>Okay, let's analyze this ARC task.

**Perception of Elements:**

The task involves 2D grids of colored pixels. The primary element seems to be the movement and consolidation of non-zero (colored) pixels. Zeros (white pixels) appear to act as empty space. The transformation seems to involve shifting these colored pixels based on certain rules, possibly prioritizing specific locations or directions. The shape and dimensions of input and output are different.

**YAML Block (Facts):**


```yaml
objects:
  - name: grid
    type: 2D array
    properties:
      - height: variable
      - width: variable
      - cells: pixels (integers 0-9 representing colors)

  - name: pixel
    type: cell
    properties:
      - color: integer (0-9)
      - row: integer
      - column: integer
      - is_zero: boolean (True if color is 0, False otherwise)

actions:
  - name: move
    description: Changes the row and/or column of a pixel.
  - name: consolidate
    description: combine color pixels.
  - name: remove_rows
    description: removes rows with values.
  - name: replace
    description: some values are replaced

relationships:
  - type: adjacency
    description: Pixels can be adjacent horizontally, vertically, or diagonally.
  - type: containment
    description: grid contains many pixel.
  - type: position
    description: relative order and location of colors after a move.
```


**Natural Language Program:**

1.  **Identify Non-Zero Pixels:** Locate all pixels in the input grid that have a non-zero color value.

2.  **Consolidate to Bottom:** Move all non-zero pixels to the bottom rows of the grid, maintaining their relative horizontal order. Empty rows created by this are removed.

3.   **Maintain Order:** Ensure that within their final respective rows, the relative horizontal order (left-to-right) of the non-zero pixels is preserved from the input to the output.

4. **Remove empty rows:** rows that are all zero at the top are removed.

In simple terms, imagine all non-zero colored pixels "falling" to the bottom, stacking on top of each other, while keeping their original left-to-right arrangement, and removing all the blank rows.

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
