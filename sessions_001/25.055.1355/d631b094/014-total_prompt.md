# d631b094 • 014 • example_3 • investigate_coder

---

## Example 3

**input:**
```
0 7 0
0 0 0
0 0 0
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x7DCBFF5DB6D0>

**output:**
```
7
```

<PIL.Image.Image image mode=RGB size=64x64 at 0x7DCBFF5DA6E0>
Okay, here's my analysis of the example input-output pair, structured as requested:

**Perception of Elements:**

The input is a 3x3 grid. Most cells are white (0), except for a single orange (7) cell in the top row, middle column. The output is a 1x1 grid containing only the orange (7) cell. It appears the transformation extracts the non-zero element.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    dimensions: 3x3
    elements:
      - value: 0
        color: white
        count: 8
      - value: 7
        color: orange
        count: 1
  - type: grid
    dimensions: 1x1
    elements:
      - value: 7
        color: orange
        count: 1

actions:
  - type: extraction
    description: "Extract the non-zero element from the input grid."

relationships:
  - type: input-output
    description: "The output grid contains only the single non-zero element present in the input grid."
```


**Natural Language Program:**

1.  Examine the input grid.
2.  Identify the single cell with a non-zero value.
3.  Create a 1x1 output grid containing only the value from that identified cell.

In more concise form: Extract the single non-zero value from the input grid and place it in a 1 x 1 grid

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
