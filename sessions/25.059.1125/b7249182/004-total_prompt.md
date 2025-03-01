# b7249182 • 004 • example_1 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x896 at 0x7F4C1B74F850>

**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0
0 0 2 2 2 2 2 0 0 0
0 0 2 0 0 0 2 0 0 0
0 0 8 0 0 0 8 0 0 0
0 0 8 8 8 8 8 0 0 0
0 0 0 0 8 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x896 at 0x7F4C231A8150>
Okay, let's analyze this input-output example pair to understand the transformation rule.

**Perception of Elements:**

*   The input and output are grids of digits, representing colored pixels.
*   The input grid contains two distinct single-pixel objects: a red pixel (2) and an azure pixel (8).
*   The output grid expands these single pixels into cross-shaped patterns of the same color.
*   The crosses appear to be centered on the original pixel locations.
*    The crosses created from the single pixels in the source have sizes that can be computed.

**YAML Fact Block:**


```yaml
facts:
  - type: input_grid
    description: Contains two single-pixel objects.
    objects:
      - color: red
        value: 2
        initial_position: [1, 4]
      - color: azure
        value: 8
        initial_position: [10, 4]

  - type: output_grid
    description: Contains two cross-shaped objects.
    objects:
      - color: red
        value: 2
        shape: cross
        center: [1, 4]
        extension:
          up: 2
          down: 2
          left: 2
          right: 2

      - color: azure
        value: 8
        shape: cross
        center: [10, 4]
        extension:
          up: 2
          down: 2
          left: 2
          right: 2
  - type: transformation
    description: "Each colored pixel in the input grid is transformed to the shape
      of the greek cross, centered at the same pixel.
      The cross size seems to be defined in extension as number of pixels.
      "
```


**Natural Language Program:**

1.  **Identify** all non-zero pixels in the input grid.
2.  **For each** identified pixel:
    a. **Note** the color (value) and the (row, column) position of the pixel.
    b. **Create** a cross-shaped pattern of the same color in the output grid, centered on the original pixel's position.
    c. The dimensions can be controlled by an `extension` parameter, that extends
    the cross by the value of `extension` in the 4 directions (up, down, left,
    right). For this example, extension is 2.
3. All the other pixels remain as 0s.


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
