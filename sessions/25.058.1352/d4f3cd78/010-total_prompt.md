# d4f3cd78 • 010 • example_2 • investigate_coder

---

## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 0 5 5 0 0
0 0 5 0 0 0 0 5 0 0
0 0 5 0 0 0 0 5 0 0
0 0 5 0 0 0 0 5 0 0
0 0 5 5 5 5 5 5 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7ACD213836B0>

**output:**
```
0 0 0 0 0 8 0 0 0 0
0 0 0 0 0 8 0 0 0 0
0 0 0 0 0 8 0 0 0 0
0 0 0 0 0 8 0 0 0 0
0 0 0 0 0 8 0 0 0 0
0 0 5 5 5 8 5 5 0 0
0 0 5 8 8 8 8 5 0 0
0 0 5 8 8 8 8 5 0 0
0 0 5 8 8 8 8 5 0 0
0 0 5 5 5 5 5 5 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7ACD21383430>
Okay, let's analyze this input-output pair.

**Perception of Elements:**

*   The input is a 10x10 grid of pixels, mostly white (0) with a gray (5) shape in the bottom half.
*   The output is the same 10x10 grid, but with some changes:
    *   A vertical azure (8) line has been added in the middle, extending upwards from the top of the gray shape.
    *   The interior of the gray shape directly below azure line are now also azure.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    dimensions: 10x10
    elements: pixels
    
  - type: shape
    color: gray (5)
    location: bottom half of grid
    description: irregular, possibly an outline

  - type: line
    color: azure (8)
    location: vertical, center
    description: extends from top of gray shape to top of grid

  - type: filled_area
    color: azure (8)
    location: within gray shape, directly below azure line
    description: replaces grey pixels
```


**Natural Language Program:**

1.  **Identify** the existing gray (5) shape in the input grid.
2.  **Find** the horizontal center of the grid.
3.  **Draw** a vertical line of azure (8) pixels, starting from the top edge of the gray shape, extending upwards to the top edge of the grid, aligned with the horizontal center.
4. **Identify** the top row of the grey object.
5. **Fill** with azure(8) any gray(5) pixels inside the shape that are directly below any azure(8) pixels.

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
