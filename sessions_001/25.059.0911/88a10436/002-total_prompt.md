# 88a10436 • 002 • example_3 • investigate_coder

---

## train_1

**input:**
```
0 2 0 0 0 0 0 0 0
2 2 1 0 0 0 0 0 0
0 1 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=576x576 at 0x7D67CBEBB650>

**output:**
```
0 2 0 0 0 0 0 0 0
2 2 1 0 0 0 0 0 0
0 1 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0
0 0 0 0 2 2 1 0 0
0 0 0 0 0 1 3 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=576x576 at 0x7D67CBEBB5D0>

## train_2

**input:**
```
0 0 0 0 6 0 0
0 0 0 0 1 1 0
0 0 0 0 2 2 2
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 5 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=448x512 at 0x7D67CBDDB650>

**output:**
```
0 0 0 0 6 0 0
0 0 0 0 1 1 0
0 0 0 0 2 2 2
0 0 0 0 0 0 0
6 0 0 0 0 0 0
1 1 0 0 0 0 0
2 2 2 0 0 0 0
0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=448x512 at 0x7D67CBE7A0D0>

## train_3

**input:**
```
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0
0 0 3 1 0 0 0 0
0 3 3 1 0 0 0 0
0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=512x640 at 0x7D67CBE7A050>

**output:**
```
0 0 0 0 0 0 0 0
0 0 0 2 2 0 0 0
0 0 0 0 3 1 0 0
0 0 0 3 3 1 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0
0 0 3 1 0 0 0 0
0 3 3 1 0 0 0 0
0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=512x640 at 0x7D67CBE79ED0>
<PIL.Image.Image image mode=RGB size=1664x1360 at 0x7D67CBDADDD0>Okay, here's my analysis of the provided examples, focusing on object perception, transformation logic, and a structured natural language program.

**Perception of Elements:**

The task involves 2D grids where each cell contains a single digit representing a color.  The primary elements are colored objects, which appear to be contiguous blocks of pixels of the same color. There's a sense of spatial rearrangement, and possibly object interaction or copying. The input and output grids are not always the same size. Single colored pixels that do not form part of a larger object are ignored.

**YAML Fact Documentation:**


```yaml
facts:
  - domain: 2D grid
  - elements: colored objects
  - object_property: color (represented by digits 0-9)
  - object_property: shape (contiguous block of same color)
  - object_property: position (grid coordinates)
  - transformation_type: spatial_rearrangement
  - transformation_detail: "copying and translation of a selected colored object to a location previously occupied by a single pixel object"
  - observation: "single pixel object of a unique color disappears after transform"
  - observation: "input is copied to output"
  - constraint: "transformation applied only to connected components that are not single pixels"

```


**Natural Language Program:**

1.  **Identify Source Objects:** In the input grid, identify all contiguous colored objects (connected components that are not single pixels - more than one pixel of same color adjacent).

2.  **Identify Target Location** In the input grid, find the location of any single pixel object that is a unique color not used by any other object in the input grid.

3. **Copy Input**: copy the entire input grid to a new grid

4.  **Translate Object:** Translate the location of a copy of the identified multi-pixel source object, such that it is centered at the target location identified in step 2.

5. **Output Result:** Leave the translated object on the output, remove all other instances of the source object in the output.

In summary, the transformation identifies multi-pixel colored objects within the input grid. It also finds a uniquely colored single pixel object, and moves a copy of the source object to that location in the output.

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
