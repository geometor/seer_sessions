# b94a9452 • 016 • example_3 • investigate_coder

---

## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 4 4 0 0 0 0 0 0
0 0 4 4 4 4 4 0 0 0 0 0 0
0 0 4 4 6 4 4 0 0 0 0 0 0
0 0 4 4 4 4 4 0 0 0 0 0 0
0 0 4 4 4 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=832x768 at 0x7F4C1B74F850>

**output:**
```
6 6 6 6 6
6 6 6 6 6
6 6 4 6 6
6 6 6 6 6
6 6 6 6 6
```

<PIL.Image.Image image mode=RGB size=320x320 at 0x7F4C1B75F350>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The input is a 12x13 grid, and the output is a 5x5 grid. The input grid contains a rectangular block of '4' (yellow) pixels with a single '6' (magenta) pixel in the center. The output grid is mostly '6' (magenta) pixels, with a single '4' (yellow) pixel at its center. The input yellow object appears to have been centered and vastly reduced in size, while the output has been filled with a single color taken from inside of that object.

**YAML Block (Facts):**


```yaml
facts:
  - input_grid_size: 12x13
  - output_grid_size: 5x5
  - input_object_color: 4 (yellow)
  - input_object_shape: rectangle
  - input_object_center_color: 6 (magenta)
  - output_background_color: 6 (magenta)
  - output_center_color: 4 (yellow)
  - transformation_type:  object_extraction_and_resizing
```


**Natural Language Program:**

1.  **Identify the Target Object:** Locate the largest rectangular block of contiguous pixels of the same color (excluding '0' - white) within the input grid.
2.  **Find the Center:** Determine the center pixel of this rectangular block. Note its color.
3. **Determine background fill color**: get color value from the center pixel of target object
4.  **Create Output Grid:** Create a 5x5 output grid.
5. **Fill the center:** fill all pixels with background fill color
6. **Extract and Place Center Pixel:** Fill the single, central pixel of 5x5 output with the original color from object in step 1.

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
