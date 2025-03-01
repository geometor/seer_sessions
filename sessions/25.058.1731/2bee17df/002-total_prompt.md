# 2bee17df • 002 • example_3 • investigate_coder

---

## train_1

**input:**
```
2 2 2 2 2 2 2 2 2 2 2 2
8 0 0 0 2 2 0 2 2 2 2 2
8 0 0 0 0 2 0 0 2 2 0 2
8 0 0 0 0 0 0 0 0 0 0 2
8 0 0 0 0 0 0 0 0 0 0 2
8 0 0 0 0 0 0 0 0 0 0 2
8 0 0 0 0 0 0 0 0 0 0 2
8 0 0 0 0 0 0 0 0 0 0 8
8 0 0 0 0 0 0 0 0 0 0 8
8 8 0 0 0 0 8 8 0 0 0 8
8 8 8 0 0 8 8 8 0 0 8 8
8 8 8 8 8 8 8 8 8 8 8 8
```

<PIL.Image.Image image mode=RGB size=768x768 at 0x7C360457AAD0>

**output:**
```
2 2 2 2 2 2 2 2 2 2 2 2
8 0 0 3 2 2 0 2 2 2 2 2
8 0 0 3 0 2 0 0 2 2 0 2
8 3 3 3 3 3 3 3 3 3 3 2
8 3 3 3 3 3 3 3 3 3 3 2
8 3 3 3 3 3 3 3 3 3 3 2
8 3 3 3 3 3 3 3 3 3 3 2
8 3 3 3 3 3 3 3 3 3 3 8
8 3 3 3 3 3 3 3 3 3 3 8
8 8 0 3 0 0 8 8 0 0 0 8
8 8 8 3 0 8 8 8 0 0 8 8
8 8 8 8 8 8 8 8 8 8 8 8
```

<PIL.Image.Image image mode=RGB size=768x768 at 0x7C360457A4D0>

## train_2

**input:**
```
8 8 8 8 8 8 8 8 8 8 8 8
2 0 0 0 0 0 8 8 8 8 8 8
2 2 0 0 0 0 0 8 8 0 0 8
2 0 0 0 0 0 0 8 0 0 0 8
2 0 0 0 0 0 0 0 0 0 0 8
2 2 2 0 0 0 0 0 0 0 0 8
2 2 0 0 0 0 0 0 0 0 0 8
2 2 0 0 0 0 0 0 0 0 0 8
2 0 0 0 0 0 0 0 0 0 0 8
2 0 0 0 0 0 0 0 0 0 2 2
2 2 0 2 0 0 2 0 0 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2
```

<PIL.Image.Image image mode=RGB size=768x768 at 0x7C360457AFD0>

**output:**
```
8 8 8 8 8 8 8 8 8 8 8 8
2 0 0 0 3 3 8 8 8 8 8 8
2 2 0 0 3 3 0 8 8 0 0 8
2 0 0 0 3 3 0 8 0 0 0 8
2 3 3 3 3 3 3 3 3 3 3 8
2 2 2 0 3 3 0 0 0 0 0 8
2 2 0 0 3 3 0 0 0 0 0 8
2 2 0 0 3 3 0 0 0 0 0 8
2 3 3 3 3 3 3 3 3 3 3 8
2 0 0 0 3 3 0 0 0 0 2 2
2 2 0 2 3 3 2 0 0 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2
```

<PIL.Image.Image image mode=RGB size=768x768 at 0x7C3604579850>

## train_3

**input:**
```
8 8 8 8 8 8 8 8 8 2
8 8 8 0 8 8 0 8 0 2
8 8 0 0 8 0 0 0 0 2
8 8 0 0 0 0 0 0 2 2
8 0 0 0 0 0 0 0 2 2
8 0 0 0 0 0 0 0 0 2
8 0 0 0 0 0 0 0 0 2
8 0 0 0 0 0 2 2 0 2
8 2 0 0 0 2 2 2 2 2
8 2 2 2 2 2 2 2 2 2
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7C360457B6D0>

**output:**
```
8 8 8 8 8 8 8 8 8 2
8 8 8 3 8 8 0 8 0 2
8 8 0 3 8 0 0 0 0 2
8 8 0 3 0 0 0 0 2 2
8 0 0 3 0 0 0 0 2 2
8 3 3 3 3 3 3 3 3 2
8 3 3 3 3 3 3 3 3 2
8 0 0 3 0 0 2 2 0 2
8 2 0 3 0 2 2 2 2 2
8 2 2 2 2 2 2 2 2 2
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7C360455CC50>
<PIL.Image.Image image mode=RGB size=2256x1586 at 0x7C36039E5BD0>Okay, here's a breakdown of my observations and a proposed natural language program for the transformation:

**Perception of Elements:**

*   **Grids:** The input and output are both grids of the same dimensions.
*   **Colors:**  Pixels have colors (represented by numbers 0-9). The most frequent colors in these examples are white (0), azure (8), red (2), and green(3).
*   **Shapes:** There are distinct regions or shapes of white (0) surrounded by borders of azure(8) and red(2).
*    **Change:** there is a connected region of white (0) pixels in the input that, in the output, is colored green (3)
*   **Background:** The azure(8) and red(2) colors remain constant between the input and output.

**YAML Fact Documentation:**


```yaml
objects:
  - name: background_frame
    type: frame
    properties:
      colors: [azure, red]
      position: constant
      behavior: static
  - name: changed_region
    type: region
    properties:
      input_color: white
      output_color: green
      shape: irregular
      position: variable
      behavior: color_change
  - name: entire_grid
     type: grid
     properties:
      dimensions: same for input and output

actions:
  - name: change_color
    agent: unknown
    target: changed_region
    parameters:
      from: white
      to: green

relationships:
  - type: surrounds
    subject: background_frame
    object: changed_region
  - type: within
    subject: changed_region
    object: entire_grid
  - type: within
     subject: background_frame
     object: entire_grid

```


**Natural Language Program:**

1.  **Identify the background frame:** Find the contiguous regions of azure (8) and red (2) that border the white areas(0). These regions don't change in color.

2.  **Locate the contiguous area to transform:** Within the frame formed by the red(2) and azure(8) area, locate the biggest connected white(0) area.

3.  **Recolor the shape** Every pixel within that located area changes its color from white (0) to green (3).

4.   **Preserve Other colors:** ensure that the red (2) and azure(8) color pixels remain unchanged in color and place.

In short we can say that the program takes all the largest connected area of color white(0) inside a frame of colors red(2) and azure(8), and changes their color into green(3). Everything else remains unchanged.

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
