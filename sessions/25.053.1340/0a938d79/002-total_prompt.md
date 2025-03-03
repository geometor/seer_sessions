# 0a938d79 • 002 • example_1 - CODE

---

# Example

**input:**
```
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=1600x640 at 0x73989FBBD600>

**output:**
```
0 0 0 0 0 2 0 8 0 2 0 8 0 2 0 8 0 2 0 8 0 2 0 8 0
0 0 0 0 0 2 0 8 0 2 0 8 0 2 0 8 0 2 0 8 0 2 0 8 0
0 0 0 0 0 2 0 8 0 2 0 8 0 2 0 8 0 2 0 8 0 2 0 8 0
0 0 0 0 0 2 0 8 0 2 0 8 0 2 0 8 0 2 0 8 0 2 0 8 0
0 0 0 0 0 2 0 8 0 2 0 8 0 2 0 8 0 2 0 8 0 2 0 8 0
0 0 0 0 0 2 0 8 0 2 0 8 0 2 0 8 0 2 0 8 0 2 0 8 0
0 0 0 0 0 2 0 8 0 2 0 8 0 2 0 8 0 2 0 8 0 2 0 8 0
0 0 0 0 0 2 0 8 0 2 0 8 0 2 0 8 0 2 0 8 0 2 0 8 0
0 0 0 0 0 2 0 8 0 2 0 8 0 2 0 8 0 2 0 8 0 2 0 8 0
0 0 0 0 0 2 0 8 0 2 0 8 0 2 0 8 0 2 0 8 0 2 0 8 0
```

<PIL.Image.Image image mode=RGB size=1600x640 at 0x73989FBBE590>
Okay, here's my analysis of the provided example, structured as requested:

**Perception of Elements:**

The task involves a transformation of a 2D grid of colored pixels. The input grid contains a few isolated pixels of color 'red' (2) and 'azure' (8) on a background of 'white' (0). The output grid appears to be a checkerboard-like pattern, constructed using the initial positions of the 'red' and 'azure' pixels as a starting point. The sizes of the input and output are different.

**YAML Fact Block:**


```yaml
facts:
  - entity: grid
    type: 2D array
    description: Contains pixels represented by integer values corresponding to colors.
  - entity: pixel
    type: element
    properties:
      color:
        type: integer
        values: [0, 2, 8]
        mapping:
          0: white
          2: red
          8: azure
      position:
        type: coordinates
        description: (row, column) within the grid.
  - action: pattern_extension
    description: Extends the initial colored pixels into a checkerboard pattern.
    parameters:
      alternating_colors: [2, 8]
      background_color: 0
  - observation: output_grid_dimensions
    description: The output grid has different dimension and extended by three columns at the start
  - relationship: checkerboard
    entity_1: red pixel
    entity_2: azure pixel
    description: Red and azure pixels alternate in the output grid, creating a checkerboard pattern.
```


**Natural Language Program:**

1.  **Identify Seeds:** Locate all pixels in the input grid that are not 'white' (0). These are the 'seed' pixels, which in this case are color 'red' (2) and 'azure' (8).
2.  **Determine Output Dimensions:** the number of rows are the same and add three columns at the start.
3.  **Create Checkerboard:** Generate a new grid which has three extra columns at the start and fill it with the checkerboard pattern. Starting at the top-left corner (0,0) of this output use one seed color and extend and repeat its color down each column and across each row, alternating with the other color.
4.  **Background:** Fill any remaining cells in the output grid with 'white' (0).


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
