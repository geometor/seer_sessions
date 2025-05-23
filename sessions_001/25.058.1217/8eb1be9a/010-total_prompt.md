# 8eb1be9a • 010 • example_2 • investigate_coder

---

## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
2 0 2 0 2 0 2 0 2 0 2 0
2 2 2 2 2 2 2 2 2 2 2 2
2 0 2 0 2 0 2 0 2 0 2 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=768x640 at 0x741F72B8F430>

**output:**
```
2 0 2 0 2 0 2 0 2 0 2 0
2 2 2 2 2 2 2 2 2 2 2 2
2 0 2 0 2 0 2 0 2 0 2 0
2 0 2 0 2 0 2 0 2 0 2 0
2 2 2 2 2 2 2 2 2 2 2 2
2 0 2 0 2 0 2 0 2 0 2 0
2 0 2 0 2 0 2 0 2 0 2 0
2 2 2 2 2 2 2 2 2 2 2 2
2 0 2 0 2 0 2 0 2 0 2 0
2 0 2 0 2 0 2 0 2 0 2 0
```

<PIL.Image.Image image mode=RGB size=768x640 at 0x741F72B8EA30>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves a grid of pixels, primarily using colors 'white' (0) and 'red' (2). The input appears to have a horizontal band of red pixels in the middle, with some alternating white pixels. The output expands this pattern, replicating the red and white pattern vertically throughout the entire grid, while keeping the solid red line in its original rows.

**YAML Block (Facts):**


```yaml
objects:
  - name: grid
    type: 2D array
    properties:
      - colors: [white, red]
      - dimensions: [height, width]
  - name: red_band
    type: object
    properties:
        - color: red
        - shape: horizontal line

  - name: white_pixels_in_band
    type: object
    properties:
      - color: white
      - shape: scattered

actions:
  - name: replicate_pattern
    description:  The alternating red and white pixel pattern within the red band is replicated vertically throughout the grid.

relationships:
  - The red_band is located in the central rows of the input grid.
  - white_pixels are interspersed within the red_band
```


**Natural Language Program:**

1.  **Identify the central red band:** Locate the contiguous horizontal rows of predominantly red pixels.
2.  **Identify the pattern within the red band.** Observe the alternating sequence of red and white pixels within these rows.
3.  **Replicate the pattern vertically:** Extend the identified red/white pattern from the red band upwards and downwards, filling the entire grid. Ensure the central solid red line remains.
4. **Maintain the original red band:** The central rows stay all red (2).
5. **Expand the alternating pattern:** rows above and below are filled with the alternating pattern.

Essentially, the transformation takes the pattern of red and white pixels *within* the central red band, keeps the center solid band, and propagates the red/white portions of the pattern vertically to fill the rest of the grid.

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
