# 67385a82 • 008 • example_2 • investigate_coder

---

## Example 2

**input:**
```
0 3 0 0 0 3
0 3 3 3 0 0
0 0 0 0 3 0
0 3 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=384x256 at 0x74AF1CCD9550>

**output:**
```
0 8 0 0 0 3
0 8 8 8 0 0
0 0 0 0 3 0
0 3 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=384x256 at 0x74AF1CB81150>
Okay, here's my analysis of the provided input-output example, formatted as a report:

**Perception of Elements:**

The task involves a grid of pixels, each with a numerical value representing a color. The input grid is transformed into an output grid of the same dimensions. The primary change observed is the replacement of some '3' (green) pixels with '8' (azure) pixels. The location of the replaced pixels seems significant. Specifically, it appears to be the green pixels that are part of a horizontal contiguous block.

**YAML Fact Block:**


```yaml
facts:
  - object: grid
    properties:
      - dimensions: 4x6 (rows x columns)
      - cell_values: [0, 3, 8]
  - object: pixel
    properties:
      - color:
        - 0: white
        - 3: green
        - 8: azure
      - location: [row, column]
  - action: replacement
    description: "Green (3) pixels are replaced by Azure (8) pixels under specific conditions."
    condition: "The green pixel is part of a horizontally contiguous sequence of green pixels."
  - relationship: contiguity
    description: "Pixels of the same color are considered contiguous if they are adjacent horizontally."
```


**Natural Language Program:**

1.  **Identify:** Examine the input grid and locate all pixels with the value '3' (green).
2.  **Check for Contiguity:** For each green pixel, check if it is part of a horizontal sequence of two or more contiguous green pixels.  A single, isolated green does not count, it must connect to another green.
3.  **Replace:** If a green pixel is part of such a horizontal sequence, replace its value with '8' (azure) in the output grid.
4. **Preserve otherwise:** All other pixels (those not meeting condition) retain their original values in the output grid.

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
