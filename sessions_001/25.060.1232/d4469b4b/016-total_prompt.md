# d4469b4b • 016 • example_3 • investigate_coder

---

## train_3

**input:**
```
3 0 0 0 0
0 0 0 3 3
0 3 3 0 0
0 3 0 3 0
3 0 3 3 0
```

<PIL.Image.Image image mode=RGB size=320x320 at 0x7CE41B97AC50>

**output:**
```
0 0 5
0 0 5
5 5 5
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x7CE4233269D0>
Okay, let's analyze this input-output pair.

**Perception of Elements:**

*   The input is a 5x5 grid. The output is a 3x3 grid.
*   The input grid contains only the values 0 (white) and 3 (green).
*   The output grid contains only the values 0 (white) and 5 (gray).
*   The input seems to have dispersed green pixels, and the output has a concentrated block of grey pixels.
*   The size reduction suggests some form of summarization or compression.

**YAML Block (Facts):**


```yaml
objects:
  - name: input_grid
    type: grid
    dimensions: 5x5
    values: [0, 3]
  - name: output_grid
    type: grid
    dimensions: 3x3
    values: [0, 5]
  - name: green_pixels
    type: pixels
    value: 3
    input_grid_location: dispersed
  - name: grey_pixels
    type: pixels
    value: 5
    output_grid_location: bottom-right corner
  - name: white_pixels
    type: pixel
    value: 0
    input_grid_location: dispersed
    output_grid_location: top-left corner

actions:
  - name: count
    object: green_pixels
    description: Count the number of green pixels in the input grid.
  - name: compress
    input: input_grid
    output: output_grid
    description: Reduce the grid size from 5x5 to 3x3.
  - name: fill
    object: output_grid
    description:  Fill part of output grid with grey based upon green pixel count

relationships:
    - input_grid_contains: [green_pixels, white_pixels]
    - output_grid_contains: [grey_pixels, white_pixels]
    - green_pixel_count_determines: grey_pixel_area
```


**Natural Language Program:**

1.  **Count:** Count the number of green (value 3) pixels in the input grid.
2.  **Compress:** Reduce the grid size from 5x5 to 3x3.
3. **Fill output**: If the green count is greater than 0, fill the bottom right corner cells with the value 5, in a square, the amount of pixels equals the count of the green. Fill all other cells with zero.

Based upon the example, if the green count is nine, create a 3 x 3 solid square, filled with '5'.

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
