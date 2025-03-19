# 7447852a • 008 • example_2 • investigate_coder

---

## Example 2

**input:**
```
2 0 0 0 2 0 0 0 2 0 0 0 2 0 0
0 2 0 2 0 2 0 2 0 2 0 2 0 2 0
0 0 2 0 0 0 2 0 0 0 2 0 0 0 2
```

<PIL.Image.Image image mode=RGB size=960x192 at 0x777851601BD0>

**output:**
```
2 0 0 0 2 4 4 4 2 0 0 0 2 0 0
4 2 0 2 0 2 4 2 0 2 0 2 4 2 0
4 4 2 0 0 0 2 0 0 0 2 4 4 4 2
```

<PIL.Image.Image image mode=RGB size=960x192 at 0x777851601DB0>
Okay, here's my analysis of the provided example, formatted as a report:

**Perception of Elements:**

The task involves a grid of colored pixels. The primary colors observed are red (2) and white (0). The transformation introduces a new color, yellow (4). The yellow color appears to be related to the position of the red pixels. The overall grid dimensions remain constant between input and output.

**YAML Block (Facts):**


```yaml
objects:
  - type: pixel
    properties:
      color:
        - white (0)
        - red (2)
        - yellow (4)
      position:
        row: [0, 1, 2]  # Row index
        col: [0-14]   # Column index

actions:
  - name: introduce_yellow
    condition: adjacent to red pixels
    parameters: none

relationships:
  - type: adjacency
    relation:
        - horizontal
        - vertical
    between: [red, yellow]
```


**Natural Language Program:**

1.  **Identify Red Pixels:** Locate all pixels with the color red (value 2) in the input grid.

2.  **Horizontal Adjacency Check (Left/Right):** For each red pixel, check if it has a horizontally adjacent white pixel (value 0).

    *   If there is a white pixel adjacent to the red pixel to its right, change the white box to its right to yellow.
    *   If there is a white pixel adjacent to the red pixel to its left, change the white box to its left to yellow.

3.  **Vertical Adjacency Check (Above/Below** For each red pixel, check if it has a vertically adjacent white pixel (value 0)

    *   If there is a white pixel adjacent to the red pixel above it, change the white box above it to yellow
    *   If there is a white pixel adjacent to the red pixel below it, change the white box below it to yellow.

4. **Diagonal Adjacency Check:** If there are white pixels diagonal to any red pixel do NOT change it to yellow.
5.  **Preserve Other Pixels:** All other pixels that are not horizontally or vertically adjacent to a red pixel remain unchanged.
6.  **Output:** The resulting grid is the output, containing red, white, and yellow pixels based on the adjacency rule.

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
