# 3af2c5a8 • 010 • example_2 • investigate_coder

---

## train_2

**input:**
```
0 0 3 3
0 3 0 3
3 3 3 0
```

<PIL.Image.Image image mode=RGB size=256x192 at 0x78E5F21D04D0>

**output:**
```
0 0 3 3 3 3 0 0
0 3 0 3 3 0 3 0
3 3 3 0 0 3 3 3
3 3 3 0 0 3 3 3
0 3 0 3 3 0 3 0
0 0 3 3 3 3 0 0
```

<PIL.Image.Image image mode=RGB size=512x384 at 0x78E5F21D3A50>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves a transformation of a smaller grid (input) into a larger grid (output). The grids contain two colors: white (0) and green (3). The output grid appears to be an expansion of the input grid, with a specific pattern of replication and insertion of rows and columns. The core object are colored blocks.

**YAML Block (Facts):**


```yaml
objects:
  - name: input_grid
    type: grid
    properties:
      - colors: [white, green]
      - dimensions: [3x4]
  - name: output_grid
    type: grid
    properties:
      - colors: [white, green]
      - dimensions: [6x8]

actions:
  - name: expand
    type: transformation
    description: Expands the input grid into the output grid.
    details: >
      Rows and columns are replicated and added to the output. The way it is done
      is that the input is replicated, rotated, and then placed into the output
      to created the checkerboard and frame.

relationships:
  - type: input_to_output
    relation: input_grid is transformed into output_grid by the 'expand' action.
  - type: dimensions
    relation: output grid is double in height compared to input and, is also double in width.
```


**Natural Language Program:**

1.  **Identify the input grid:** A 3x4 grid with white (0) and green (3) pixels.
2.  **Double dimensions**: make the output height = input x 2. make output width = input width x 2
3.  **Replicate input**: each row and column will become two of the same in the output.
4. **Frame it.** The input is replicated, but it is framed by the inverse.
5. **Checkerboard.** The replication of the input and addition of the inverse results in a checker board appearance.


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
