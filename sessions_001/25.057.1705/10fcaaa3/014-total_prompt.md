# 10fcaaa3 • 014 • example_3 • investigate_coder

---

## Example 3

**input:**
```
0 0 0
0 4 0
0 0 0
0 0 0
4 0 0
```

<PIL.Image.Image image mode=RGB size=192x320 at 0x777851601D10>

**output:**
```
8 0 8 8 0 8
0 4 0 0 4 0
8 0 8 8 0 8
0 8 8 0 8 0
4 0 0 4 0 0
8 8 8 8 8 8
0 4 0 0 4 0
8 0 8 8 0 8
0 8 8 0 8 0
4 0 0 4 0 0
```

<PIL.Image.Image image mode=RGB size=384x640 at 0x7778516016D0>
Okay, here's my analysis of the provided example, formatted as a report:

**Perception of Task Elements:**

The task involves transforming a smaller grid (input) into a larger grid (output). The primary colors involved are white (0), yellow (4), and azure (8). The output grid appears to be an expansion and a patterned replication of the input grid, with the addition of the azure color. The yellow pixels in the input seem to maintain their relative positions within a subsection of the output, while also appearing in a mirrored position. The azure color seems to fill in a checkerboard-like pattern, and also forms a border around blocks of four cells.

**YAML Fact Block:**


```yaml
facts:
  - object: input_grid
    type: grid
    properties:
      - colors: [white, yellow]
      - dimensions: [5, 3]
  - object: output_grid
    type: grid
    properties:
      - colors: [white, yellow, azure]
      - dimensions: [10, 6]
  - observation: yellow_pixels_replicated
    details: Yellow pixels from input appear in the output, maintaining relative position within a quadrant and mirrored.
  - observation: azure_fills_pattern
    details: Azure color creates a checkerboard pattern and outlines 2x2 blocks.
  - observation: dimensions_relationship
    details: Output grid dimensions are double the input grid dimensions (height * 2, width * 2).
  - action: expand_and_replicate
    details: The input grid is expanded, and elements are replicated with a specific pattern and added color.
```


**Natural Language Program:**

1.  **Double Dimensions:** Create a new output grid with dimensions twice as large as the input grid (double the height and double the width).

2.  **Replicate Yellow:** Copy each yellow (4) pixel from the input grid to the output grid. The positions in the output grid can be described as `(row * 2 + 1, col * 2 + 1)` where row and col are from the original input indices, and the row and column are 0-indexed. Replicate copied yellow positions by creating mirror along the new row axis.

3. **Fill with Azure background:** Create a checkerboard pattern filling in with 8 by taking each output pixel and checking this condition `(row + col) % 2 == 0`.

4.  **Overlay Border:** For any empty cells, if the cells above, below, left, or right are of the azure color, change this empty cell to azure.

5.  **Fill Remaining:** All the cells that still contain white(0) should be set to be azure(8).

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
