# a65b410d • 010 • example_2 • investigate_coder

---

## train_2

**input:**
```
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=576x512 at 0x7F4C1B703C50>

**output:**
```
3 3 3 3 3 3 0 0 0
3 3 3 3 3 0 0 0 0
3 3 3 3 0 0 0 0 0
2 2 2 0 0 0 0 0 0
1 1 0 0 0 0 0 0 0
1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=576x512 at 0x7F4C1B703DD0>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves transforming a grid of numerical values (representing colors) into another grid of numerical values. The input grid appears to contain a single horizontal line of red (2) pixels. The output grid seems to be an expansion and diversification of this initial line, introducing green (3) and blue (1) pixels in a specific pattern above and below the original red line.

**YAML Block (Facts):**


```yaml
facts:
  - object: horizontal_line
    properties:
      color: red (2)
      location: row 4
      length: 3 pixels
    actions:
      - expanded_upward: 3 rows of green (3) pixels created
      - expanded_downward: 2 rows created, with decreasing length and alternating colors of blue(1) and white (0)
  - grid_size:
    input:
      width: 9
      height: 8
    output:
      width: 9
      height: 8
```


**Natural Language Program:**

1.  **Identify:** Locate the horizontal line of red (2) pixels in the input grid.
2.  **Expand Upward:** Above the red line, create three rows of green (3) pixels. Each subsequent row of green pixels extends one pixel further to the left than the row below it.
3.  **Expand Downward:** Below the red line, create two rows.
    *   The first row consists of blue (1) pixels, and its length is one pixel less than the red line.
    *   The second row has one blue (1) pixel at the left, and is one pixel shorter than the blue line above.
4. **Fill:** The rest of the output grid is filled with white pixels.


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
