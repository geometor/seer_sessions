# ba97ae07 • 022 • example_4 • investigate_coder

---

## train_4

**input:**
```
0 3 0 0 0 0
0 3 0 0 0 0
0 3 0 0 0 0
0 3 0 0 0 0
2 3 2 2 2 2
0 3 0 0 0 0
0 3 0 0 0 0
0 3 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=384x512 at 0x7FC253D5D850>

**output:**
```
0 3 0 0 0 0
0 3 0 0 0 0
0 3 0 0 0 0
0 3 0 0 0 0
2 2 2 2 2 2
0 3 0 0 0 0
0 3 0 0 0 0
0 3 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=384x512 at 0x7FC253D5CAD0>
Okay, here's my analysis of the provided input-output pair:

**Perception of Elements:**

The task involves a grid of single-digit integers, representing colors. The primary colors observed are green (3), white (0), and red (2).  The input grid appears to have a vertical line of green (3) and a horizontal line intersecting, with red (2) in it. The transformation seems to focus on the horizontal line of red pixels.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    properties:
      dimensions: 8x6 (rows x columns)
      colors: [0, 2, 3] # white, red, green
  - type: line
    properties:
      orientation: vertical
      color: 3 # green
      column: 1
  - type: line
    properties:
       orientation: horizontal
       color: 2
       row: 4
       
actions:
  - type: remove_color
    target: line
    color: 3 #green
    orientation: horizontal
    
relationships:
   - type: intersection
     objects: [vertical line, horizontal line]

```


**Natural Language Program:**

1.  **Identify Objects:** Locate the vertical green line and the horizontal red line.
2.  **Locate Intersection** The point where they meet.
3.  **Apply Rule** Keep all pixels of horizontal line except pixels with color code 3.

In simpler, terms eliminate all values of '3' in the horizontal intersecting line, while not changing the color of any pixel in the vertical line.

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
