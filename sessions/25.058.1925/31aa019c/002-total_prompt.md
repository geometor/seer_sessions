# 31aa019c • 002 • example_3 • investigate_coder

---

## train_1

**input:**
```
0 0 0 1 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 2 0 0 0 1
0 0 1 0 0 0 0 0 0 5
0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0
0 5 1 0 1 0 0 0 0 0
0 8 1 0 0 0 1 0 3 0
0 0 0 0 0 0 0 3 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x78E5F21D3E50>

**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
2 2 2 0 0 0 0 0 0 0
2 4 2 0 0 0 0 0 0 0
2 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x78E5F21D3D50>

## train_2

**input:**
```
2 7 7 1 0 3 0 0 0 3
0 0 0 9 0 0 0 0 3 7
0 0 0 1 0 0 0 6 0 9
0 0 0 0 0 0 0 1 0 0
9 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 3 0
0 5 0 7 3 0 0 0 1 0
4 4 0 0 0 1 0 0 0 5
0 0 0 0 0 0 0 5 3 0
0 0 0 0 4 5 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x78E5F214ABD0>

**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 2 2 0
0 0 0 0 0 0 2 6 2 0
0 0 0 0 0 0 2 2 2 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x78E5F264F650>

## train_3

**input:**
```
6 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 2 8
0 7 0 0 2 0 5 0 2 0
0 9 0 1 0 0 0 0 0 0
0 9 0 0 0 0 0 0 0 1
0 0 0 0 0 6 0 0 0 0
0 1 0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0
0 0 5 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x78E5F21D38D0>

**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 0 0
0 0 0 0 0 2 3 2 0 0
0 0 0 0 0 2 2 2 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x78E5F20EFF50>
<PIL.Image.Image image mode=RGB size=2000x1330 at 0x78E5F267AFD0>Okay, let's analyze this ARC task.

**Perception of Elements:**

The task involves transforming a grid of colored pixels (represented by numbers 0-9) into another grid of the same dimensions. The most obvious change is that many of the colored pixels in the input disappear in the output. A specific region, however, seems to be highlighted and potentially altered in color. It appears there's some concept of a "background" (represented by 0, or white) and "foreground" objects. The outputs all share a red object composed by a 3x3 block in the same place, replacing an object of any color on the input.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    properties:
      - dimensions: 10x10
      - cells: pixels (integers 0-9, representing colors)
  - type: background
    properties:
      - color: 0 (white)
  - type: foreground_objects
    properties:
      - colors: non-zero integers (1-9)
      - shapes: varied (appear to be irregular collections of adjacent pixels)
  - type: highlighted_region
    properties:
      - shape: 3x3 square
      - color_input: any non-zero
      - color_output: 2(red) and possibly the original center
    location: varies, the non-zero color object closest to the bottom right corner

actions:
  - select_region: Identify a region to highlight. The criteria is the lowest, then furthest right non-zero object.
  - replace: other colors with 2(red), except center, which is preserved
  - clear: Set all pixels outside the selected highlighted_region to 0 (white).

relationships:
  - spatial: Pixels are adjacent (up, down, left, right, diagonal).
  - containment: The highlighted_region is a subset of the grid.
  - transformation: input grid transforms into output grid

```


**Natural Language Program:**

1.  **Identify the Target Object:** Find the non-zero colored object in the input grid that is closest to the bottom-right corner. Prioritize the lowest row first, and on the same row, choose rightmost item.

2.  **Define Highlighted Region:** Once the target object has been found, create a 3x3 square region, centered on the single pixel of the target object which is not zero, furthest to the bottom and right.

3. **Replace with red:** Every value of the 3x3 square will be replaced by the value `2`

4.  **Clear Background:** Set all pixels *outside* the 3x3 highlighted square to 0 (white).

5. **Preserve the center:** If the target object's center was an existing color, preserve that color.

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
