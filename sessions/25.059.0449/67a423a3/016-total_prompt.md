# 67a423a3 • 016 • example_3 • investigate_coder

---

## train_3

**input:**
```
0 0 1 0 0 0
0 0 1 0 0 0
9 9 1 9 9 9
0 0 1 0 0 0
0 0 1 0 0 0
0 0 1 0 0 0
```

<PIL.Image.Image image mode=RGB size=384x384 at 0x744068D7A150>

**output:**
```
0 0 1 0 0 0
0 4 4 4 0 0
9 4 1 4 9 9
0 4 4 4 0 0
0 0 1 0 0 0
0 0 1 0 0 0
```

<PIL.Image.Image image mode=RGB size=384x384 at 0x744070736B50>
Okay, here's my analysis of the provided input-output example pair.

**Perception of Elements:**

The task involves a grid of colored pixels. The primary colors involved are blue (1), maroon/dark red (9), and white (0). In the output, yellow (4) appears. The transformation seems to involve a change in color surrounding the blue (1) pixels. Specifically, it appears some white (0) pixels and some maroon (9) pixels adjacent to blue are changed to yellow.

**YAML Block (Facts):**


```yaml
objects:
  - type: pixel
    properties:
      color:
        - white (0)
        - blue (1)
        - maroon (9)
        - yellow (4)
      position: [row, column]
actions:
  - type: color_change
    target: pixel
    from: [white, maroon]
    to: yellow
    condition: adjacent to blue
relationships:
  - type: adjacency
    description: Pixels are considered adjacent if they share a side (not diagonal).
```


**Natural Language Program:**

1.  **Identify** all blue (1) pixels in the input grid.
2.  **Locate** all pixels that are directly adjacent (up, down, left, or right, but not diagonally) to the blue pixels.
3.  **Change** the color of any adjacent pixels from white (0) or maroon (9) to yellow (4).
4.  **Preserve** the color of the blue pixels and any other pixel not described above.
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
