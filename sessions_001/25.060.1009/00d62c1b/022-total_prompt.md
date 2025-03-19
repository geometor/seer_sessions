# 00d62c1b • 022 • example_4 • investigate_coder

---

## train_4

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 0 0 0 0
0 0 3 0 0 3 0 0 0 0
0 0 3 0 0 3 0 3 0 0
0 0 3 3 3 3 3 3 3 0
0 0 0 3 0 0 0 0 3 0
0 0 0 3 0 0 0 3 3 0
0 0 0 3 3 0 0 3 0 3
0 0 0 3 0 3 0 0 3 0
0 0 0 0 3 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7FC253D5CC50>

**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 0 0 0 0
0 0 3 4 4 3 0 0 0 0
0 0 3 4 4 3 0 3 0 0
0 0 3 3 3 3 3 3 3 0
0 0 0 3 0 0 0 0 3 0
0 0 0 3 0 0 0 3 3 0
0 0 0 3 3 0 0 3 4 3
0 0 0 3 4 3 0 0 3 0
0 0 0 0 3 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7FC253D4F8D0>
Okay, here's my analysis of the provided input-output example, focusing on perception, object identification, and the transformation rule.

**Perception of Elements:**

*   The input and output are grids of the same dimensions (10x10).
*   The grids contain numerical values representing colors. 0 is white, 3 is green, and 4 is yellow.
*   The input grid primarily consists of white (0) and green (3) pixels.
*   The output grid introduces yellow (4) pixels within the existing green (3) regions.
*    The yellow pixels seem to replace existing green, forming 2x1 or 1x2 rectangles.
*    The yellow areas appear to highlight some kind of feature within the larger green regions.

**YAML Block (Facts):**


```yaml
objects:
  - id: grid
    type: 2D array
    properties:
      dimensions: 10x10
      values: [0, 3, 4]  # Possible pixel values (colors)

  - id: green_regions
    type: connected_components
    properties:
      color: 3
      shape: irregular

 - id: yellow_highlights
    type: rectangles
    properties:
         color: 4
         size: [1x2, 2x1]
         location: inside green regions

actions:
  - name: highlight
    type: replace
    agent: system
    target: green_regions
    replacement: yellow_highlights
    constraints:
       - "yellow regions are only created within existing green regions"
       - "yellow regions are 2x1 or 1x2 rectangles"

relationships:
  - type: spatial
    subject: yellow_highlights
    object: green_regions
    description: "Yellow highlights are contained within green regions."
```


**Natural Language Program:**

1.  **Identify Green Regions:** Locate all contiguous regions of green (3) pixels within the input grid.
2.  **Analyze Shape/Feature, Determine Highlights:** Look at each green area, and locate internal 2x1 or 1x2 sections. These sections are, in reading order:
    *   The first encountered 2x1 or 1x2 rectangle where both pixels are on a line where all non-white pixels on that row are contiguous.
3.  **Create Yellow Highlights:** Within some of the identified green regions, replace a 2x1 or 1x2 section of green pixels with yellow (4) pixels.

In summary, the transformation identifies specific sub-regions (2x1 or 1x2 rectangles) within larger green areas and highlights them by changing their color to yellow. The highlights replace existing green and never added.

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
