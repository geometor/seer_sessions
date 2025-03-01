# 3428a4f5 • 016 • example_3 • investigate_coder

---

## train_3

**input:**
```
2 2 0 2 2
2 0 2 2 2
2 0 0 0 0
0 2 0 2 0
2 2 2 0 2
2 0 2 0 0
4 4 4 4 4
2 0 0 2 2
0 0 2 0 2
2 2 0 0 0
0 0 2 0 2
0 2 0 2 2
0 2 2 0 2
```

<PIL.Image.Image image mode=RGB size=320x832 at 0x7B4BFDBD37D0>

**output:**
```
0 3 0 0 0
3 0 0 3 0
0 3 0 0 0
0 3 3 3 3
3 0 3 3 0
3 3 0 0 3
```

<PIL.Image.Image image mode=RGB size=320x384 at 0x7B4C05B57ED0>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves transforming a larger grid (input) into a smaller grid (output). The input grid contains pixels of colors red (2), white (0), and yellow (4). The output grid contains pixels of colors green (3) and white (0). The output grid appears to be a condensed or abstracted version of the input grid, focusing on specific features and changing their colors. The single row of yellow (4) pixels in the input seems to be particularly important.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    properties:
      - name: input_grid
        dimensions: [13, 5]
        colors: [red, white, yellow]
      - name: output_grid
        dimensions: [6, 5]
        colors: [green, white]
  - type: pixel
    properties:
      - color: red, white, yellow, green

actions:
  - name: condense
    description: Reduce the size of the grid.
  - name: recolor
    description: Change the color of certain pixels.
  - name: locate_yellow_row
    description: identify y-position of the row with all yellow pixels

relationships:
  - type: spatial
    description: The output grid is smaller than the input grid.
  - type: color_mapping
    description:  red pixels in a specific region map to green; all other red pixels seem to map to white
```


**Natural Language Program:**

1.  **Locate the Yellow Row:** Find the row index in the input grid that is entirely filled with yellow (4) pixels.
2. **Define Output Region:** Determine a region of interest in the input grid. The top of the region of interest begins one row above yellow row, the region of interest continues to the end of input. The height of the output grid can be calculated by `input_grid.height - yellow_row_index`
3. **Condense:** Reduce input grid section above the identified yellow row to output grid size
4.  **Recolor:** Within this new grid section, change all red (2) pixels to green (3). All other colors become white (0).


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
