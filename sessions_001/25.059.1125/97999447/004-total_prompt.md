# 97999447 • 004 • example_1 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=512x640 at 0x7F4C1B75CA50>

**output:**
```
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 2 5 2 5 2 5
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 6 5 6 5 6
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=512x640 at 0x7F4C1B6BFDD0>
Okay, let's analyze this input-output example.

**Perception of Elements:**

The input is a 10x8 grid, mostly filled with 0s (white pixels). There are two non-zero pixels: a '2' (red) at (2,2) and a '6' (magenta) at (5,3). The output grid has the same dimensions. The '2' and '6' pixels from the input are still present in the output.  A new '5'(gray) color appears, forming alternating horizontal lines with the 2 and 6.

**YAML Block (Facts):**


```yaml
objects:
  - type: pixel
    value: 2
    color: red
    initial_position: (2, 2)
  - type: pixel
    value: 6
    color: magenta
    initial_position: (5, 3)
  - type: pixel
    value: 0
    color: white
  - type: pixel
    value: 5
    color: gray
grid:
  width: 8
  height: 10
actions:
- type: fill
  description: alternating fill to the right of colored pixels
```


**Natural Language Program:**

1.  Identify the non-zero pixels in the input grid (excluding white pixels).
2. For each identified non-zero pixel, copy to output.
3.  Starting at the column immediately to the right of each copied pixel, begin an alternating fill pattern extending to the edge of the grid. This pattern consists of the original pixel, followed by gray color pixel, repeating this sequence until the end of the row is reached.


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
