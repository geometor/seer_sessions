# d037b0a7 • 008 • example_2 • investigate_coder

---

## Example 2

**input:**
```
0 2 0
7 0 8
0 0 0
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x71BF73EB5DB0>

**output:**
```
0 2 0
7 2 8
7 2 8
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x71BF740D65D0>
Okay, here's my analysis of the provided example, formatted as a report:

**Perception of Elements:**

The task involves a 3x3 grid of single-digit integers (0-9), representing different colors. The transformation seems to involve replicating a part of the grid. Specifically, the middle row of the input grid appears to be copied to the bottom row in the output grid. The top row remains unchanged. The colors in the copied row are maintained.

**YAML Fact Block:**


```yaml
facts:
  - type: grid
    dimensions: 3x3
    elements: single_digit integers (0-9)
    element_interpretation: colors
  - observation: row_replication
    source_row: 1  # Indexing starts from 0
    destination_row: 2
    description: The middle row is copied to the bottom row.
  - observation: row_preservation
    source_row: 0
    description: top row is unchanged
```


**Natural Language Program:**

1.  **Identify** the input grid as a 3x3 matrix of color values.
2.  **Preserve** the top row (row index 0) of the grid, it is not modified
3.  **Copy** the entire middle row (row index 1) of the input grid.
4.  **Replace** the contents of the bottom row (row index 2) of the grid with the copied middle row.
5.  **Output** the modified grid.

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
