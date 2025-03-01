# c9e6f938 • 002 • example_3 • investigate_coder

---

## train_1

**input:**
```
0 7 0
0 0 7
0 7 7
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x7F4C1B75DCD0>

**output:**
```
0 7 0 0 7 0
0 0 7 7 0 0
0 7 7 7 7 0
```

<PIL.Image.Image image mode=RGB size=384x192 at 0x7F4C1B67E150>

## train_2

**input:**
```
0 0 0
0 7 7
0 0 0
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x7F4C1B67F8D0>

**output:**
```
0 0 0 0 0 0
0 7 7 7 7 0
0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=384x192 at 0x7F4C1B67E6D0>

## train_3

**input:**
```
0 0 0
7 0 0
0 0 0
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x7F4C1B67E3D0>

**output:**
```
0 0 0 0 0 0
7 0 0 0 0 7
0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=384x192 at 0x7F4C2318BCD0>
<PIL.Image.Image image mode=RGB size=1280x464 at 0x7F4C1B74F9D0>Okay, let's analyze the provided input-output examples to discern the transformation rule.

**Perception of Elements:**

The task involves 2D grids containing numerical values representing colors. The primary color observed is '0' (white) and '7' (orange). The transformation seems to involve expanding the orange (7) regions horizontally, sometimes with a mirroring effect. The dimensions of the grid also change.

**YAML Block (Facts):**


```yaml
objects:
  - name: grid
    type: 2D array
    properties:
      - rows: variable
      - columns: variable
      - values: [0, 7] # white and orange

  - name: orange_region
    type: contiguous block of '7's
    properties:
      - shape: variable (can be a single cell or a horizontal line)

actions:
  - name: expand_horizontally
    description: The orange region grows in the horizontal direction.
  - name: mirror
    description: The orange region expands in the opposite direction as well in some cases.

relationships:
  - orange_region is contained within grid
```


**Natural Language Program:**

1.  **Identify** the orange region(s) within the input grid. An orange region is defined as one or more adjacent cells with the value '7'.

2.  **Determine the expansion factor**: Observe how the orange regions from the input map onto the output.
    *   In example 1, a single '7' expands to two '7's, two '7' adjacent expands to four '7's
    *   In example 2, two '7's expand into four '7's
    *   In example 3, a single '7' expands into two, mirrored.

3. **Expand**:
    *   If there exists at least one '7':
        1.  Double each sequence of adjacent '7's horizontally.

4.  **Mirror**
    *   If, after doubling, there are no adjacent '7's, fill the available locations with a mirrored set.

5. **Adjust the Grid:**
    1. The final width is double the original if there were no adjacent 7s in input and input.width + number\_of\_7s - 1
    2. The final height is same as the input.
    3. Insert 0 to fill the added space if any.

In summary, the transformation duplicates the orange regions horizontally, and in case where 7s were single they are mirror in addition to being doubled. The grid's width doubles or expands in size according the expansion of 7s, and it will be filled with 0.

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
