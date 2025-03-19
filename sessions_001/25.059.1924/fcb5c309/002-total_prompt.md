# fcb5c309 • 002 • example_3 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 4 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 0 0 0 0
2 2 2 2 2 2 2 0 0 0 0 0 0
2 0 0 0 0 0 2 0 0 0 2 2 2
2 4 0 0 0 0 2 0 0 0 2 0 2
2 0 0 0 0 0 2 0 0 0 2 0 2
2 0 0 0 4 0 2 0 0 0 2 2 2
2 0 0 0 0 0 2 0 0 0 0 0 0
2 2 2 2 2 2 2 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0 0 4 0
```

<PIL.Image.Image image mode=RGB size=832x832 at 0x716635BBB5D0>

**output:**
```
4 4 4 4 4 4 4
4 0 0 0 0 0 4
4 4 0 0 0 0 4
4 0 0 0 0 0 4
4 0 0 0 4 0 4
4 0 0 0 0 0 4
4 4 4 4 4 4 4
```

<PIL.Image.Image image mode=RGB size=448x448 at 0x716635BBBE50>

## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0
0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 1 1 1 1 1 1 1 0
0 0 0 0 0 0 0 0 1 0 0 3 0 0 1 0
0 3 0 0 0 3 0 0 1 0 0 0 0 0 1 0
0 0 0 0 0 0 3 0 1 3 0 3 0 0 1 0
0 0 0 0 0 0 0 0 1 0 0 0 0 0 1 0
0 1 1 1 1 1 1 0 1 1 1 1 1 1 1 0
0 1 0 0 0 0 1 0 0 0 0 0 0 0 0 0
0 1 0 0 0 3 1 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 1 0 0 0 0 0 0 0 0 0
3 1 1 1 1 1 1 0 0 0 0 3 0 0 0 0
3 0 0 0 0 0 0 3 0 0 3 3 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=1024x832 at 0x716635BBB550>

**output:**
```
3 3 3 3 3 3 3
3 0 0 3 0 0 3
3 0 0 0 0 0 3
3 3 0 3 0 0 3
3 0 0 0 0 0 3
3 3 3 3 3 3 3
```

<PIL.Image.Image image mode=RGB size=448x384 at 0x716635B76A50>

## train_3

**input:**
```
0 0 0 0 0 0 0 0 2 0 0 0 0 0 0 0
0 3 3 3 3 3 3 3 0 0 2 0 0 0 0 0
0 3 0 2 0 2 0 3 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 3 0 0 3 3 3 3 0 0
0 3 0 0 0 0 0 3 2 0 3 0 2 3 0 0
0 3 0 2 0 0 0 3 0 0 3 0 0 3 0 0
0 3 0 0 0 0 2 3 0 0 3 0 0 3 0 0
0 3 3 3 3 3 3 3 0 0 3 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0
0 0 0 3 3 3 0 2 0 0 0 0 0 0 0 2
0 0 0 3 0 3 0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 3 0 0 0 0 0 2 0 0 0 0
0 0 2 3 3 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=1024x960 at 0x716635B76B50>

**output:**
```
2 2 2 2 2 2 2
2 0 2 0 2 0 2
2 0 0 0 0 0 2
2 0 0 0 0 0 2
2 0 2 0 0 0 2
2 0 0 0 0 2 2
2 2 2 2 2 2 2
```

<PIL.Image.Image image mode=RGB size=448x448 at 0x716635B76050>
<PIL.Image.Image image mode=RGB size=3008x1488 at 0x716635BE9050>Okay, let's analyze the provided examples to understand the transformation.

**Perception of Elements:**

The task involves 2D grids of colored pixels. The input grids have varying dimensions and contain multiple colors, while the output grids are smaller, have a consistent square-like shape, and mostly consist of a single color with some background (white/0) pixels. The key seems to be identifying a specific color in the input and creating a bounding box around it in the output. Other colors appear to be irrelevant to the transformation.

**YAML Block (Facts):**


```yaml
objects:
  - name: input_grid
    type: 2D array
    properties:
      - colors: [0-9] (representing different colors)
      - dimensions: variable (rows x columns)
  - name: output_grid
    type: 2D array
    properties:
      - colors: [0-9]
      - dimensions: variable, but generally forms a bounding box
  - name: target_color
    type: integer
    properties:
      - value: varies per example (4, 3, then 2)

actions:
  - name: identify_target_color
    description: Determine the color that defines the bounding box.
  - name: find_bounding_box
    description: Locate the outermost positions of the target color in the input grid.
  - name: create_output
    description: Generate an output grid where all pixels within the bounding box are filled with the target color, except for the inner '0' pixels.

relationships:
  - input_grid contains target_color
  - output_grid is a bounding_box representation of target_color in input_grid
```


**Natural Language Program:**

1. **Identify the Target Color:**  For each example pair, there's a single color, other than white (0), that is prominent in the output grid. This is the "target color". In the first example its 4 (yellow), in the second it's 3 (green), in the third it is 2 (red).

2. **Find the Bounding Box:** In the input grid, find the minimum and maximum row and column indices where the target color appears. This defines a rectangular bounding box.

3. **Create the Output Grid:** Create a new grid.
    -   The dimensions of this new grid are determined by the size of the bounding box (max_row - min_row + 1, max_col - min_col + 1).
    -   Fill all cells within the bounding box with the target color.
    -   Iterate over the cells of the original input. If a cell in the input grid is equal to 0 and is positioned inside the bounding box set corresponding output cell to 0.

Essentially, the transformation extracts a rectangular region from the input grid based on the extent of a specific color and fills it with target color, preserving inner '0' pixels.

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
