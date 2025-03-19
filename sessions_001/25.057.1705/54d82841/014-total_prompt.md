# 54d82841 • 014 • example_3 • investigate_coder

---

## Example 3

**input:**
```
0 0 0 0 0 0 0
0 8 8 8 0 0 0
0 8 0 8 6 6 6
0 0 0 0 6 0 6
0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=448x320 at 0x777869E5D450>

**output:**
```
0 0 0 0 0 0 0
0 8 8 8 0 0 0
0 8 0 8 6 6 6
0 0 0 0 6 0 6
0 0 4 0 0 4 0
```

<PIL.Image.Image image mode=RGB size=448x320 at 0x777851443E30>
Okay, here's my analysis of the provided example, formatted as a report:

**Perception of Elements:**

The task involves a grid of colored pixels. The input grid transforms into the output grid based on some rule. The most obvious change is the addition of a new row at the bottom, containing yellow (4) pixels.  The placement of the yellow pixels seems related to the columns, and possibly to the absence of colors other than white (0).

**YAML Block (Facts):**


```yaml
facts:
  - object: grid
    properties:
      - dimensions: 5x7 (input), 6x7 (output)
      - cell_values: integers (0-9) representing colors
  - object: pixel
    properties:
      - color:  mapped to integer value (0: white, 6: magenta, 8: azure, 4: yellow)
      - position: row and column index within the grid
  - action: add_row
    description: A new row is added to the bottom of the grid.
  - action: set_pixel_color
    description: Pixels in the new row are assigned the color yellow (4).
    conditions:
      - column_condition: set the color to 4 if the input grid column contains only 0.
  - relationships:
       -  "new row position is below original grid"
       -  "yellow pixel in new row appears only at the bottom of the column containing only value 0 (white)"
```


**Natural Language Program:**

1.  **Add a new row** at the bottom of the input grid.
2.  **Iterate through each column** of the *original* input grid.
3.  **Check Column Values:** For each column, determine if the input column values are *all* white (0).
4. **Populate new row**
    * If all the original values are 0 (white) in input, set the corresponding pixel in the new row to yellow (4).
    * leave all other pixels in the bottom row as 0 (white).

Essentially, the transformation adds a row that flags columns that were originally all white with a yellow pixel at the bottom.

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
