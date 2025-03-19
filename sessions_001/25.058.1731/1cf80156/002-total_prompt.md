# 1cf80156 • 002 • example_3 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 2 2 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0
0 0 0 2 2 2 0 0 0 0 0 0
0 0 0 2 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=768x640 at 0x7C36039E5ED0>

**output:**
```
0 2 2 2
0 0 2 0
2 2 2 0
2 0 2 0
```

<PIL.Image.Image image mode=RGB size=256x256 at 0x7C36039E6250>

## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 0 0 0
0 0 1 1 0 0 0 0 0 0 0 0
0 0 0 1 0 0 0 0 0 0 0 0
0 0 1 1 1 0 0 0 0 0 0 0
0 0 0 0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=768x704 at 0x7C36039E4AD0>

**output:**
```
1 0 0
1 1 0
0 1 0
1 1 1
0 0 1
```

<PIL.Image.Image image mode=RGB size=192x320 at 0x7C36039E5650>

## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 8 0 0 0 0 0
0 0 0 8 8 8 8 0 0 0 0 0
0 0 0 0 0 0 8 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=768x768 at 0x7C36039E58D0>

**output:**
```
0 8 0 8 0
8 8 8 8 0
0 0 0 8 8
```

<PIL.Image.Image image mode=RGB size=320x192 at 0x7C36039E61D0>
<PIL.Image.Image image mode=RGB size=2384x1138 at 0x7C360BFEA3D0>Okay, let's analyze the provided examples to understand the transformation rule.

**Perception of Elements:**

The task involves 2D grids as input and output. The grids contain single-digit integers representing different colors. The input grids are larger (12x10 or 12x11) and contain a single connected shape/object of a non-zero color, surrounded by zeros. The output grids are smaller and appear to be a cropped, potentially rotated, version of the input grid, containing only the non-zero colored object.

**YAML Block - Facts:**


```yaml
objects:
  - name: input_grid
    type: 2D array
    properties:
      - dimensions: 12 x (10 or 11)
      - values: integers (0-9)
  - name: output_grid
    type: 2D array
    properties:
      - dimensions: variable, smaller than input_grid
      - values: integers (0-9)
  - name: colored_object
    type: connected component
    properties:
       - color: non-zero integer
       - shape: irregular

actions:
  - name: extract_object
    description: Isolates the non-zero colored object from the input grid.
  - name: crop
    description: Removes the surrounding zeros to create a minimal bounding box around the object
  - name: rotate
    description: possible rotation

relationships:
  - input_grid contains colored_object
  - output_grid is a transformed version of colored_object
```


**Natural Language Program:**

1. **Identify the colored object:** Locate the contiguous block of non-zero pixels within the input grid. This defines the region of interest.
2. **Extract the bounding box:** Determine the minimum and maximum row and column indices that enclose the colored object. This defines a rectangular subgrid.
3. **Create the output grid** Create new grid from the bounding box.

Let's walk through the examples and make sure the natural language steps are correct.

example 1
input

```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 2 2 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0
0 0 0 2 2 2 0 0 0 0 0 0
0 0 0 2 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

output

```
0 2 2 2
0 0 2 0
2 2 2 0
2 0 2 0
```


example 2
input

```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 0 0 0
0 0 1 1 0 0 0 0 0 0 0 0
0 0 0 1 0 0 0 0 0 0 0 0
0 0 1 1 1 0 0 0 0 0 0 0
0 0 0 0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

output

```
1 0 0
1 1 0
0 1 0
1 1 1
0 0 1
```

example 3
input

```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 8 0 0 0 0 0
0 0 0 8 8 8 8 0 0 0 0 0
0 0 0 0 0 0 8 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

output

```
0 8 0 8 0
8 8 8 8 0
0 0 0 8 8
```
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
