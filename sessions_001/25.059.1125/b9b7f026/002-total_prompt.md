# b9b7f026 • 002 • example_3 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 6 6 6 0 0 0 0 3 3 3 0 0
0 6 0 6 0 0 0 0 3 3 3 0 0
0 6 0 6 0 1 1 0 3 3 3 0 0
0 6 6 6 0 1 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 7 7 7 0
0 0 0 0 0 0 0 0 0 7 7 7 0
0 0 0 2 2 2 2 2 0 7 7 7 0
0 0 0 2 2 2 2 2 0 0 0 0 0
0 0 0 2 2 2 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
4 4 4 0 0 0 0 0 8 8 8 8 0
4 4 4 0 0 0 0 0 8 8 8 8 0
0 0 0 0 0 0 0 0 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=832x960 at 0x7F4C1B74D050>

**output:**
```
6
```

<PIL.Image.Image image mode=RGB size=64x64 at 0x7F4C1B67E150>

## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 7 7 7 7
0 0 0 0 0 0 0 0 0 0 0 0 0 7 7 7 7
8 8 8 8 8 0 0 0 0 0 0 0 0 7 7 7 7
8 8 8 8 8 0 0 5 5 5 5 0 0 7 7 7 7
8 8 8 8 8 0 0 5 5 5 5 0 0 7 7 7 7
0 0 0 0 0 0 0 5 5 5 5 0 0 7 7 7 7
0 0 0 2 2 2 0 5 0 0 5 0 0 0 0 0 0
0 0 0 2 2 2 0 5 0 0 5 0 0 0 0 0 0
0 0 0 2 2 2 0 5 5 5 5 0 0 0 0 0 0
0 0 0 2 2 2 0 5 5 5 5 0 0 0 0 0 0
0 0 0 2 2 2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 0 0 0 0 4 4 4 4 4 0 0
0 0 0 0 0 0 0 0 0 0 4 4 4 4 4 0 0
0 0 0 0 0 0 0 0 0 0 4 4 4 4 4 0 0
0 0 0 0 0 0 0 0 0 0 4 4 4 4 4 0 0
```

<PIL.Image.Image image mode=RGB size=1088x960 at 0x7F4C1B74F850>

**output:**
```
5
```

<PIL.Image.Image image mode=RGB size=64x64 at 0x7F4C1B67E450>

## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 1 1 0 0 3 3 3 3 3 0 0
0 0 1 1 1 1 1 1 0 0 3 3 3 3 3 0 0
0 0 1 1 1 1 1 1 0 0 3 3 3 3 3 0 0
0 0 1 1 1 1 1 1 0 0 3 3 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 2 2 0 0 7 7 7 7 7 0
0 0 2 2 2 2 2 2 2 0 0 7 7 7 7 7 0
0 0 2 0 0 0 2 2 2 0 0 7 7 7 7 7 0
0 0 2 0 0 0 2 2 2 0 0 7 7 7 7 7 0
0 0 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=1088x1024 at 0x7F4C1B67E3D0>

**output:**
```
2
```

<PIL.Image.Image image mode=RGB size=64x64 at 0x7F4C1B67EAD0>
<PIL.Image.Image image mode=RGB size=3136x1168 at 0x7F4C1B700550>Okay, I'm ready to analyze this ARC-AGI task. Here's my breakdown of the provided examples:

**Perception of Elements:**

The task involves 2D grids (input) and single digits (output). The input grids contain various colored rectangular objects, with 0 (white) representing the background. The output appears to be a single digit, possibly corresponding to one of the colored objects within the input grid. The key seems to be identifying a specific colored rectangle and then outputting its color value.

**YAML Block (Facts):**


```yaml
task_type: object_selection
objects:
  - type: rectangle
    properties:
      - color: [white, blue, red, green, yellow, gray, magenta, orange, azure, maroon]
      - size: variable
      - position: variable
  - type: background
    properties:
      - color: white
      - size: entire_grid

actions:
  - type: identify_largest_rectangle
  - type: select_rectangle_by_color
  - type: find_inner_rectangle
  - type: get_rectangle_color
relationships:
  - rectangles: contain_other_rectangles

```


**Natural Language Program:**

1.  **Identify Rectangles:** Examine the input grid and identify all distinct rectangular shapes formed by contiguous pixels of the same color.
2.  **Find "Inside" Rectangle** If a rectangle fully encloses the non-zero pixels of one and only one other rectangle, select the inside rectangle.
3.  **Output Color:** Output the color code (single digit integer) of that inside rectangle.

The core idea is focusing on a unique enclosed rectangle and reporting its color value.

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
