# 673ef223 • 016 • example_3 • investigate_coder

---

## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2
0 0 0 0 0 0 8 0 0 2
0 0 8 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 2
0 0 0 0 8 0 0 0 0 2
0 0 0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x1280 at 0x744068D7A550>

**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2
0 0 0 0 0 0 4 8 8 2
0 0 4 8 8 8 8 8 8 2
0 0 0 0 0 0 0 0 0 2
0 0 0 0 4 8 8 8 8 2
0 0 0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0
2 8 8 8 8 8 8 8 8 8
2 8 8 8 8 8 8 8 8 8
2 0 0 0 0 0 0 0 0 0
2 8 8 8 8 8 8 8 8 8
2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x1280 at 0x744068E449D0>
Okay, let's analyze this input-output pair.

**Perception of Elements:**

*   The input and output grids are of the same dimensions (20x10).
*   The primary colors involved are white (0), red (2), azure (8), and yellow (4).
*   There are vertical and horizontal lines of red (2) pixels.
*   There are isolated azure (8) pixels within the white (0) region, seemingly surrounded by or adjacent to red (2) lines.
*    In areas where azure and reds interact, in the output the azure appears to expand, and yellow is introduced.

**YAML Block - Facts:**


```yaml
objects:
  - name: red_lines
    type: line
    color: red
    orientation:
      - vertical
      - horizontal
    properties:
      - contiguous

  - name: azure_pixels
    type: pixel
    color: azure
    properties:
     - isolated
     - can be adjacent to red lines

  - name: yellow_pixels
    type: pixel
    color: yellow
    properties:
        - appear in output only

  - name: background
    type: fill
    color: white

actions:
  - name: expand_azure
    agent: azure_pixels
    condition: adjacent to red_lines, in area defined by red lines
    result:
      - azure pixels fill contiguous white areas bounded by red_lines
  - name: introduce_yellow
      agent: process
      condition: where original azure was
      result: those pixels become yellow

relationships:
  - red_lines define regions:
    - azure_pixels might reside within these
  - azure_pixels and red_lines have spatial relationship:
    - adjacency triggers transformation
```


**Natural Language Program:**

1.  **Identify Red Lines:** Locate all contiguous horizontal and vertical lines of red (2) pixels. These act as boundaries.
2.  **Identify initial Azure Pixels:** Find all azure (8) pixels.
3. **Fill within boundaries**: identify areas bound by the red lines, and expand the azure (8) pixels to fill any contiguous white (0) areas.
4.  **Introduce Yellow:** Where azure pixels were located in the input grid, replace with yellow (4) in the output grid.
5. **Preserve Red:** The red lines (2) remain unchanged.
6. **Background Remains:** All other white (0) areas not next to existing azure areas remain.


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
