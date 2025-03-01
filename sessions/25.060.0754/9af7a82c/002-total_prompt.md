# 9af7a82c • 002 • example_4 • investigate_coder

---

## train_1

**input:**
```
2 2 1
2 3 1
1 1 1
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x7A174C5BB1D0>

**output:**
```
1 2 3
1 2 0
1 2 0
1 0 0
1 0 0
```

<PIL.Image.Image image mode=RGB size=192x320 at 0x7A174C5BBA50>

## train_2

**input:**
```
3 1 1 4
2 2 2 4
4 4 4 4
```

<PIL.Image.Image image mode=RGB size=256x192 at 0x7A174C5B9550>

**output:**
```
4 2 1 3
4 2 1 0
4 2 0 0
4 0 0 0
4 0 0 0
4 0 0 0
```

<PIL.Image.Image image mode=RGB size=256x384 at 0x7A174C5B82D0>

## train_3

**input:**
```
8 8 2
3 8 8
3 3 4
3 3 4
```

<PIL.Image.Image image mode=RGB size=192x256 at 0x7A174C5B9E50>

**output:**
```
3 8 4 2
3 8 4 0
3 8 0 0
3 8 0 0
3 0 0 0
```

<PIL.Image.Image image mode=RGB size=256x320 at 0x7A174C5BA4D0>

## train_4

**input:**
```
1 1 1
2 2 1
2 8 1
2 8 1
```

<PIL.Image.Image image mode=RGB size=192x256 at 0x7A174C5B9250>

**output:**
```
1 2 8
1 2 8
1 2 0
1 2 0
1 0 0
1 0 0
```

<PIL.Image.Image image mode=RGB size=192x384 at 0x7A174C5BB950>
<PIL.Image.Image image mode=RGB size=1056x720 at 0x7A174C5BB650>Okay, here's my analysis of the provided input-output examples, focusing on elements, facts, and a natural language program describing the transformation.

**Perception of Elements:**

The core elements appear to be grids of single-digit integers, representing colored pixels.  The input grids seem to be smaller and more "dense" with non-zero values, while the output grids are larger, sparser (more zeros), and re-ordered. The output grid appears to "list" each unique digit found in the input, in reverse order.

**YAML Block (Facts):**


```yaml
objects:
  - input_grid:
      type: 2D array
      elements: integers (0-9)
      properties:
        rows: variable
        columns: variable
        colors: determined by integer values
  - output_grid:
      type: 2D array
      elements: integers (0-9)
      properties:
        rows: greater than or equal to input_grid rows
        columns: equal to input rows
        colors: determined by integer values

actions:
  - identify_unique_digits:
      input: input_grid
      output: ordered set of unique digits
  - reorder_digits: takes unique digits and puts them into reverse order
  - construct_output:
      input: ordered_digits, original input dimensions
      output: output_grid

relationships:
  - output_grid_columns: corresponds to sorted, reversed, unique values in the input_grid.
  - output_grid_rows: expands to height needed to accomodate listing of digits in column.
  - zero_padding: output_grid filled with zeros where no input digits map.
```


**Natural Language Program:**

1. **Examine** the input grid and identify all *unique* digits present, ignoring their original positions.
2. **Sort** this set of unique digits into descending order.
3. **Create** an output grid:
    - The number of *columns* in the output grid equals the number of unique digits in the input grid.
    - The number of *rows* of the first colum equals the columns + 1 of the input grid. The remaining columns have a height based on how many items are left to add.
4.  **Iterate** and list each item from the ordered set of digits into columns.
5. **Fill** the remaining cells of the output grid with zeros.

Essentially, the transformation extracts the unique digits, sorts them, and arranges them in reverse order vertically.

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
