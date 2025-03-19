# 6e02f1e3 • 020 • example_4 • investigate_coder

---

## Example 4

**input:**
```
3 3 3
3 3 3
3 3 3
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x7DCBFF213340>

**output:**
```
5 5 5
0 0 0
0 0 0
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x7DCBFF212680>
Okay, here's my analysis of the example input-output pair, formatted as a report:

**Perception of Elements:**

The task involves a transformation of a 2D grid of single-digit integers (representing colors) into another 2D grid of the same dimensions. The input grid consists entirely of the number 3 (green). The output grid has the top row changed to 5 (gray) and the other two rows changed to 0 (white).

**YAML Block (Facts):**


```yaml
facts:
  - object: input_grid
    type: 2D array
    dimensions: 3x3
    elements:
      type: integer
      values: [3]
  - object: output_grid
    type: 2D array
    dimensions: 3x3
    elements:
      type: integer
      values: [0, 5]
  - relationship: row_transformation
    input: input_grid.row[0]
    output: output_grid.row[0]
    transformation: change_all_values(3, 5)
  - relationship: row_transformation
    input: input_grid.row[1:]
    output: output_grid.row[1:]
    transformation: change_all_values(3,0)

```


**Natural Language Program:**

1.  **Identify the input grid:** A 3x3 grid filled with the value 3 (green).
2.  **Transform the first row:** Change all values in the first row of the input grid from 3 to 5 (green to gray).
3.  **Transform the remaining rows**: Change all the values of the other two rows to 0 (white).
4.  **Construct the output grid:** Create a new 3x3 grid with the transformed rows.

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
