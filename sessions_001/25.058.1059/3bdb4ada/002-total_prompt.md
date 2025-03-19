# 3bdb4ada • 002 • example_2 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 0
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 0
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=1920x512 at 0x7DBFF21C1BD0>

**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 0
4 0 4 0 4 0 4 0 4 0 4 0 4 0 4 0 4 0 4 0 4 0 4 0 4 0 4 0 4 0
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 8 0 8 0 8 0 8 0 8 0 8 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=1920x512 at 0x7DBFF1F77D90>

## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7 7 7 7 7 7 7 7 7 7 7 0 0
0 0 0 0 0 0 0 7 7 7 7 7 7 7 7 7 7 7 0 0
0 0 0 0 0 0 0 7 7 7 7 7 7 7 7 7 7 7 0 0
```

<PIL.Image.Image image mode=RGB size=1280x512 at 0x7DBFF1F76850>

**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0
0 1 0 1 0 1 0 1 0 1 0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7 7 7 7 7 7 7 7 7 7 7 0 0
0 0 0 0 0 0 0 7 0 7 0 7 0 7 0 7 0 7 0 0
0 0 0 0 0 0 0 7 7 7 7 7 7 7 7 7 7 7 0 0
```

<PIL.Image.Image image mode=RGB size=1280x512 at 0x7DBFF1F77E30>
<PIL.Image.Image image mode=RGB size=3260x1074 at 0x7DBFF201CD70>Okay, let's analyze the provided input-output pairs to understand the transformation.

**Perception of Elements:**

The task involves 2D grids containing colored pixels. The primary colors involved are yellow (4), azure (8), blue (1), and orange (7), with white (0) seemingly acting as a background or separator. The transformation seems to involve a consistent alteration of colored regions, specifically, an insertion of a white (0) pixel at every other position within each colored, contiguous, horizontal block, along rows where they originally formed a continuous line.

**YAML Block - Facts:**


```yaml
objects:
  - type: grid
    description: 2D array of pixels
    properties:
      - width: number of columns
      - height: number of rows
      - cells: values representing colors

  - type: block
    description: Contiguous horizontal sequence of pixels of the same color.
    properties:
      - color: integer value (0-9)
      - start_x: starting column index
      - end_x: ending column index
      - row: row index
      - length: number of pixels (end_x - start_x + 1)

actions:
  - name: checker
    description: Inserts a background pixel (0) at every other position within a block.
    parameters:
      - block: The target block.

relationships:
  - type: spatial
    description: Blocks are contained within the grid. Blocks of the same color are grouped, rows within a group alternate being checked.
```


**Natural Language Program:**

1.  **Identify Blocks:** Iterate through each row of the input grid. For each row, identify contiguous horizontal blocks of non-background (non-0) pixels. A block is defined by its starting column, ending column, color, and row number.

2.  **Group Blocks:** Group blocks by the original input row and by color.

3.  **Alternate Rows:** Withing each group of blocks, every *other* horizontal block will be modified to be checkered with white.

4.  **Checker:** For each *other* block, iterate through its pixels. Replace every other pixel with a background pixel (0), starting from the second pixel in the block.

5. **Construct Output:** Create an output grid identical to the input grid. Apply modifications by creating a checkered pattern in the identified blocks, starting on the second row.

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
