# 444801d8 • 010 • example_2 • investigate_coder

---

## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 1 1 0 1 1 0 0 0 0
0 1 0 2 0 1 0 0 0 0
0 1 0 0 0 1 0 0 0 0
0 1 1 1 1 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 1 0 1 1 0
0 0 0 0 1 0 3 0 1 0
0 0 0 0 1 1 1 1 1 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x78E5F214A150>

**output:**
```
0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 0 0 0 0
0 1 1 2 1 1 0 0 0 0
0 1 2 2 2 1 0 0 0 0
0 1 2 2 2 1 0 0 0 0
0 1 1 1 1 1 0 0 0 0
0 0 0 0 3 3 3 3 3 0
0 0 0 0 1 1 3 1 1 0
0 0 0 0 1 3 3 3 1 0
0 0 0 0 1 1 1 1 1 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x78E5F214A550>
Okay, here's my analysis of the provided input-output pair:

**Perception of Elements:**

The task involves two grids of colored pixels. The primary colors involved appear to be blue (1), red (2), and green (3), with white (0) as the background. It seems that existing colored regions in the input are being modified, specifically it looks like the red replaces an existing non-blue, non-background color and expands. The colors are all connected.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    properties:
      - colors: [white, blue, red, green]
      - dimensions: 10x10
  - type: colored_region
    properties:
      - color: blue
        shape: irregular
      - color: red
        shape: irregular
      - color: green
        shape: irregular
  
actions:
 - type: replacement
   description: One color replaces another color
   details: The color red will replace any color on the top blue object. While Green replaces colors on the bottom blue object.

relationships:
    - type: adjacency
      description: Colors are adjacent to other color and to the background

```


**Natural Language Program:**

1.  **Identify Regions:** Locate the blue regions within the input grid.
2.  **Top Blue Object**: On the topmost blue object, check for any red pixels. Replace all colors on the blue object, except the blue, with the color red.
3. **Bottom Blue Object**: On the bottommost blue object, check for any green pixels. Replace all colors on the blue object, except the blue, with the color green.
4.  **Background:** The white background (0) remains unchanged.

Essentially, on the topmost blue color, the red fills, while on the bottommost blue color, the green fills.

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
