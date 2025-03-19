# 8a004b2b • 020 • example_3 • investigate_coder

---

## train_3

**input:**
```
0 0 0 4 0 0 0 0 0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 2 2 0 0 0 1 1 1 0 0 0 0 0
0 0 0 0 2 2 2 0 0 0 1 1 1 0 0 0 0 0
0 0 0 0 2 2 2 0 0 0 1 1 1 0 0 0 0 0
0 0 0 0 0 0 0 3 3 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 3 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 3 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 1 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=1152x1024 at 0x7F2DF79E0750>

**output:**
```
4 0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 1 1 1 1 1 1 0
0 2 2 2 1 1 1 1 1 1 0
0 2 2 2 1 1 1 1 1 1 0
0 0 0 0 3 3 3 1 1 1 0
0 0 0 0 3 3 3 1 1 1 0
0 0 0 0 3 3 3 1 1 1 0
0 0 0 0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0 0 0 4
```

<PIL.Image.Image image mode=RGB size=704x704 at 0x7F2DF677DD50>
Okay, here's my analysis of the provided input-output example pair, aiming to discern the underlying transformation logic.

**Perception of Elements:**

The task involves 2D grids containing colored pixels. The colors are represented by digits 0-9. The input grid appears to have distinct regions of colors, including single pixels and blocks of the same color. The output grid seems to be a cropped and condensed version of the input, retaining some of the colored regions but significantly reducing the overall size and removing large areas of background (color 0). There appears to be some logic how colored blocks move to new locations. Yellow (4) pixels looks like they move to the corners. The other colors combine into one large object.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    properties:
      dimensions: [variable_height, variable_width]
      cells: integers (0-9) representing colors
  - type: region
    properties:
      color: integer (1-9)
      shape: rectangle (contiguous block of same color) or single_pixel
      position: [row, column]
  - type: background
    properties:
     color: 0

actions:
  - name: crop
    description: Remove rows and columns of background color (0) from the edges of the grid.
  - name: consolidate
    description: combine regions of color 1, 2, and 3 into adjacent space, colored 1
  - name: reposition
    description: move yellow pixels into available corners

relationships:
  - regions_within_grid: Each region is contained within the grid.
  - background_surrounds_regions: Regions of non-zero color are surrounded by background (0).
```


**Natural Language Program:**

1.  **Identify Regions:** Locate all contiguous regions (blocks) of non-zero colored pixels and single non-zero pixels within the input grid.
2.  **Crop Background:** Remove all rows and columns along the edges of the grid that contain only background color (0). Continue until a non-zero pixel is encountered on the outer edge.
3.  **Consolidate colored regions:** Find the regions that have color, 2 (red) and 3 (green) and set the color to the right-most color in the row.
4.  **Reposition Yellow Pixels:** Find all single pixels of color 4 (yellow). Locate the available corners in the grid, where "available" means a location that is currently the background color, 0. Move the pixels to the top-left, top-right, bottom-left, and bottom-right corners, in any order.
5. **Consolidate and Fill:** Take the 1, 2 and 3 colored regions and consolidate to the color that is at the right-most edge of each row.


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
