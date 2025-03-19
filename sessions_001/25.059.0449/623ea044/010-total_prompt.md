# 623ea044 • 010 • example_2 • investigate_coder

---

## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=960x960 at 0x7440707B07D0>

**output:**
```
0 0 0 0 0 0 7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 0 0 0 0 0 7
0 0 0 0 0 0 0 0 0 7 0 0 0 7 0
0 0 0 0 0 0 0 0 0 0 7 0 7 0 0
0 0 0 0 0 0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0 0 7 0 7 0 0
0 0 0 0 0 0 0 0 0 7 0 0 0 7 0
0 0 0 0 0 0 0 0 7 0 0 0 0 0 7
0 0 0 0 0 0 0 7 0 0 0 0 0 0 0
0 0 0 0 0 0 7 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 0 0 0 0 0 0
0 0 0 0 7 0 0 0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=960x960 at 0x7440707B1250>
Okay, let's analyze this input-output pair.

**Perception of Elements:**

The input is a 15x15 grid where almost all pixels are black (0), except for a single orange (7) pixel near the center-right. The output is also a 15x15 grid, but it contains a diagonal line of orange (7) pixels running from the top-center-right to the bottom-left, effectively "mirroring" and repeating the original orange pixel, as well as a reverse diagonal, or cross, centered on the original 7.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    dimensions: 15x15
    elements: pixels
    
  - type: pixel
    color_values: [0, 7]
    colors: [black, orange]
    initial_state:
      - color: orange
        position: (5, 11) # row, col (0-indexed)
    final_state:
      - color: orange
        positions_created:  #diagonal line positions
          - (0,6)
          - (1,7)
          - (2,8)
          - (3,9)
          - (4,10)
          - (5,11)
          - (6,10)
          - (7,9)
          - (8,8)
          - (9,7)
          - (10,6)
          - (11,5)
          - (12,4)
          - (13,3)
          - (14,2)

actions:
  - type: mirror_and_repeat
    object: pixel
    axis: diagonal # from top-left to bottom-right, and top-right to bottom left
    color_to_copy: 7

relationships:
    - type: contains
      subject: grid
      object: pixels

```


**Natural Language Program:**

1.  **Identify the Key Pixel:** Locate the single orange (7) pixel in the input grid.
2.  **Create diagonals:** From the orange pixel, create pixels of the same color along a diagonal extending from the identified pixel and reflecting the original 7, repeating outwards in each direction.
3.  **Output Grid:** The output grid retains the same dimensions as the input grid. All other pixels remain black (0).

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
