# 508bd3b6 • 004 • example_1 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 2 2
0 0 0 0 0 0 0 0 0 0 2 2
0 0 0 0 0 0 0 0 0 0 2 2
0 0 0 0 0 0 0 0 0 0 2 2
0 0 0 0 0 0 0 0 0 0 2 2
0 0 0 0 0 0 0 0 0 0 2 2
0 0 0 0 0 0 0 0 0 0 2 2
0 0 0 0 0 0 0 0 0 0 2 2
0 0 0 0 0 0 0 0 0 0 2 2
0 0 0 0 0 0 0 0 0 0 2 2
0 0 0 8 0 0 0 0 0 0 2 2
0 0 8 0 0 0 0 0 0 0 2 2
```

<PIL.Image.Image image mode=RGB size=768x768 at 0x744068E00150>

**output:**
```
0 0 0 0 0 3 0 0 0 0 2 2
0 0 0 0 0 0 3 0 0 0 2 2
0 0 0 0 0 0 0 3 0 0 2 2
0 0 0 0 0 0 0 0 3 0 2 2
0 0 0 0 0 0 0 0 0 3 2 2
0 0 0 0 0 0 0 0 3 0 2 2
0 0 0 0 0 0 0 3 0 0 2 2
0 0 0 0 0 0 3 0 0 0 2 2
0 0 0 0 0 3 0 0 0 0 2 2
0 0 0 0 3 0 0 0 0 0 2 2
0 0 0 8 0 0 0 0 0 0 2 2
0 0 8 0 0 0 0 0 0 0 2 2
```

<PIL.Image.Image image mode=RGB size=768x768 at 0x744068E01250>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves a grid of colored pixels. The primary colors observed are white (0), red (2), azure (8), and green (3). The input grid contains a large white area, a vertical red rectangle on the right edge, and two azure pixels near the bottom-left. The output grid is very similar to the input, but a sequence of green pixels appears, seemingly originating from the top edge and moving downwards in a diagonal path.

**YAML Fact Documentation:**


```yaml
facts:
  - object: background
    color: white (0)
    description: fills most of the grid
  - object: red_rectangle
    color: red (2)
    shape: rectangle
    position: right edge, extends from top to bottom
    size: 12x2 (height x width)
  - object: azure_pixels
    color: azure (8)
    count: 2
    position: bottom-left, one pixel apart horizontally
  - object: green_path
    color: green (3)
    shape: diagonal line
    position: starts from top, moves down and slightly right
    length: variable, appears to stop before azure pixels
```


**Natural Language Program:**

1.  **Identify Static Elements:** The red rectangle on the right edge and the two azure pixels in the bottom-left remain unchanged in the output. These are static elements.
2. **Identify Dynamic Elements**: Green(3) pixels where added.
3.  **Describe the Transformation:**
     a. A green (3) pixel appears and moves until stopped by the top of the blue(8) pixel.
    b. At each horizontal row, The green pixel changes its position to the next column to the right.


```text
program:
  - find a constant 12x2 rectangle of color red(2) along the right
  - find all the azure(8) pixel
  - draw a line of green(3), starting from the center top
  - the green line should progress one step right on each row down
  - stop the green line above the azure pixel
```
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
