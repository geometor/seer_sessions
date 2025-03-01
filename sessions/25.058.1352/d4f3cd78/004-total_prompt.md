# d4f3cd78 • 004 • example_1 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 5 5 0 0
0 0 5 0 0 0 0 5 0 0
0 0 5 0 0 0 0 5 0 0
0 0 5 0 0 0 0 5 0 0
0 0 5 0 0 0 0 5 0 0
0 0 5 5 5 0 5 5 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7ACD2131A350>

**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 5 5 0 0
0 0 5 8 8 8 8 5 0 0
0 0 5 8 8 8 8 5 0 0
0 0 5 8 8 8 8 5 0 0
0 0 5 8 8 8 8 5 0 0
0 0 5 5 5 8 5 5 0 0
0 0 0 0 0 8 0 0 0 0
0 0 0 0 0 8 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7ACD2131A0D0>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves a 2D grid (matrix) of single-digit integers, representing colors. The primary object is a hollow square made of gray (5) pixels. The transformation fills the interior of the square with azure (8) pixels. The transformation also includes the color change of "0" into "8" in last two rows.

**YAML Block (Facts):**


```yaml
objects:
  - type: square
    color: gray (5)
    property: hollow
    location: centered in the grid
  - type: background
    color: white (0)
  - type: fill
    color: azure (8)

actions:
  - type: fill
    target: interior of the square
    color: azure (8)
  - type: replace
    target: two last rows
    find: white(0)
    replace_with: azure(8)

relationships:
  - square: encloses interior space
  - fill: occupies interior space
  - two last rows: position absolute.
```


**Natural Language Program:**

1.  **Identify** a hollow square object formed by gray (5) pixels within the grid.
2.  **Fill** the interior region of the identified square with azure (8) pixels.
3. **Locate** the last two rows.
4. **Change** the color value of white(0) into azure(8) in the last two rows.

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
