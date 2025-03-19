# be94b721 • 008 • example_2 • investigate_coder

---

## Example 2

**input:**
```
0 0 0 0 0 0 0 6 6 0
0 3 0 0 4 4 0 0 6 0
3 3 3 0 4 4 0 0 0 0
0 3 0 0 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x320 at 0x777869E5D450>

**output:**
```
4 4
4 4
4 4
```

<PIL.Image.Image image mode=RGB size=128x192 at 0x7778518FB430>
Okay, here's my analysis of the provided example, focusing on perception, documented facts, and a natural language program describing the transformation.

**Perception of Elements:**

The input is a grid of colored pixels, where each number represents a distinct color. The output is a smaller grid containing only one color (yellow, represented by '4') extracted from the input. The input grid contains several distinct colored regions (green '3', yellow '4', and magenta '6', as well as many white '0' pixels), while the output grid consists of only the yellow pixels arranged in a filled rectangle. The position and size of the rectangle in the output do not obviously correlate to the position of the colored regions.

**YAML Block (Facts):**


```yaml
facts:
  - input:
      type: grid
      elements:
        - color: white
          value: 0
        - color: green
          value: 3
        - color: yellow
          value: 4
        - color: magenta
          value: 6
      dimensions: [5, 10]
  - output:
      type: grid
      elements:
        - color: yellow
          value: 4
      dimensions: [3, 2]
  - objects:
      - name: green_region
        color: green
        value: 3
      - name: yellow_region
        color: yellow
        value: 4
      - name: magenta_region
        color: magenta
        value: 6
  - actions:
      - name: extract_color
        target: yellow_region
      - name: reshape
        description: Form a rectangle from extracted color, based on its total count
  - relationships:
      - type: contains
        from: input
        to: [green_region, yellow_region, magenta_region]
      - type: color_match
        from: yellow_region
        to: output

```


**Natural Language Program:**

1.  **Identify Objects:** Locate all contiguous regions of the same color within the input grid. Specifically, pay attention to the yellow region (pixels with a value of '4').
2.  **Count Target Pixels:** Count the total number of yellow pixels.
3.  **Determine Dimensions** Find the dimensions that mostly evenly divides the total number of pixels, with a preference to width being smaller than height
4.  **Construct Output:** Create a new, solid rectangle consisting only of yellow pixels.


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
