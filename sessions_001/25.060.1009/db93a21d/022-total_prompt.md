# db93a21d • 022 • example_4 • investigate_coder

---

## train_4

**input:**
```
0 0 0 0 0 0 0 9 9 9 9 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 9 9 9 9 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 9 9 9 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 9 9 9 9 0 0 0 0 0 0 0 0 9 9 9 9 9 9
0 0 9 9 9 9 0 0 0 0 0 0 0 0 9 9 9 9 9 9
0 0 9 9 9 9 0 0 0 0 0 0 0 0 9 9 9 9 9 9
0 0 0 0 0 0 0 0 0 0 0 0 0 0 9 9 9 9 9 9
0 0 0 0 0 0 0 0 0 0 0 0 0 0 9 9 9 9 9 9
0 0 0 0 0 0 0 0 0 0 0 0 0 0 9 9 9 9 9 9
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=1280x1280 at 0x7FC252B98CD0>

**output:**
```
0 0 0 0 0 3 3 9 9 9 9 3 3 0 0 0 0 0 0 0
0 0 0 0 0 3 3 9 9 9 9 3 3 0 0 0 0 0 0 0
0 0 0 0 0 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0
0 0 0 0 0 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 1 1 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 1 1 1 0 0 0 0 0 0 0 0 0
3 3 3 3 3 3 3 3 1 1 1 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 1 1 1 3 3 3 3 3 3 3 3 3
3 3 9 9 9 9 3 3 1 1 1 3 3 3 3 3 3 3 3 3
3 3 9 9 9 9 3 3 1 1 1 3 3 3 9 9 9 9 9 9
3 3 9 9 9 9 3 3 1 1 1 3 3 3 9 9 9 9 9 9
3 3 9 9 9 9 3 3 1 1 1 3 3 3 9 9 9 9 9 9
3 3 3 3 3 3 3 3 1 1 1 3 3 3 9 9 9 9 9 9
3 3 3 3 3 3 3 3 1 1 1 3 3 3 9 9 9 9 9 9
0 0 1 1 1 1 0 1 1 1 1 3 3 3 9 9 9 9 9 9
0 0 1 1 1 1 0 1 1 1 1 3 3 3 3 3 3 3 3 3
0 0 1 1 1 1 0 1 1 1 1 3 3 3 3 3 3 3 3 3
0 0 1 1 1 1 0 1 1 1 1 3 3 3 3 3 3 3 3 3
0 0 1 1 1 1 0 1 1 1 1 0 0 0 1 1 1 1 1 1
0 0 1 1 1 1 0 1 1 1 1 0 0 0 1 1 1 1 1 1
```

<PIL.Image.Image image mode=RGB size=1280x1280 at 0x7FC253D5CB50>
Okay, here's my analysis of the provided input-output example pair, presented as a report:

**Perception of Elements:**

The task involves transforming a grid of colored pixels. The input grid primarily contains maroon (9) and white (0) pixels, while the output grid introduces blue (1) and green (3) pixels, in addition to retaining some of the maroon and white pixels. There's a clear structural change: shapes are being filled or outlined with different colors. It appears as if regions in the original image are either filled with another color, or outlined.

**YAML Fact Documentation:**


```yaml
objects:
  - name: maroon_region_1
    type: contiguous_region
    color: maroon (9)
    initial_location: top_left
    shape: rectangle
    size: 4x2
    bordering_color: white (0)
  - name: maroon_region_2
    type: contiguous_region
    color: maroon (9)
    initial_location: bottom_left
    shape: rectangle
    size: 4x3
    bordering_color: white (0)
  - name: maroon_region_3
    type: contiguous_region
    color: maroon(9)
    initial_location: bottom_right
    shape: rectangle
    size: 6x3
    bordering_color: white (0)
  - name: white_region
    type: background
    color: white (0)
    initial_location: surrounds maroon regions

  - name: blue_outline
    type: outline
    color: blue (1)
    outline_of: maroon_region_2
    thickness: 1 pixel

  - name: green_fill
    type: fill
    color: green(3)
    fill_of_regions:
      - white, surrounding maroon region 1, that also touch the top edge
      - maroon region 1, and replace its maroon pixels
    thickness: flood_fill

actions:
  - type: fill
    target: white, surrounding maroon region 1, that also touch the top edge
    color: green (3)
  - type: fill
    target: maroon_region_1
    color: green (3)
  - type: outline
    target: maroon_region_2
    color: blue (1)

relationships:
  - maroon_region_1 is adjacent to white_region
  - maroon_region_2 is adjacent to white_region
  - maroon_region_3 is adjacent to white_region
  - blue_outline encloses maroon_region_2 after transformation.
  - green fill covers maroon_region_1 after transformation
```


**Natural Language Program:**

1.  **Identify Maroon Regions:** Locate all contiguous regions of maroon (9) pixels.
2.  **Green Fill (Top Region and surround):** Find the top-most maroon region.
    *   Replace all maroon pixels of that region by green pixels.
    *   Find connected white region to the identified maroon region, that also touch the top edge of the grid
    *   Replace pixels in that white region with green.
3.  **Blue Outline (Middle Region):** find the leftmost maroon object.
    * If it is located directly under an object that was colored green, replace that region's white bounding box with blue color.
4.  **Bottom-Right Region**: Keep the bottom-right maroon region unchanged.


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
