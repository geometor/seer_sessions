# e509e548 • 004 • example_1 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0
0 0 0 3 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 3 3 0 0 0 0 0 3 3 3 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 0 0 0
0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0
0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 0 0 0
3 3 3 3 0 0 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 3 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 3 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 3 0 3 0 0 0
0 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0
```

<PIL.Image.Image image mode=RGB size=1344x1216 at 0x716635C4CA50>

**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0
0 0 0 2 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 2 0 0 0 0 0 6 6 6 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 6 6 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 6 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 6 0 0 0
2 2 2 2 0 0 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 6 6 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 6 0 0 0
0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 6 0 6 0 0 0
0 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 0 0
```

<PIL.Image.Image image mode=RGB size=1344x1216 at 0x716635C5E0D0>
Okay, here's my analysis of the provided input-output example, formatted as a report:

**Perception of Elements:**

The task involves a grid of pixels, each with a color value from 0 to 9. The input grid contains green (3) pixels forming various shapes, some isolated, some connected. The output grid appears to have a corresponding color for each green object in the input, with connected components of green seemingly grouped and represented with unique colors. The background (0) remains unchanged.

**YAML Fact Block:**


```yaml
facts:
  - observation: Input grid contains pixels of colors 0 (white) and 3 (green).
  - observation: Output grid contains pixels of colors 0 (white), 1 (blue), 2 (red), and 6 (magenta).
  - object_type: GreenComponent
    properties:
      color: 3
      pixels: List[Tuple[int, int]]  # List of (row, col) coordinates
      connected: bool                 # True if pixels form a connected component
  - relationship: Input green components map to output colored components.
  - relationship: Each connected green component in the input is represented by a unique color in the output.
  - action: ColorMapping
    input: GreenComponent
    output_color: int # Determined based on connectivity and possibly a sequential assignment
  - background: Background color 0 remains unchanged in both input and output.
```


**Natural Language Program:**

1.  **Identify Green Components:** Scan the input grid and identify all contiguous groups (connected components) of green (3) pixels. Consider two green pixels adjacent if they share a side (not just a corner).
2.  **Assign Output Colors:** For each *distinct* green connected component identified:
    *   If a component consists of a single, isolated green pixel, map the pixel in the output with the color blue (1).
    *   If the component has multiple horizontally or vertically adjacent green pixels, find the top left pixel within each unique component and map the component with red (2) if top left's column index is less than 5 else map it with color magenta(6).
3.  **Preserve Background:** All white (0) pixels in the input remain white (0) in the output.

In summary, the transformation detects connected components of green pixels and replaces each distinct component by a unique color, with single-pixel components being blue, and multi-pixel components being represented by red or magenta based on its location. The background remains unchanged.

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
