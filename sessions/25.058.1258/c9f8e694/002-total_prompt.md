# c9f8e694 • 002 • example_2 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
1 0 5 5 0 0 0 0 0 0 0 0
2 0 5 5 0 0 0 0 0 0 0 0
1 0 5 5 0 0 0 0 0 0 0 0
1 0 5 5 0 0 0 0 0 0 0 0
1 0 5 5 0 0 0 0 5 5 0 0
2 0 5 5 0 0 0 0 5 5 0 0
2 0 5 5 0 0 0 0 5 5 0 0
1 0 0 0 0 0 0 0 5 5 0 0
1 0 0 0 5 5 5 0 5 5 0 0
1 0 0 0 5 5 5 0 5 5 0 0
2 0 0 0 5 5 5 0 5 5 0 0
```

<PIL.Image.Image image mode=RGB size=768x768 at 0x7E120E2F6350>

**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0
1 0 1 1 0 0 0 0 0 0 0 0
2 0 2 2 0 0 0 0 0 0 0 0
1 0 1 1 0 0 0 0 0 0 0 0
1 0 1 1 0 0 0 0 0 0 0 0
1 0 1 1 0 0 0 0 1 1 0 0
2 0 2 2 0 0 0 0 2 2 0 0
2 0 2 2 0 0 0 0 2 2 0 0
1 0 0 0 0 0 0 0 1 1 0 0
1 0 0 0 1 1 1 0 1 1 0 0
1 0 0 0 1 1 1 0 1 1 0 0
2 0 0 0 2 2 2 0 2 2 0 0
```

<PIL.Image.Image image mode=RGB size=768x768 at 0x7E120E2F6210>

## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
3 5 5 5 5 0 0 0 0 0 0 0
3 5 5 5 5 0 0 5 5 5 5 5
4 5 5 5 5 0 0 5 5 5 5 5
4 5 5 5 5 0 0 5 5 5 5 5
3 0 0 0 0 0 0 5 5 5 5 5
4 0 0 0 5 5 5 5 5 5 5 5
3 0 0 0 5 5 5 5 5 5 5 5
3 0 0 0 5 5 5 5 5 5 5 5
3 0 0 0 5 5 5 5 5 5 5 5
4 0 0 0 5 5 5 0 0 0 0 0
4 0 0 0 5 5 5 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=768x768 at 0x7E120E2F6030>

**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0
3 3 3 3 3 0 0 0 0 0 0 0
3 3 3 3 3 0 0 3 3 3 3 3
4 4 4 4 4 0 0 4 4 4 4 4
4 4 4 4 4 0 0 4 4 4 4 4
3 0 0 0 0 0 0 3 3 3 3 3
4 0 0 0 4 4 4 4 4 4 4 4
3 0 0 0 3 3 3 3 3 3 3 3
3 0 0 0 3 3 3 3 3 3 3 3
3 0 0 0 3 3 3 3 3 3 3 3
4 0 0 0 4 4 4 0 0 0 0 0
4 0 0 0 4 4 4 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=768x768 at 0x7E120E2F62B0>
<PIL.Image.Image image mode=RGB size=1596x1586 at 0x7E120DD8AA30>Okay, here's my analysis of the provided input-output pairs, formatted as requested:

**Perception of Elements:**

The task involves 2D grids where each cell contains a single digit integer representing a color. The primary operation appears to be a kind of "color replacement" or "selective recoloring". Specifically, a certain color (represented by a digit) within the input grid is replaced by the color of a neighboring pixel. It seems that only one color is subject to the replacement in each example, while all other colors are maintained. The shapes created by same colored pixels influence where replacement color comes from.

**YAML Fact Documentation:**


```yaml
facts:
  - task_type: color_transformation
  - objects:
    - grid: 2D array of digits
    - cells: individual elements within the grid, representing colors
    - color_blocks: contiguous regions of the same color
  - properties:
    - color: digit representing the color of a cell
    - position: row and column index of a cell
  - actions:
    - replace_color: changing the color of a cell to a different color
  - relationships:
    - adjacency: cells sharing a side (not just a corner)
    - color_block_membership: a cell belonging to a group of adjacent cells with same color

```


**Natural Language Program:**

1.  **Identify the Target Color:** In each pair, find the color that changes from input to output (5 in example one and 5 in example two).

2.  **Identify Seed color** Locate the seed color - color of the pixel directly left of Target color at top left corner of the grid. If left side is Target color or 0, then locate pixel directly above first instance.

3. **Replace target color pixels:** Replace the color in the target color pixels with the seed color.
4.  **Preserve Other Colors:** All other colors in the input grid remain unchanged in the output grid.

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
