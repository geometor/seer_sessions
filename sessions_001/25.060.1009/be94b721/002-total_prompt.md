# be94b721 • 002 • example_4 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 3 3 0 0 0 0 0 0
0 0 2 0 0 0 3 0 0 1 0 0 0
0 0 2 2 0 0 0 0 1 1 0 0 0
0 2 2 2 0 0 0 0 1 1 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=832x448 at 0x7FC253C82050>

**output:**
```
2 2 0
0 2 0
0 2 2
2 2 2
```

<PIL.Image.Image image mode=RGB size=192x256 at 0x7FC253C82750>

## train_2

**input:**
```
0 0 0 0 0 0 0 6 6 0
0 3 0 0 4 4 0 0 6 0
3 3 3 0 4 4 0 0 0 0
0 3 0 0 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x320 at 0x7FC253C82150>

**output:**
```
4 4
4 4
4 4
```

<PIL.Image.Image image mode=RGB size=128x192 at 0x7FC25B7097D0>

## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 0 0 0 0 7 7 0
0 0 8 0 0 0 2 0 0 7 0
0 8 8 0 0 2 2 0 0 7 0
0 8 8 0 0 0 2 0 0 7 0
0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=704x384 at 0x7FC25B70AED0>

**output:**
```
8 8 8
0 8 0
8 8 0
8 8 0
```

<PIL.Image.Image image mode=RGB size=192x256 at 0x7FC25B70A250>

## train_4

**input:**
```
0 0 0 0 0 0 0 0 0
0 0 0 7 0 0 2 2 2
0 0 0 7 7 0 0 2 0
0 0 0 0 7 0 2 2 2
8 8 8 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=576x448 at 0x7FC25B70A650>

**output:**
```
2 2 2
0 2 0
2 2 2
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x7FC25B70BC50>
<PIL.Image.Image image mode=RGB size=2912x784 at 0x7FC25B70A550>Okay, let's analyze the provided examples to understand the transformation rule.

**Perception of Elements:**

The task involves 2D grids with single-digit integer values (0-9) representing different colors. The transformation seems to focus on extracting a specific colored object from the input grid and presenting it as the output grid, with the rest of the grid converted to 0. The extracted shapes are always solid rectangles and have the largest area compared to other colored object in the image.

**Facts (YAML):**


```yaml
objects:
  - name: input_grid
    type: 2D array
    properties:
      - values: integers (0-9)
      - colors: mapped to values (COLOR_MAP)

  - name: output_grid
    type: 2D array
    properties:
      - values: integers (0-9)
      - colors: mapped to values

  - name: target_object
    type: contiguous block
    properties:
      - color: single color
      - shape: rectangular
      - criteria: largest area among objects of distinct colors
      

actions:
  - name: identify_largest_object
    description: Find the largest contiguous rectangular block of a single color.
  - name: extract_object
    description: Create a new grid containing only the identified object.
  - name: pad_object
    description: replace all other values in new grid with 0

relationships:
  - input_grid contains multiple target_object instances
  - output_grid is a minimal representation of one target_object
  - output_grid is derived from the input_grid.

```


**Natural Language Program:**

1.  **Identify Objects:** Scan the input grid and identify all distinct contiguous rectangular regions of the same color.
2.  **Calculate Areas:** Determine the area (number of pixels) of each identified object.
3.  **Select Largest:** Find the object with the largest area.
4.  **Extract:** Create a new grid, copying only the pixels of the largest object, preserving its shape and relative position.
5.  **Isolate and output**: set every cell not part of the identified object in the new grid to 0 (white), the output grid shows only the largest object.


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
