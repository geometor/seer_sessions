# 2dee498d • 008 • example_2 • investigate_coder

---

## Example 2

**input:**
```
2 0 0 1 2 0 0 1 2 0 0 1
4 2 1 4 4 2 1 4 4 2 1 4
4 1 2 4 4 1 2 4 4 1 2 4
1 0 0 2 1 0 0 2 1 0 0 2
```

<PIL.Image.Image image mode=RGB size=768x256 at 0x74AF37938F50>

**output:**
```
2 0 0 1
4 2 1 4
4 1 2 4
1 0 0 2
```

<PIL.Image.Image image mode=RGB size=256x256 at 0x74AF1C88F250>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves transforming a rectangular grid of colored pixels into a smaller rectangular grid. The colors are represented by single-digit integers. The input grid appears to have a repeating pattern, and the output grid seems to be a condensed version of that pattern. The dimensions of the grid are reduced. It looks like columns are being removed.

**YAML Block (Facts):**


```yaml
facts:
  - type: grid
    description: input grid
    dimensions: 4x12
    elements: colored pixels (integers 0-9)
    pattern: repeating sequence of columns
  - type: grid
    description: output grid
    dimensions: 4x4
    elements: colored pixels (integers 0-9)
    pattern: subset of input grid columns
  - operation: column removal
    description: every third column is removed to create output.
```


**Natural Language Program:**

The input grid is transformed into the output grid by removing every third column. Iterate through the input grid's columns. Keep the first two, remove the third and repeat until all rows are complete. The output contains same rows, but only with a subset of the original columns.

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
