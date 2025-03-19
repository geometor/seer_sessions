# a699fb00 • 004 • example_1 • investigate_coder

---

## train_1

**input:**
```
1 0 1 0 0
0 0 0 0 0
0 0 0 0 0
0 1 0 1 0
0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=320x320 at 0x7F4C1B6BF250>

**output:**
```
1 2 1 0 0
0 0 0 0 0
0 0 0 0 0
0 1 2 1 0
0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=320x320 at 0x7F4C1B67DFD0>
Okay, here's my analysis of the provided input-output example pair:

**Perception of Elements:**

The task involves a 2D grid of pixels, each with a single digit integer value representing a color. The primary change appears to be the modification of specific pixels that were originally blue (value 1) in the input, changing them to red (value 2) in the output. Other pixels seem to remain unchanged. The spatial arrangement of the grid and the pixels remains consistent.

**YAML Fact Block:**


```yaml
facts:
  - type: grid
    description: 2D array of pixels
    input_dimensions: 5x5
    output_dimensions: 5x5
  - type: object
    description: individual pixels
    property: color_value (integer 0-9)
  - type: transformation
    description: color change
    input_color: blue (1)
    output_color: red (2)
    condition: "adjacent to two other blue pixels"
  - type: observation
    description: other pixels remain unchanged
```


**Natural Language Program:**

1.  **Iterate** through each pixel in the input grid.
2.  **Identify** pixels with a value of 1 (blue).
3.  **Check Neighbors:** For each blue pixel, examine its four directly adjacent neighbors (up, down, left, and right). Do not check diagonal.
4.   **Conditional Change**: If and only if a blue pixel is cardinally adjacent to *exactly* two other blue pixels, change its value to 2 (red).
5.  **Preserve**: All other pixels retain their original values.
6.  **Output**: The modified grid becomes the output.

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
