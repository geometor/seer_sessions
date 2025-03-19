# 2bcee788 • 022 • example_4 • investigate_coder

---

## train_4

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 0 0 0 0
0 0 0 0 0 8 0 0 0 0
0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7B4BFE1798D0>

**output:**
```
3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3
3 3 3 8 8 8 3 3 3 3
3 3 3 3 3 8 3 3 3 3
3 3 3 3 3 8 3 3 3 3
3 3 3 8 8 8 3 3 3 3
3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7B4BFDB421D0>
Okay, let's analyze this input-output pair.

**Perception of Elements:**

*   The input is a 10x10 grid with mostly white (0) pixels. There's a horizontal line of three azure (8) pixels and a single red (2) pixel below and to the right of the azure line.
*   The output is also a 10x10 grid. Most of the grid is green (3). The azure (8) pixels from the input are retained in the same position, But the red (2) is gone, and the azure line is extended by an additional line.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    dimensions: 10x10
    elements: pixels
    background:
      input: 0  # white
      output: 3 # green
  - type: line
    color: 8 # azure
    length: 3
    orientation: horizontal
    position:
        start: [4,3] # row 5 (index 4), col 4 (index 3)

  - type: pixel
    color: 2 # red
    position: [6,5] # row 7(index 6), col 6 (index 5)

actions:
  - type: fill
    target: background
    color: 3
  - type: copy
    target: line
    color: 8
    position: same
  - type: extend_shape
    target: line
    color: 8
    extend_down: true
    amount: 2
  - type: remove
    target: pixel
    color: 2

```


**Natural Language Program:**

1.  **Background Change:** Change all background (white/0) pixels in the input grid to green (3) pixels in the output grid.
2. **Copy azure object:** The azure object of three adjacent pixels in a horizontal line is maintained.
3. **Extend azure:** The initial azure shape is extended downward by two pixels, resulting in an L shape, or the inverse of an L, depending on perspective.
4.  **Remove Red Pixel:** The single red pixel in the input is not present, or it transforms to green matching the background.


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
