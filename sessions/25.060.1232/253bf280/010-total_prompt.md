# 253bf280 • 010 • example_2 • investigate_coder

---

## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 0 0
0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=704x640 at 0x7CE41B95CDD0>

**output:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 3 0 0 0 8 0 0
0 0 0 0 3 0 0 0 3 0 0
0 0 0 0 3 0 0 0 3 0 0
0 0 0 0 3 0 0 0 3 0 0
0 0 0 0 3 0 0 0 8 0 0
0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=704x640 at 0x7CE41B95F850>
Okay, here's my analysis of the provided input-output example, focusing on perception, object identification, and the transformation rule.

**Perception of Elements:**

*   The input and output are grids of digits, representing colored pixels.
*   The primary colors involved are white (0), azure (8), and green (3).
*   The azure pixels in the input seem to trigger the appearance of green pixels in the output.
*    The shape is a mirrored, rotated, L.

**YAML Block (Facts):**


```yaml
objects:
  - type: pixel
    properties:
      color: [white, azure, green]
      position: [row, column]
  - type: shape
    properties:
      color: azure
      form: L
      position: [row, column]

actions:
  - type: copy
    properties:
    agent: azure pixel
    target: azure pixel

  - type: extend
    properties:
      agent: azure pixel
      color: green
      direction: [vertical]
      length: 4

relationships:
  - type: spatial
    relation: adjacent
    objects: [azure pixel, green pixel]
```


**Natural Language Program:**

1.  **Identify Azure Pixels:** Locate all pixels with the value 8 (azure) in the input grid.
2.  **Copy Azure Pixels:** Maintain any azure pixel from input to output.
3.  **Vertical Extension (Green):** For each azure pixel:
    *   If it is not on the edge, create a vertical line of green (3) pixels extending upwards and downwards.
    *   The green line should consist of four pixels total.
    *   Specifically, two green (3) pixels, up and down, adjacent, from an azure (8) pixel.

In summary, the transformation involves copying the azure pixels and creating a 4-pixel-long vertical green line centered on *some* azure pixels. The azure pixels at either end of the L shape are the exceptions, they do not sprout green pixels.

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
