# d631b094 • 008 • example_2 • investigate_coder

---

## Example 2

**input:**
```
0 2 0
2 0 0
0 2 0
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x7DCBFF5DB6D0>

**output:**
```
2 2 2
```

<PIL.Image.Image image mode=RGB size=192x64 at 0x7DCBFF5DA410>
Okay, here's my analysis of the provided example, formatted as a report:

**Perception of Task Elements:**

*   **Input:** A 3x3 grid with cells containing either '0' (white) or '2' (red).
*   **Output:** A 1x3 grid (one row, three columns) where all cells are '2' (red).
*   The core transformation appears to involve extracting the color '2' (red) from the input grid and reconstructing it into a single row in the output.

**YAML Fact Block:**


```yaml
facts:
  - object: input_grid
    type: grid
    dimensions: 3x3
    elements:
      - value: 0
        color: white
      - value: 2
        color: red
  - object: output_grid
    type: grid
    dimensions: 1x3
    elements:
      - value: 2
        color: red
  - action: extract
    source: input_grid
    target: output_grid
    property: color
    value: 2
  - action: reconstruct
    dimensions: 1x3
    value: 2
```


**Natural Language Program:**

1.  **Scan** the input grid.
2.  **Identify** all cells with the value '2' (red).
3.  **Extract** the red color.
4. **Construct** the output as a new grid with the extracted value and grid dimensions is 1x3.

In simpler terms, the program finds all red cells in the input and creates a 1x3 output grid filled with red cells.

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
