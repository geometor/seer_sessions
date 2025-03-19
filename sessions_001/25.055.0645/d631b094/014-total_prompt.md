# d631b094 • 014 • example_3 • investigate_coder

---

## Example 3

**input:**
```
0 7 0
0 0 0
0 0 0
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x73226F5CEB30>

**output:**
```
7
```

<PIL.Image.Image image mode=RGB size=64x64 at 0x73226F5CF5B0>
Okay, here's my analysis of the example input-output pair, presented as a report:

**Perception of Task Elements:**

The input is a 3x3 grid. Most of the cells are '0' (white), except for a single cell with '7' (orange) in the top-middle position. The output is a 1x1 grid containing only the value '7' (orange). It appears the task involves extracting the non-zero value from the input grid.

**YAML Block - Facts:**


```yaml
facts:
  - observation: Input is a 3x3 grid.
  - observation: Output is a 1x1 grid.
  - object: input_grid
    type: grid
    dimensions: 3x3
    elements: integers
    properties:
      - majority_value: 0 (white)
      - non_zero_values: [7]
  - object: output_grid
    type: grid
    dimensions: 1x1
    elements: integers
    properties:
      - value: 7 (orange)
  - action: extract_non_zero
    description: Identify and extract the non-zero value from the input grid.
  - relationship: output_value equals non_zero_value in input_grid
```


**Natural Language Program:**

1.  Examine the input grid.
2.  Identify the single cell containing value different than 0.
3.  Create output grid equal the value in the cell.

In simple word. Find the non-zero value in the input grid and create the output containing this value.

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
