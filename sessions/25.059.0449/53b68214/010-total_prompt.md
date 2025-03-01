# 53b68214 • 010 • example_2 • investigate_coder

---

## train_2

**input:**
```
0 0 3 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x320 at 0x7440707191D0>

**output:**
```
0 0 3 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x744068D79F50>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves 2D grids. The primary element is a vertical line of green (color code 3) pixels. The input grid is smaller (5x10) than the output grid (10x10). The green line remains in the same x-coordinate (column 2) in both input and output. The output grid seems to be an expansion of the input grid's height, repeating the input pattern to fill the new rows.

**YAML Block (Facts):**


```yaml
objects:
  - name: grid
    type: 2D array
    properties:
      - width: 10
      - height: variable (5 in input, 10 in output)
      - values: integers (0-9 representing colors)
  - name: green_line
    type: object
    properties:
      - color: green (3)
      - shape: vertical line
      - position:
        - x: 2 # Column index 2 (third column)
        - y: variable # Extends the full height
    relationship: green_line is contained within grid

actions:
  - name: expand_height
    description: The grid's height is doubled.
    parameters:
      - input_height: 5
      - output_height: 10

  - name: repeat_pattern
    description: The pattern of the input grid is repeated vertically in the output grid.

```


**Natural Language Program:**

1.  **Identify the Input:** We have an input grid of 5 rows and 10 columns. A vertical line of green pixels (color 3) exists at column index 2 (the third column).

2.  **Determine Output Dimensions:** The output grid's width remains the same (10 columns), but its height is doubled to 10 rows.

3. **Vertical Pattern Repetition:** Duplicate the entire rows of input and append below.

4.  **Preserve the Green Line:** The green line at column index 2 is preserved and extended to the full height of the expanded output grid. Effectively the input rows pattern repeats to the output height.

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
