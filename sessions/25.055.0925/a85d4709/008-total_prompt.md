# a85d4709 • 008 • example_2 • investigate_coder

---

## Example 2

**input:**
```
0 0 5
0 0 5
0 0 5
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x7EB509BCAC80>

**output:**
```
3 3 3
3 3 3
3 3 3
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x7EB509A69A80>
Okay, here's my analysis of the provided example, formatted as a report:

**Perception of Task Elements:**

The task involves a transformation of a grid of single-digit integers. The input grid contains the values 0 and 5, while the output grid contains only the value 3. The dimensions of the grid (3x3) remain constant across the transformation. The colors associated with the digits, are white (0), gray (5), and green (3).

**YAML Fact Block:**


```yaml
facts:
  - subject: input_grid
    attribute: dimensions
    value: 3x3
    relation: same_as
    object: output_grid
  - subject: input_grid
    attribute: cell_values
    value: [0, 5]
  - subject: output_grid
    attribute: cell_values
    value: [3]
  - subject: transformation
    attribute: type
    value: replacement
    description: All cell values in the input grid are replaced with the value 3 in the output grid.
```


**Natural Language Program:**

1.  **Initialization:** Start with an input grid of size 3x3.
2.  **Replacement:** Replace every value within input to 3 to make output grid.
3. **Termination**: The final output is 3x3 grid of 3.

In essence, the program takes every cell within an NxM matrix and replace all values with the constant `3`.

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
