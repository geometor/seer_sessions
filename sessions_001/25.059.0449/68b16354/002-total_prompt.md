# 68b16354 • 002 • example_3 • investigate_coder

---

## train_1

**input:**
```
8 1 2 1 4
4 4 2 4 8
3 7 2 4 8
2 7 7 8 7
8 7 7 4 8
```

<PIL.Image.Image image mode=RGB size=320x320 at 0x744068D7A150>

**output:**
```
8 7 7 4 8
2 7 7 8 7
3 7 2 4 8
4 4 2 4 8
8 1 2 1 4
```

<PIL.Image.Image image mode=RGB size=320x320 at 0x744068D7A7D0>

## train_2

**input:**
```
7 3 3 1 2
1 8 2 4 1
2 7 8 7 2
7 7 4 1 8
8 1 7 7 1
```

<PIL.Image.Image image mode=RGB size=320x320 at 0x744068D7AAD0>

**output:**
```
8 1 7 7 1
7 7 4 1 8
2 7 8 7 2
1 8 2 4 1
7 3 3 1 2
```

<PIL.Image.Image image mode=RGB size=320x320 at 0x744068D79FD0>

## train_3

**input:**
```
2 7 4 3 4 8 3
2 3 7 1 2 3 3
8 7 4 3 2 2 4
1 1 2 1 4 4 7
2 4 3 1 1 4 1
4 8 7 4 4 8 2
7 3 8 4 3 2 8
```

<PIL.Image.Image image mode=RGB size=448x448 at 0x744068D7A8D0>

**output:**
```
7 3 8 4 3 2 8
4 8 7 4 4 8 2
2 4 3 1 1 4 1
1 1 2 1 4 4 7
8 7 4 3 2 2 4
2 3 7 1 2 3 3
2 7 4 3 4 8 3
```

<PIL.Image.Image image mode=RGB size=448x448 at 0x744068D7A6D0>
<PIL.Image.Image image mode=RGB size=1168x946 at 0x744068E7F250>Okay, I've reviewed the provided input-output pairs. Here's my analysis:

**Perception of Elements:**

The task involves 2D grids of single-digit integers, where each integer represents a color. The transformation appears to be a spatial manipulation of the grid rather than a change in the colors themselves. The size of grids also appear to be the same. It seems like simple row reversal.

**Facts (YAML):**


```yaml
task_type: grid_transformation
transformation_type: spatial
objects:
  - type: grid
    properties:
      - dimensions: rows x columns
      - elements: integers (representing colors)
actions:
  - name: reverse_rows
    description: The order of rows in the grid is reversed.
relationships:
  - input_grid is transformed to output_grid by reversing_rows
```


**Natural Language Program:**

The transformation rule is to reverse the order of the rows in the input grid. The first row becomes the last, the second row becomes the second-to-last, and so on, until the last row becomes the first. The columns are kept the same.

Essentially, the output grid is a vertically flipped version of the input grid.

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
