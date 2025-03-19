# 8be77c9e • 002 • example_3 • investigate_coder

---

## train_1

**input:**
```
1 1 0
1 1 1
0 0 0
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x7F2DF67FDAD0>

**output:**
```
1 1 0
1 1 1
0 0 0
0 0 0
1 1 1
1 1 0
```

<PIL.Image.Image image mode=RGB size=192x384 at 0x7F2DF78BFAD0>

## train_2

**input:**
```
0 0 0
1 0 1
1 1 0
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x7F2DF78BF6D0>

**output:**
```
0 0 0
1 0 1
1 1 0
1 1 0
1 0 1
0 0 0
```

<PIL.Image.Image image mode=RGB size=192x384 at 0x7F2DF78BF350>

## train_3

**input:**
```
0 0 0
0 0 1
0 0 1
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x7F2DF78BF2D0>

**output:**
```
0 0 0
0 0 1
0 0 1
0 0 1
0 0 1
0 0 0
```

<PIL.Image.Image image mode=RGB size=192x384 at 0x7F2DF78BF650>
<PIL.Image.Image image mode=RGB size=704x656 at 0x7F2DF7900B50>Okay, let's analyze the provided input-output pairs to discern the transformation rule.

**Perception of Elements:**

The task involves 2D grids (likely represented as matrices) where each cell contains a single digit integer (0 or 1), representing colors (0: white, 1: blue). The transformation seems to involve an expansion of the input grid, replicating the original input pattern in a specific way. The output grids are always larger than the input grids, specifically, they appear to be mirrored copies.

**Facts (YAML):**


```yaml
objects:
  - name: input_grid
    type: 2D array
    properties:
      - values: [0, 1]
      - shape: (rows, cols)

  - name: output_grid
    type: 2D array
    properties:
      - values: [0, 1]
      - shape: (rows', cols')

actions:
  - name: replicate
    description: The input grid is copied.
  - name: reflect
    description: The input grid is mirrored, creating the output_grid.
    parameters:
      - axis: vertical (across rows)

relationships:
  - type: transformation
    from: input_grid
    to: output_grid
    via: [replicate, reflect]
```


**Natural Language Program:**

1. **Copy** the input grid.
2. **Reflect** the input grid vertically (across the horizontal midline).
3. The output grid consists of the original grid on the top and the reflected version appended below.

In essence, the transformation rule is a vertical reflection of the input grid. The output is the original grid with its vertically mirrored copy appended below it.

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
