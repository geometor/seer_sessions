# db3e9e38 • 002 • example_1 • investigate_coder

---

## Example 1

**input:**
```
0 0 0 7 0 0 0
0 0 0 7 0 0 0
0 0 0 7 0 0 0
0 0 0 7 0 0 0
0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=448x320 at 0x76911EE1F750>

**output:**
```
8 7 8 7 8 7 8
0 7 8 7 8 7 0
0 0 8 7 8 0 0
0 0 0 7 0 0 0
0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=448x320 at 0x76911EB26490>
Okay, here's my analysis of the provided example, formatted as a report:

**Perception of Elements:**

The task involves a transformation of a grid of colored pixels. The input grid contains a vertical line of orange (7) pixels in the center. The output grid introduces azure (8) pixels surrounding the orange (7) pixels, forming a sort of "thickened" or "outlined" version of the original line, but with an interesting wrapping/extension. The white (0) background is mostly preserved, but it gets overwritten by the new azure pixels.

**YAML Block - Facts:**


```yaml
objects:
  - type: grid
    properties:
      dimensions: [5, 7] # [height, width]
      colors: [0, 7, 8] # white, orange, azure
    elements:
      - type: pixel
        properties:
          color: int
          position: [row, col]

  - type: line
    properties:
      color: 7 # orange
      orientation: vertical
      start: [0, 3] # row, col
      end: [3, 3]

actions:
  - type: surround
    object: line
    properties:
       with_color: 8   #azure
       original_color: 7 #orange

relationships:
  - type: adjacency
    description: azure pixels are placed adjacent to orange pixels.
  - type: containment
    description: output grid contains the transformed line.
```


**Natural Language Program:**

1.  **Identify the Object:** Locate the vertical line of orange (7) pixels in the input grid.
2.  **Surround with Azure:** For each orange (7) pixel:
     a. Change any directly adjacent pixels, that are up, down, left, right, or diagonal, to azure (8).
3. **Wrap around:** If the original object touches the edge of the grid, extend the surrounding color to the opposite side.


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
