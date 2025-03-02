# 28e73c20 • 026 • example_4 • investigate_coder

---

## train_4

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=832x832 at 0x7CE4233083D0>

**output:**
```
3 3 3 3 3 3 3 3 3 3 3 3 3
0 0 0 0 0 0 0 0 0 0 0 0 3
3 3 3 3 3 3 3 3 3 3 3 0 3
3 0 0 0 0 0 0 0 0 0 3 0 3
3 0 3 3 3 3 3 3 3 0 3 0 3
3 0 3 0 0 0 0 0 3 0 3 0 3
3 0 3 0 3 3 3 0 3 0 3 0 3
3 0 3 0 3 0 0 0 3 0 3 0 3
3 0 3 0 3 3 3 3 3 0 3 0 3
3 0 3 0 0 0 0 0 0 0 3 0 3
3 0 3 3 3 3 3 3 3 3 3 0 3
3 0 0 0 0 0 0 0 0 0 0 0 3
3 3 3 3 3 3 3 3 3 3 3 3 3
```

<PIL.Image.Image image mode=RGB size=832x832 at 0x7CE4233087D0>
Okay, let's analyze this input-output pair.

**Perception of Elements:**

The input is a 13x13 grid filled entirely with zeros (white pixels). The output is a 13x13 grid with a complex pattern of threes (green pixels) and zeros (white pixels). The overall shape created by the green pixels resembles a stylized, hollow "X" with a thick border and a central square also made of green pixels.

**YAML Block (Facts):**


```yaml
facts:
  - input_grid:
      dimensions: 13x13
      elements:
        - value: 0
          color: white
  - output_grid:
      dimensions: 13x13
      elements:
        - value: 3
          color: green
        - value: 0
          color: white
  - transformation:
      type: pattern_replacement
      description: "A specific pattern of 0s is replaced by 3s, creating a shape."
  - object:
      shape_description: "hollow X with thick border and central square"
      color: green
      pixels: 3

```


**Natural Language Program:**

1.  **Initialize:** Start with the input grid, a 13x13 array filled with 0s.

2.  **Draw Outer Border:** Change the values of pixels on the perimeter of the grid to 3.

3. **Draw diagonals**: Change values of the pixels on both diagonals to 3, creating a large 'X'.

4. **Draw Inner Border.** Change values of the pixels to 3 for the inner and outer perimeter of the diagonals such that the diagonals become 3 pixels thick.

5. **Draw square**: Change the values of the pixels to 3 at the middle of the grid forming a 3x3 square.

6.  **Output:** The resulting grid is the output.

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
