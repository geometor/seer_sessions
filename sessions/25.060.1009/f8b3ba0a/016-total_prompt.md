# f8b3ba0a • 016 • example_3 • investigate_coder

---

## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 3 3 0 3 3 0 3 3 0
0 0 0 0 0 0 0 0 0 0
0 1 1 0 3 3 0 3 3 0
0 0 0 0 0 0 0 0 0 0
0 3 3 0 8 8 0 3 3 0
0 0 0 0 0 0 0 0 0 0
0 3 3 0 8 8 0 3 3 0
0 0 0 0 0 0 0 0 0 0
0 3 3 0 2 2 0 2 2 0
0 0 0 0 0 0 0 0 0 0
0 2 2 0 3 3 0 3 3 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x832 at 0x7FC253D7EED0>

**output:**
```
2
8
1
```

<PIL.Image.Image image mode=RGB size=64x192 at 0x7FC252BC6450>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The input is a grid of colored pixels (represented by numbers 0-9). The output appears to be a sequence of single-digit numbers, each corresponding to a color. There are repeating horizontal lines of '0' values. The relevant data is in blocks between the solid white (0) lines. Inside those blocks, there are pairs of colored blocks, each is a different color.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    properties:
      rows: 13
      columns: 10
      cells: pixels (integers 0-9)
  - type: block
    properties:
      color: varies (1, 2, 3, 8)
      shape: 2x2 rectangle
      location: varies
  - type: output_sequence
    properties:
      elements: integers
      length: 3

actions:
    - identify_blocks: Locate 2x2 regions of non-zero, uniform color.
    - extract_color: Determine the color value of each identified block.
    - order: vertically stack in ascending row number
    - build sequence: construct a sequence of colors from blocks.
    

relationships:
  - blocks_within_grid: The 2x2 blocks are contained within the larger grid.
  - color_to_output: each block color is a single value in the output
  - ordering: color values are presented vertically stacked.

```


**Natural Language Program:**

1.  **Identify Blocks:** Scan the input grid to find all 2x2 square regions where all four pixels have the same non-zero color.
2.  **Ignore Background:** Disregard any rows that consist entirely of '0' (white) pixels.
3.  **Extract Color:** For each identified 2x2 block, record the color value (the number) of the pixels within that block.
4. **Order Colors:** Sort the extracted color in ascending order by the row that they appear. The first one appears on row 4, the second on row 8, and the third on row 10.
5.  **Build Output:** Create an output sequence which contains the sorted colors, where each is a separate entry presented as single stacked values.


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
