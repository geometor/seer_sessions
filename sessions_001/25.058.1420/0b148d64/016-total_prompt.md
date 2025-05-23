# 0b148d64 • 016 • example_3 • investigate_coder

---

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

<PIL.Image.Image image mode=RGB size=1088x1216 at 0x7A60A575D4F0>

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

<PIL.Image.Image image mode=RGB size=384x576 at 0x7A608C34ADF0>
Okay, let's analyze this input-output pair.

**Perception of Elements:**

The input is a large grid containing pixels of colors white (0), blue (1), and yellow (4). The output is a smaller grid containing only white (0) and yellow (4). The output grid appears to be a cropped and condensed version of a section of the input grid. It seems like a specific region of interest related to color '4' from the input is selected, and some surrounding white pixels are also retained.

**YAML Block (Facts):**


```yaml
objects:
  - name: input_grid
    type: grid
    properties:
      colors: [0, 1, 4]
      shape: [19, 17]
  - name: output_grid
    type: grid
    properties:
      colors: [0, 4]
      shape: [9, 6]
  - name: yellow_region
    type: object
    properties:
      color: 4
      location: bottom_left_input
  - name: white_region
    type: object
    properties:
       color: 0
       location: surrounds_yellow

actions:
  - name: extract
    agent: unknown
    input: input_grid, yellow_region_coordinates
    output: output_grid
    description: Extracts a rectangular section focused on the '4' colored area from the input grid, and removes all pixels of color 1.

relationships:
  - type: spatial
    subject: yellow_region
    object: input_grid
    description: The yellow region is located in the bottom-left part of the input grid.
  - type: spatial
     subject: output_grid
     object: input_grid
     description:  output grid dimensions and contents originate within the input grid, removing blue pixels
  - type: content
    subject: output_grid
    object: yellow_region, white_region
    description: The output grid consists of the yellow (4) region from the input and a white (0) border around.

```


**Natural Language Program:**

1.  **Identify the Target Region:** Locate the contiguous region of yellow (4) pixels in the input grid. It is at the bottom left.
2.  **Define Extraction Boundaries:** Determine a rectangular boundary around the yellow region. It appears to be expanded to encompass the entire yellow area.
3. **Extract Sub-Grid**: from the coordinates of the bounding box created, copy the contents
4.  **Filter Colors:** Within this extracted region, keep only the yellow (4) and white (0) pixels. Remove all blue (1) pixels.
5.  **Form Output:** The resulting filtered sub-grid becomes the output grid.

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
