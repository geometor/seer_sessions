# fcc82909 • 004 • example_1 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 9 9 0 0 0 0 0 0 0
0 6 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 4 0 0 0
0 0 0 0 0 7 7 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x716635BBB250>

**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 9 9 0 0 0 0 0 0 0
0 6 6 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0
0 3 3 0 0 8 4 0 0 0
0 0 0 0 0 7 7 0 0 0
0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 3 3 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x716635BBB350>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves a grid of colored pixels. The input grid contains several distinct colored regions (objects). The output grid seems to modify some of these regions, specifically by adding or expanding some colored areas based on existing ones. The background color is white (0).

**YAML Block (Facts):**


```yaml
objects:
  - type: region
    properties:
      color: [9, 6, 8, 4, 7]  # Distinct colors present in the input
      shape: irregular # Shapes are not predefined geometric forms
      size: variable  # The number of pixels in each region varies.
    relations:
      adjacent: true # Regions of different colors can be adjacent.
  - type: background
    properties:
      color: 0 # White
      shape: rectangle
      size: 10x10
    
actions:
 - type: expansion
   target:
     color: 6
     direction: down
   result:
     new_color: 3
 - type: expansion
   target:
     color: 9
     direction: down
   result:
     new_color: 3
 - type: expansion
   target:
     color: 7
     direction: up
   result:
     new_color: 3
```


**Natural Language Program:**

1.  **Identify Regions:** Locate all distinct colored regions in the input grid. Note their colors and positions.
2.  **Conditional Expansion:** For every pixel that compose the lower edge of a *maroon* or a *magenta* object: add a new object below of the green color that fills the width of the original object, and has height=3. For every pixel that compose the upper edge of an *orange* object: add a new object above with color green, and height=3, and the same width as the initial object.
3. **Other Objects:** Any other objects in the input remain in the same place and retain color and shape.


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
