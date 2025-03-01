# 539a4f51 • 006 • example_1 • investigate_coder

---

## train_1

**input:**
```
2 2 2 3 0
2 2 2 3 0
2 2 2 3 0
3 3 3 3 0
0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=320x320 at 0x744068DB7E50>

**output:**
```
2 2 2 3 2 2 2 3 2 2
2 2 2 3 2 2 2 3 2 2
2 2 2 3 2 2 2 3 2 2
3 3 3 3 2 2 2 3 2 2
2 2 2 2 2 2 2 3 2 2
2 2 2 2 2 2 2 3 2 2
2 2 2 2 2 2 2 3 2 2
3 3 3 3 3 3 3 3 2 2
2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x744068DB7ED0>
Okay, here's a breakdown of my observations and proposed transformation rule for the provided example:

**Perception of Elements:**

*   **Input Grid:** A 5x5 grid containing pixels of colors red (2), green (3), and white (0). There are distinct rectangular regions of red and green.
*   **Output Grid:** A 10x10 grid. The white (0) pixels from the input are gone. The red (2) and green (3) areas are still present, but the shape, size and area have changed. The Output grid appears to be composed of all 2s except a line of 3s.
* **Transformation:** It seem that the input pixels are mapped to larger area in output, and that the 0 value has been used somehow to determine the background value of the output.

**YAML Block (Facts):**


```yaml
objects:
  - name: input_grid
    type: grid
    properties:
      width: 5
      height: 5
      colors: [red, green, white]
    regions:
      - name: red_region
        shape: rectangle
        color: red
        top_left: [0,0]
        bottom_right: [2,3]
      - name: green_region
        shape: rectangle
        color: green
        top_left: [3,0]
        bottom_right: [3,3]
      - name: white_region
          shape: rectangle
          color: white
          top_left: [0,4]
          bottom_right: [4,4]

  - name: output_grid
    type: grid
    properties:
      width: 10
      height: 10
      colors: [red, green]
    regions:
      - description: expanded areas that appear to map from input
```


**Natural Language Program:**

1.  **Expansion:** Each non-white pixel in the input grid is expanded into a 2x2 block of the same color in the output grid. The top-left of each 2x2 block will map to row index `r*2`, col index `c*2`, where `r` and `c` are the input row and column of a non-white pixel.
2. **Background:** Create an output grid and fill every cell with the value `2`.
3. **Replacement:** Go through each pixel of the input. Replace the area in output corresponding to non-zero pixels, determined by the rule in step 1.

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
