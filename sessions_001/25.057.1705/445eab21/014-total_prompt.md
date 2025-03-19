# 445eab21 • 014 • example_3 • investigate_coder

---

## Example 3

**input:**
```
0 4 4 4 4 4 4 0 0 0
0 4 0 0 0 0 4 0 0 0
0 4 0 0 0 0 4 0 0 0
0 4 0 0 0 0 4 0 0 0
0 4 0 0 0 0 4 0 0 0
0 4 0 0 0 0 4 0 0 0
0 4 4 4 4 4 4 0 0 0
0 0 0 0 0 0 0 2 2 2
0 0 0 0 0 0 0 2 0 2
0 0 0 0 0 0 0 2 2 2
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x777851601DB0>

**output:**
```
4 4
4 4
```

<PIL.Image.Image image mode=RGB size=128x128 at 0x777851443C50>
Okay, here's my analysis of the provided example, formatted as a report:

**Perception of Elements:**

The task involves two grids: an input grid and an output grid. The input grid contains two distinct shapes formed by colored pixels. One shape is a larger "C" made of yellow (4) pixels, and the other is a smaller square made of red (2) pixels. The output grid contains only a small 2x2 square of yellow (4) pixels. The background of both grids is white (0).

**YAML Fact Block:**


```yaml
facts:
  - object: shape_1
    type: "C"
    color: yellow
    pixels: [ (0,1), (0,2), (0,3), (0,4), (0,5), (0,6), (1,1), (2,1), (3,1), (4,1), (5,1), (6,1), (6,2), (6,3), (6,4), (6,5), (6,6) ]
  - object: shape_2
    type: square
    color: red
    pixels: [ (7,7), (7,8), (7,9), (8,7), (8,9), (9,7), (9,8), (9,9) ]
  - object: output_shape
    type: square
    color: yellow
    pixels: [ (0,0), (0,1), (1,0), (1,1) ]
    size: 2x2

  - action: extract_subshape
    input: shape_1
    output: output_shape
    description: A 2x2 subshape is extracted from the larger yellow shape.

  - relation: shape_2_ignored
    description: The red shape in the input is completely ignored in the output.
```


**Natural Language Program:**

1.  **Identify Shapes:** Locate all distinct shapes within the input grid. A shape is defined as a contiguous block of pixels of the same color.
2.  **Select Target Shape:** Identify the object made by the yellow (value 4) pixels. Other shape(s) are ignored.
3.  **Extract Sub-shape:** From the upper-leftmost corner of the yellow "C" object in the original, extract a 2x2 square sub-shape from the targeted shape.
4. **Return sub-shape**: return the extracted sub-shape as a new grid, keeping the original colors and values.

In summary, the transformation rule involves identifying the largest yellow shape, and extracting a 2x2 square of pixels starting from the top-left part of the yellow "c" shape. The red shape is completely ignored.

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
