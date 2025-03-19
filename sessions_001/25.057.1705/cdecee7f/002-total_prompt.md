# cdecee7f • 002 • example_1 • investigate_coder

---

## Example 1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 1 0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 9
0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7778515B6170>

**output:**
```
3 1 8
9 7 6
0 0 0
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x7778516D14F0>
Okay, here's a breakdown of my observations and a proposed natural language program for the transformation:

**Perception of Elements:**

*   The input is a 10x10 grid.
*   The output is a 3x3 grid.
*   The input grid contains single, non-zero, colored pixels, sparsely distributed. The rest of the pixels are white (0).
*   The output grid seems to contain the non-zero pixels from the input grid, rearranged.
*	The colors of the non-zero pixels are preserved during transformation.
*	The output grid contains 3 rows, and some rows could be empty.
*   It appears the non-zero values are extracted and arranged into a smaller grid, possibly based on their original positions relative to each other, but it isn't simply cropping or translating a region of the original.

**YAML Block (Facts):**


```yaml
facts:
  - type: grid
    description: Input grid
    dimensions: 10x10
    elements: integers (0-9 representing colors)
  - type: grid
    description: Output grid
    dimensions: 3x3
    elements: integers (0-9 representing colors)
  - type: object
    description: Non-zero pixels
    property: color (determined by integer value)
    property: position (row, column in the input grid)
  - type: operation
    description: Extraction and Rearrangement
    details: Non-zero pixels from the input are placed in the output grid, maintaining color.
  - type: observation
    description: Output grid rows order could relate to the values of the input
```


**Natural Language Program:**

1.  **Identify** all non-zero pixels in the input grid. Record their values (colors) and their original (row, column) positions.

2. **Sort** these non-zero pixels in descending order first according to input row, and in the event of matching rows, ascending by color/value.

3. **Create** empty rows in the output grid.

4.  **Populate Output** the output grid with the sorted pixels starting from index 0, top to bottom, left to right.

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
