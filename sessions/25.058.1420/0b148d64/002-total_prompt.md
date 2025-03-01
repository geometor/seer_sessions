# 0b148d64 • 002 • example_3 • investigate_coder

---

## train_1

**input:**
```
8 8 8 8 8 0 8 8 8 8 0 0 0 0 8 8 8 8 0 8 8
8 0 0 8 0 8 0 8 8 8 0 0 0 0 8 8 8 0 0 0 8
8 8 8 0 0 0 8 8 8 8 0 0 0 0 8 8 0 8 8 8 8
8 8 0 8 8 8 8 0 8 8 0 0 0 0 8 8 0 0 0 8 8
8 8 8 8 0 8 8 0 8 8 0 0 0 0 8 8 8 0 8 8 8
0 0 0 8 8 0 8 0 0 8 0 0 0 0 8 0 0 0 8 0 0
8 8 8 8 0 0 8 0 8 0 0 0 0 0 8 8 8 0 8 8 8
8 0 0 8 0 0 8 8 0 8 0 0 0 0 8 0 8 8 8 8 8
8 8 8 8 8 8 0 8 0 0 0 0 0 0 8 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 2 2 2 2 0 0 0 0 8 8 0 8 8 0 8
2 0 2 2 2 0 0 2 2 2 0 0 0 0 8 8 8 8 0 8 0
0 2 2 2 2 2 2 0 2 0 0 0 0 0 8 8 8 0 0 0 8
2 2 2 2 0 2 2 2 2 2 0 0 0 0 8 8 0 8 8 8 0
2 2 2 2 2 2 0 2 0 0 0 0 0 0 8 8 8 8 8 0 0
2 2 2 2 2 0 2 0 2 2 0 0 0 0 8 0 8 0 8 8 8
2 2 0 2 2 0 0 0 0 0 0 0 0 0 8 8 0 8 0 0 8
0 2 2 0 0 2 2 0 0 2 0 0 0 0 8 0 0 0 8 8 0
2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 8 8 0 0 8 8
2 0 2 2 0 2 2 2 2 2 0 0 0 0 8 8 8 0 8 8 8
```

<PIL.Image.Image image mode=RGB size=1344x1344 at 0x7A608CFC2210>

**output:**
```
0 2 2 2 0 0 2 2 2 2
2 0 2 2 2 0 0 2 2 2
0 2 2 2 2 2 2 0 2 0
2 2 2 2 0 2 2 2 2 2
2 2 2 2 2 2 0 2 0 0
2 2 2 2 2 0 2 0 2 2
2 2 0 2 2 0 0 0 0 0
0 2 2 0 0 2 2 0 0 2
2 2 2 2 2 2 2 2 2 2
2 0 2 2 0 2 2 2 2 2
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7A608CFC2170>

## train_2

**input:**
```
2 0 2 2 2 2 0 0 0 0 2 0 2 2 2 2 0 0 2
2 2 2 2 0 2 2 0 0 0 0 2 2 2 2 2 0 0 0
0 0 2 2 0 2 0 0 0 0 2 2 2 0 2 2 2 2 2
2 0 2 0 2 2 0 0 0 0 0 2 2 2 2 2 2 0 0
0 2 0 2 2 2 2 0 0 0 0 0 0 2 2 0 2 2 2
2 2 2 0 2 0 2 0 0 0 2 0 2 2 2 2 0 2 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 0 2 0 0 0 2 0 0 0 0 3 3 3 3 3 0 3 3
0 2 2 0 0 2 2 0 0 0 3 3 3 0 0 0 3 3 0
0 2 2 0 0 2 0 0 0 0 3 3 3 0 3 0 3 0 0
2 2 2 0 0 2 2 0 0 0 3 3 0 0 0 3 3 3 3
2 0 0 2 2 2 0 0 0 0 3 0 0 0 3 0 3 0 3
2 0 2 0 0 0 2 0 0 0 0 3 3 0 3 3 3 0 3
0 2 2 0 2 2 0 0 0 0 0 3 3 0 0 3 0 3 0
```

<PIL.Image.Image image mode=RGB size=1216x1152 at 0x7A608CEF63F0>

**output:**
```
0 3 3 3 3 3 0 3 3
3 3 3 0 0 0 3 3 0
3 3 3 0 3 0 3 0 0
3 3 0 0 0 3 3 3 3
3 0 0 0 3 0 3 0 3
0 3 3 0 3 3 3 0 3
0 3 3 0 0 3 0 3 0
```

<PIL.Image.Image image mode=RGB size=576x448 at 0x7A608CEF6490>

## train_3

**input:**
```
0 1 0 1 1 1 0 0 1 1 0 1 0 0 0 0 0
1 0 1 0 0 0 0 0 1 1 1 1 1 1 0 1 1
1 1 0 1 1 0 0 0 1 1 1 1 1 1 0 1 1
1 1 0 0 1 1 0 0 1 1 0 1 1 1 1 1 1
0 1 1 1 0 0 0 0 1 1 0 0 0 1 1 1 0
1 0 0 1 0 0 0 0 1 1 0 0 1 1 1 1 1
0 0 0 1 1 0 0 0 1 1 1 0 0 1 0 0 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
4 0 0 4 0 4 0 0 1 0 0 1 1 1 1 1 1
4 4 4 4 0 4 0 0 1 0 1 1 1 1 1 1 0
4 0 4 0 0 4 0 0 0 1 0 0 1 1 1 1 1
0 4 4 4 4 0 0 0 1 1 0 0 1 0 1 0 1
4 4 4 0 4 4 0 0 1 1 1 1 1 1 1 1 0
0 4 4 4 4 0 0 0 0 1 0 0 0 0 1 1 1
0 4 4 4 0 4 0 0 0 1 0 1 0 1 1 1 0
0 4 0 0 0 0 0 0 1 0 1 1 1 0 1 0 1
4 4 0 4 0 4 0 0 1 1 1 0 0 1 1 1 0
```

<PIL.Image.Image image mode=RGB size=1088x1216 at 0x7A608CEF6170>

**output:**
```
4 0 0 4 0 4
4 4 4 4 0 4
4 0 4 0 0 4
0 4 4 4 4 0
4 4 4 0 4 4
0 4 4 4 4 0
0 4 4 4 0 4
0 4 0 0 0 0
4 4 0 4 0 4
```

<PIL.Image.Image image mode=RGB size=384x576 at 0x7A608CEF6210>
<PIL.Image.Image image mode=RGB size=3728x2034 at 0x7A608C34B4D0>Okay, here's my analysis of the provided input-output examples, focusing on perception, object identification, and the transformation rule.

**Perception of Elements**

The task involves 2D grids of colored pixels. The input grids are larger and contain a horizontal dividing line of black (0) pixels separating two distinct regions.  Above the line are seemingly random arrangements of colors.  Below the line is a region with one prominent color forming a shape.  The output grids are smaller, cropped versions of the lower region, specifically focusing on the shape defined by the prominent, non-black color. The other colors in that bottom region are replaced by black in the output.

**YAML Block: Facts**


```yaml
objects:
  - grid:
      type: 2D array
      elements: pixels
      properties:
        height: variable
        width: variable
  - pixel:
      type: element
      properties:
        color: integer (0-9)
  - region:
      type: subgrid
      properties:
          top_boundary: black_line # horizontal line of 0s
          bottom_boundary: input_grid_bottom
          left_boundary: input_grid_left
          right_boundary: input_grid_right

  - shape:
     type: object
     properties:
        color:  prominent_color_in_region # color other than 0 most frequent in the region
        boundary:  contiguous_block

actions:
  - identify_region:
      input: full_grid
      output: region
  - identify_shape:
      input: region
      output: shape_boundary
  - crop:
      input: region, shape_boundary
      output: cropped_grid
  - recolor:
      input: cropped_grid, shape
      output: output grid

relationships:
  - input_grid_contains: region
  - region_contains: shape
  - output_grid_is: cropped_and_recolored_region

```


**Natural Language Program**

1. **Identify Region:** Find the horizontal line of black (0) pixels that divides the input grid into two regions.  The region of interest is the one *below* this line.

2. **Identify Shape:** Within the region of interest, determine the most frequent non-black color. This color defines the "shape". All contiguous pixels of this color constitute the shape.

3. **Crop:** Determine the smallest bounding box that completely encloses the shape found in step 2. This bounding box acts as the cropping area.

4. **Recolor:** Create the output grid. This will have size of the bounding box in the step 3. Copy all pixels within the bounding box from the input region to output grid.

5. **Final Recoloring**. Within this cropped grid, replace all pixels that are *not* the shape's color with black (0). The final result will be a 2 color grid.

In short - find region of interest under black horizontal divider, isolate prominent shape within it, crop to shape, then recolor with the rest as background of black.

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
