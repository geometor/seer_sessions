# be94b721 • 002 • example_1 • investigate_coder

---

## Example 1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 3 3 0 0 0 0 0 0
0 0 2 0 0 0 3 0 0 1 0 0 0
0 0 2 2 0 0 0 0 1 1 0 0 0
0 2 2 2 0 0 0 0 1 1 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=832x448 at 0x7778518FB430>

**output:**
```
2 2 0
0 2 0
0 2 2
2 2 2
```

<PIL.Image.Image image mode=RGB size=192x256 at 0x777851443C50>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves transforming a larger grid (input) into a smaller grid (output). The input grid contains several distinct colored regions (red, green, and blue, represented by values 2, 3, and 1, respectively) against a white background (value 0). The output grid seems to focus on a single color from the input (red, value 2), preserving its shape and relative position but cropping out the rest of the input grid.

**YAML Block (Facts):**


```yaml
objects:
  - id: red_shape
    color: red
    value: 2
    type: contiguous_region
    initial_position: (1,1) # Top-left corner of the shape in input
    final_position: (0,0) # Top-left corner of the shape in output
  - id: green_shape
    color: green
    value: 3
    type: contiguous_region
    initial_position: (1,5)
  - id: blue_shape
    color: blue
    value: 1
    type: contiguous_region
    initial_position: (2, 9)
  - id: background
    color: white
    value: 0
    type: background

actions:
  - type: selection
    target: red_shape
    description: The red shape is selected for preservation.
  - type: cropping
    description: The input grid is cropped around the selected shape.
  - type: size_reduction
    description: reduce size of input to size of output.

relationships:
  - red_shape_in_output: The output grid contains only the 'red_shape'.
  - spatial_preservation: The relative shape and position of 'red_shape' are maintained in the output.
```


**Natural Language Program:**

1.  **Identify Contiguous Regions:** Identify all distinct, contiguous regions of color within the input grid. In this case, they are red, green, blue and white regions.
2.  **Select Target Region:** Select the red region (value 2) as the target.
3. **Determine Output Boundaries:** Find the minimum bounding box that fully encloses red region.
4.  **Crop and Output:** Crop the input grid to this bounding box that surrounds it, resulting in the output grid. This effectively isolates the red region.

In essence, the program identifies and extracts the red colored region.

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
