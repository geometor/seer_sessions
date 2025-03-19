# e179c5f4 • 014 • example_3 • investigate_coder

---

## Example 3

**input:**
```
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
1 0 0 0
```

<PIL.Image.Image image mode=RGB size=256x640 at 0x786C548805D0>

**output:**
```
8 8 8 1
8 8 1 8
8 1 8 8
1 8 8 8
8 1 8 8
8 8 1 8
8 8 8 1
8 8 1 8
8 1 8 8
1 8 8 8
```

<PIL.Image.Image image mode=RGB size=256x640 at 0x786C5492F150>
Okay, here's my analysis of the provided example, focusing on perception, documented facts, and a natural language program describing the transformation.

**Perception of Elements:**

The input is a 10x4 grid of mostly white (0) pixels, with a single blue (1) pixel in the bottom left corner. The output is a 10x4 grid. The output grid appears to be filled with azure (8) pixels, and a 3x3 cross/plus sign shaped object of blue (1) pixels. The location of the blue object within the output grid appears to be related to the initial position of the single blue pixel in the input grid.

**YAML Block (Facts):**


```yaml
facts:
  - input_grid:
      dimensions: 10x4
      elements:
        - color: white
          value: 0
          count: 39
        - color: blue
          value: 1
          count: 1
          initial_position: [9, 0]  # row, column (0-indexed)
  - output_grid:
      dimensions: 10x4
      elements:
        - color: azure
          value: 8
          count: 35
        - color: blue
          value: 1
          count: 5
          shape: cross
          center_position: [9, 0] # row, column (0, indexed), relative to input blue pixel
  - transformation:
    - type: replace_background
      original_color: 0
      new_color: 8
    - type: create_shape
      shape: cross
      color: 1
      size: 3x3  # Specifies the extent of the cross.
      center: input_blue_pixel_location

```


**Natural Language Program:**

1.  **Background Replacement:** Change all white (0) pixels in the input grid to azure (8).
2.  **Shape Creation:** Create a cross/plus sign shaped object.
    -   The cross is made of blue (1) pixels.
    -   The dimensions of the cross is 3x3.
    -    The center of the cross will be placed at the input blue pixel.
3. Render the output grid with background and shape.


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
