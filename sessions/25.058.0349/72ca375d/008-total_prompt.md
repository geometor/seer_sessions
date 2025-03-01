# 72ca375d • 008 • example_2 • investigate_coder

---

## Example 2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 4 4 0 0 0 0 0 0
0 0 4 4 0 0 8 8 8 0
0 0 0 0 0 0 8 0 8 8
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x76911E9AEB70>

**output:**
```
4 4
4 4
```

<PIL.Image.Image image mode=RGB size=128x128 at 0x76911E973930>
Okay, here's my analysis of the provided example, formatted as a report:

**Perception of Elements:**

The task involves transforming a grid of colored pixels (represented by numbers 0-9) into a smaller grid. The input grid contains several distinct colored regions (yellow, azure, and red), while the output grid consists of only one colored region (yellow). The spatial arrangement of the colored regions in the input seems crucial. The output appears to isolate a particular object based on color and possibly shape.

**YAML Fact Block:**


```yaml
facts:
  - object: yellow_square
    type: rectangle
    color: yellow
    properties:
      - size: 2x2
      - location: top_left_quadrant
    input_grid:
      rows: 10
      columns: 10
      pixels:
        - value: 0-9
          color: 0=white, 1=blue, 2=red, 3=green, 4=yellow, 5=gray, 6=magenta, 7=orange, 8=azure, 9=maroon
  - action: extract
    target: yellow_square
    result: output_grid
  - object: azure_region
    type: irregular
    color: azure
    properties:
      - size: variable
      - location: adjacent_to yellow_square
    input_grid_presence: true
    output_grid_presence: false
  - object: red_region
    type: rectangle
    color: red
    properties:
      - size: variable
      - location: bottom_quadrant
    input_grid_presence: true
    output_grid_presence: false
  - output_grid:
      rows: 2
      columns: 2

```


**Natural Language Program:**

1.  **Identify** the 2x2 yellow square object in the input grid.
2.  **Extract** the 2x2 yellow square object.
3.  The extracted square object **becomes** the output grid. All other regions are discarded.

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
