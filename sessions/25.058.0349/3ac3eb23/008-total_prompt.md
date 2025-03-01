# 3ac3eb23 • 008 • example_2 • investigate_coder

---

## Example 2

**input:**
```
0 4 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=448x384 at 0x76911E9AF750>

**output:**
```
0 4 0 0 0 0 0
4 0 4 0 0 0 0
0 4 0 0 0 0 0
4 0 4 0 0 0 0
0 4 0 0 0 0 0
4 0 4 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=448x384 at 0x76911E9AE210>
Okay, let's analyze this example and break down the transformation.

**Perception of Elements:**

*   **Input Grid:** A 6x7 grid with mostly '0' (white) pixels and a single '4' (yellow) pixel in the top row.
*   **Output Grid:** A 6x7 grid with a vertical, alternating pattern of '4' (yellow) and '0' (white) pixels, originating from where the yellow pixel was in the input and mirroring 4 on it's immediate right neighbor .
*   **Transformation:** The single yellow pixel seems to trigger a vertical "stripe" pattern, alternating yellow and white, downwards. The yellow is mirrored on its neighbor.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    dimensions: [6, 7]
    elements:
      - value: 0
        color: white
      - value: 4
        color: yellow
    properties:
        - static # input grid appears unchanged

  - type: grid
    dimensions: [6, 7]
    elements:
      - value: 0
        color: white
      - value: 4
        color: yellow
    properties:
        - dynamic # output grid is generated

actions:
  - type: propagate
    trigger:
      object: pixel
      value: 4
      color: yellow
    direction: vertical_down
    pattern: alternate
    values: [4,0]
  - type: mirror
    trigger:
      object: pixel
      value: 4
      color: yellow
    direction: right
    pattern: once

relationships:
  - type: spatial
    between: [input_grid, output_grid]
    description: output_grid is generated from input_grid based on location of a specific element
```


**Natural Language Program:**

1.  **Locate:** Find the single yellow (4) pixel in the input grid.
2. **Mirror:** From the found position, copy it on the immediate right neighbor, if the neighbor is 0.
3.  **Propagate:** From the found position, draw a vertical line downwards to the bottom of the grid.
4.  **Alternate:** The vertical line alternates between yellow (4) and white (0) pixels.
5. Mirror: From each newly generated pixel, copy it on the immediate right neighbor, if neighbor is 0.
6. all other are unchanged.


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
