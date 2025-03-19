# a5313dff • 016 • example_3 • investigate_coder

---

## train_3

**input:**
```
0 0 0 2 2 2 2 2 0 0 0 0
0 0 0 2 0 0 0 2 0 0 0 0
0 0 0 2 0 2 0 2 2 2 2 0
0 0 0 2 0 0 0 2 0 0 2 0
0 0 0 2 2 2 2 2 0 0 2 0
0 0 0 2 0 0 0 2 0 0 2 0
0 0 0 2 0 2 0 2 2 2 2 0
0 0 0 2 0 0 0 2 0 0 0 0
0 0 0 2 2 2 2 2 0 0 0 0
0 0 0 0 0 0 0 2 2 2 2 2
0 0 0 0 0 0 0 2 0 0 0 2
0 0 0 0 0 0 0 2 0 2 0 2
```

<PIL.Image.Image image mode=RGB size=768x768 at 0x7F4C2318BDD0>

**output:**
```
0 0 0 2 2 2 2 2 0 0 0 0
0 0 0 2 1 1 1 2 0 0 0 0
0 0 0 2 1 2 1 2 2 2 2 0
0 0 0 2 1 1 1 2 1 1 2 0
0 0 0 2 2 2 2 2 1 1 2 0
0 0 0 2 1 1 1 2 1 1 2 0
0 0 0 2 1 2 1 2 2 2 2 0
0 0 0 2 1 1 1 2 0 0 0 0
0 0 0 2 2 2 2 2 0 0 0 0
0 0 0 0 0 0 0 2 2 2 2 2
0 0 0 0 0 0 0 2 0 0 0 2
0 0 0 0 0 0 0 2 0 2 0 2
```

<PIL.Image.Image image mode=RGB size=768x768 at 0x7F4C1B75CA50>
Okay, let's analyze this input-output example pair to understand the transformation.

**Perception of Elements:**

*   The input and output grids are the same size (12x12).
*   The input grid contains only two colors: white (0) and red (2).
*   The output grid introduces a third color: blue (1).
*   The blue pixels in the output appear to fill the interior of the red object in the input. All interior white (0) pixels surrounded by red (2) pixels that were not edge pixels, have now become blue (1).
*    The edge shape and pixels of the red object is the same in the input and output.

**YAML Block (Facts):**


```yaml
objects:
  - name: red_object
    type: shape
    color: red (2)
    attribute: connected
    boundary: "outer edge of the shape"

  - name: white_background
    type: background
    color: white (0)
    attribute: surrounds red_object
    
  - name: enclosed_white
    type: pocket
    color: white(0)
    attribute: inside red_object
    
  - name: blue_fill
    type: fill
    color: blue (1)
    location: replaces enclosed_white

actions:
  - name: fill_interior
    agent: unknown
    target: enclosed_white
    result: blue_fill
    precondition: "enclosed_white is completely surrounded by red_object"

relationships:
    - type: containment
      subject: red_object
      object: enclosed_white
      
    - type: substitution
      subject: enclosed_white
      object: blue_fill
```


**Natural Language Program:**

1.  Identify the contiguous region of red (2) pixels, forming a "red\_object".
2.  Identify white (0) pixels that are completely surrounded by the "red\_object". Consider this as an "enclosed\_white" region.
3. Change all pixels inside "enclosed\_white" region from white (0) to blue (1), creating a "blue\_fill".
4.  The outer "boundary" of the red object remains unchanged.
5.  The overall output grid dimensions are identical to the input.

Essentially, the transformation is an "interior fill" operation. The program detects an enclosed region of white pixels within a red shape and fills that region with blue, leaving the surrounding red pixels and outer white areas as.

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
