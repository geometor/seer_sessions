# 855e0971 • 016 • example_3 • investigate_coder

---

## train_3

**input:**
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 0 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 0 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 0 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 0 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
```

<PIL.Image.Image image mode=RGB size=960x832 at 0x7A174C74F650>

**output:**
```
8 8 8 0 8 8 8 8 8 8 8 0 8 8 8
8 8 8 0 8 8 8 8 8 8 8 0 8 8 8
8 8 8 0 8 8 8 8 8 8 8 0 8 8 8
8 8 8 0 8 8 8 8 8 8 8 0 8 8 8
8 8 8 0 8 8 8 8 8 8 8 0 8 8 8
2 2 2 2 2 0 2 2 2 2 2 2 2 2 2
2 2 2 2 2 0 2 2 2 2 2 2 2 2 2
2 2 2 2 2 0 2 2 2 2 2 2 2 2 2
2 2 2 2 2 0 2 2 2 2 2 2 2 2 2
2 2 2 2 2 0 2 2 2 2 2 2 2 2 2
3 3 3 3 3 3 3 0 3 3 3 3 3 3 3
3 3 3 3 3 3 3 0 3 3 3 3 3 3 3
3 3 3 3 3 3 3 0 3 3 3 3 3 3 3
```

<PIL.Image.Image image mode=RGB size=960x832 at 0x7A17541447D0>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves a grid of colored pixels. There are three distinct horizontal bands of color: azure (8) at the top, red (2) in the middle, and green (3) at the bottom. Within each band, there's a single white (0) pixel. The transformation seems to replicate each row containing a white pixel multiple times.

**YAML Block (Facts):**


```yaml
objects:
  - name: grid
    type: 2D array
    properties:
      - colors: [0, 2, 3, 8]  # white, red, green, azure
      - dimensions: [13, 15] # input dimensions, rows, cols
  - name: color_band
    type: horizontal_region
    properties:
      - colors: [8, 2, 3] #azure, red, green
      - arrangement: stacked vertically
  - name: white_pixel
    type: single_cell
    properties:
       - color: 0
       - location: varies within each color band

actions:
  - name: replicate_row
    description: Duplicate rows containing the white pixel.
    parameters:
      - count: determined by the input

relationships:
   - white_pixel is_within color_band
   - color_bands are_part_of grid
```


**Natural Language Program:**

1.  **Identify Color Bands:** The input grid is divided into three horizontal color bands: azure on top, red in the middle, and green at the bottom.

2.  **Locate White Pixels:** Within each color band, find the single white (0) pixel. Note the row index of each white pixel.

3. **Determine number of white pixels** Determine how many times each colored section has a white square in it's area

4.  **Replicate Rows:** For each row containing a white pixel: make copies of the row, and place them directly below the original row. The final count for each row with a white pixel in it, should be the same as the number of white pixels in the grid.

In summary, the input is a grid divided in three horizontal colored sections. Within each colored section, there is a white pixel. We replicate the rows containing white pixels so that for each original row with a white pixel, there are *n* rows in the output, where *n* is the number of white pixels in the input.

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
