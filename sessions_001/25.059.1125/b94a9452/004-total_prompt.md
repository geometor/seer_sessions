# b94a9452 • 004 • example_1 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 2 0 0 0 0 0 0
0 0 0 2 4 4 2 0 0 0 0 0 0
0 0 0 2 4 4 2 0 0 0 0 0 0
0 0 0 2 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=832x768 at 0x7F4C1B700450>

**output:**
```
4 4 4 4
4 2 2 4
4 2 2 4
4 4 4 4
```

<PIL.Image.Image image mode=RGB size=256x256 at 0x7F4C1B703D50>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves transforming a larger grid (input) into a smaller grid (output). The input grid contains a central "object" composed of red (2) and yellow (4) pixels, surrounded by white (0) pixels. The output grid seems to be a zoomed-in and slightly altered representation of the central object in the input grid. The colors are preserved, but there's a change in the arrangement and potentially the relative size of colored regions. The output seems to extract the smallest square containing all non-zero pixels and inverts it.

**YAML Block (Facts):**


```yaml
objects:
  - name: input_grid
    type: grid
    properties:
      - dimensions: 12 x 13
      - colors: [0, 2, 4] # white, red, yellow
      - central_object:
          shape: rectangle-like
          colors: [2, 4]
          location: near center

  - name: output_grid
    type: grid
    properties:
      - dimensions: 4 x 4
      - colors: [2, 4] # red, yellow
      - structure: inverted color pattern of input's central non-zero region
```


**Natural Language Program:**

1.  **Identify the Region of Interest (ROI):** Find the smallest rectangular region within the input grid that encompasses all non-zero pixels (the central object composed of red and yellow pixels).
2. **Extract:** extract the non-zero section.
3.  **Invert the ROI:** swap colors on the x,y axes of the extracted section.

Essentially, the transformation identifies the smallest enclosing box around the colored region in the input, extracts, and swaps axis.

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
