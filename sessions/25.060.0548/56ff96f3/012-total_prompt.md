# 56ff96f3 • 012 • example_2 • investigate_coder

---

## train_2

**input:**
```
0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7
0 0 3 0 7 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=512x448 at 0x7B4C05BB91D0>

**output:**
```
0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0
0 3 3 0 0 0 0 0
0 3 3 0 7 7 7 7
0 3 3 0 7 7 7 7
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=512x448 at 0x7B4C05BB8ED0>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves a grid of colored pixels. The input grid contains sparse pixels of green (3) and orange (7), with the rest being white (0). The output grid shows an expansion of these colored regions. The green (3) expands downwards and the Orange (7) expands rightwards.

**YAML Block - Facts:**


```yaml
objects:
  - id: green_region
    color: green (3)
    initial_position: row 1, column 1
    shape: single pixel
    action: expand downwards
  - id: orange_region
    color: orange (7)
    initial_position: row 3, column 4
    shape: single pixel
    action: expand rightwards
  - id: background
    color: white (0)
    shape: fills the remaining grid

relationships:
  - green_region expands until encountering white edge.
  - Orange_region expands until it encounters white edge.
  - expansion fills connected areas.
```


**Natural Language Program:**

1.  **Identify Objects:** Find all pixels with colors other than white (0). These are the seed pixels for object regions. In the example, we find a green (3) pixel and an orange (7) pixel.
2.  **Green Expansion:** For the green pixel extend a vertical filled line straight down.
3.  **Orange Expansion:** For the orange pixel extend a horizontal filled line to the right.
4.  **Fill to Edge**: Both expansions continue until reaching the bottom of input matrix and right edge.


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
