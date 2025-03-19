# a3df8b1e • 014 • example_3 • investigate_coder

---

## Example 3

**input:**
```
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
1 0 0 0
```

<PIL.Image.Image image mode=RGB size=256x640 at 0x786C547D3450>

**output:**
```
0 0 0 1
0 0 1 0
0 1 0 0
1 0 0 0
0 1 0 0
0 0 1 0
0 0 0 1
0 0 1 0
0 1 0 0
1 0 0 0
```

<PIL.Image.Image image mode=RGB size=256x640 at 0x786C54B102D0>
Okay, here's my analysis of the provided example, formatted as a report:

**Perception of Elements:**

The task involves a transformation of a 2D grid of single-digit integers (representing colors) into another 2D grid of the same dimensions. The input grid predominantly consists of '0' (white) pixels, with a single '1' (blue) pixel in the bottom-left corner. The output grid retains the same dimensions but has the blue pixels arranged in a distinct pattern - a diagonal line running from the bottom-left to the top-right corner, with a sort of "cross" pattern alternating between rows and columns.

**YAML Fact Block:**


```yaml
facts:
  - type: grid
    description: Input and output are 2D grids of integers.
    dimensions: identical for input and output
  - type: pixel_values
    description: Pixel values range from 0 to 9, representing colors.
    dominant_value: 0 (white) in the input
  - type: object
    description: A single blue pixel (value 1) is the primary object of interest.
    input_location: Bottom-left corner (last row, first column).
  - type: transformation
    description: The blue pixel's position is transformed.
    output_pattern: a combination of diagonal line and cross-shape distribution

```


**Natural Language Program:**

1.  **Identify:** Locate the single blue pixel (value '1') in the input grid. In this specific example its in the lower left corner.
2. **Create Cross Pattern:** Create a pattern of alternating rows/columns of blue, starting in the bottom left corner and moving across the entire grid

The core concept is moving the "blue pixel" diagonally and create a cross pattern of rows/columns.

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
