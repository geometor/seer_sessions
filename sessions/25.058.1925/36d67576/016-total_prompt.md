# 36d67576 • 016 • example_3 • investigate_coder

---

## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 2 0 0 0 0 0 0 0 0
0 1 4 4 4 0 0 0 0 0 0 0 0
0 0 3 4 0 0 0 0 0 0 0 0 0
0 0 0 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 4 0 0 0 0
0 0 0 0 0 0 0 4 4 4 0 0 0
0 0 0 0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0 0 0 0
0 0 0 4 4 4 0 0 0 0 0 0 0
0 0 0 2 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=832x832 at 0x78E5F214A550>

**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 2 0 0 0 0 0 0 0 0
0 1 4 4 4 0 0 0 0 0 0 0 0
0 0 3 4 0 0 0 0 0 0 0 0 0
0 0 0 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 4 0 0 0 0
0 0 0 0 0 0 0 4 4 4 1 0 0
0 0 0 0 0 0 0 0 4 3 0 0 0
0 0 0 0 1 0 0 0 1 0 0 0 0
0 0 0 0 4 3 0 0 0 0 0 0 0
0 0 0 4 4 4 1 0 0 0 0 0 0
0 0 0 2 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=832x832 at 0x78E5F214AAD0>
Okay, here's my analysis of the provided input-output example, formatted as a report:

**Perception of Elements:**

The task involves a grid of colored pixels (represented by numbers 0-9). The input and output grids have the same dimensions. There are multiple distinct colored "objects" within the grid, which seem to be defined by contiguous blocks of non-zero pixels. The primary colors present are blue (1), red (2), green (3), and yellow (4), along with white/background (0). There's an apparent interaction or modification of existing yellow object.

**YAML Fact Documentation:**


```yaml
facts:
  - observation: |
      The input and output grids have identical dimensions (13x13).
  - objects:
      - type: contiguous_block
        description: A group of one or more pixels of the same non-zero color, adjacent either horizontally or vertically.
        properties:
          - color: Identified by the digit (1-9) representing the color.
          - shape: Defined by the arrangement of pixels.
      - type: background
        description: pixels with value 0.
        properties:
          - color: white, represented by 0
  - actions:
    - type: modification
      description: |
            There is one blue pixel color added to the right side of an object and it appears as extension to that object.

  - relationships:
      - type: spatial
        description: Objects are positioned relative to each other within the grid.
      - type: modification_target
        description: There is a change in some objects from input and output and this happens only one yellow object.
```


**Natural Language Program:**

1.  **Identify Objects:** Scan the input grid and identify all contiguous blocks of non-zero colored pixels. Consider each of these as a distinct object.

2.  **Locate Target Object:** Locate the objects that are yellow in the input grid.

3.  **Perform Modification**: The last two rows (from bottom to top) of yellow object are replaced with blue.
    If there is one isolated pixel of yellow color, that yellow pixel is going to change to green.

4.  **Reconstruct Grid:** Preserve all unchanged. Place modified object from input into the new output grid.

5.  **Output:** The modified grid is the final output.

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
