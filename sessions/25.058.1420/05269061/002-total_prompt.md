# 05269061 • 002 • example_3 • investigate_coder

---

## train_1

**input:**
```
2 8 3 0 0 0 0
8 3 0 0 0 0 0
3 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=448x448 at 0x7A608C312490>

**output:**
```
2 8 3 2 8 3 2
8 3 2 8 3 2 8
3 2 8 3 2 8 3
2 8 3 2 8 3 2
8 3 2 8 3 2 8
3 2 8 3 2 8 3
2 8 3 2 8 3 2
```

<PIL.Image.Image image mode=RGB size=448x448 at 0x7A608C313610>

## train_2

**input:**
```
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 1
0 0 0 0 0 1 2
0 0 0 0 1 2 4
0 0 0 1 2 4 0
0 0 1 2 4 0 0
```

<PIL.Image.Image image mode=RGB size=448x448 at 0x7A608C3139D0>

**output:**
```
2 4 1 2 4 1 2
4 1 2 4 1 2 4
1 2 4 1 2 4 1
2 4 1 2 4 1 2
4 1 2 4 1 2 4
1 2 4 1 2 4 1
2 4 1 2 4 1 2
```

<PIL.Image.Image image mode=RGB size=448x448 at 0x7A608C312530>

## train_3

**input:**
```
0 0 0 0 8 3 0
0 0 0 8 3 0 0
0 0 8 3 0 0 0
0 8 3 0 0 0 4
8 3 0 0 0 4 0
3 0 0 0 4 0 0
0 0 0 4 0 0 0
```

<PIL.Image.Image image mode=RGB size=448x448 at 0x7A608C3131B0>

**output:**
```
4 8 3 4 8 3 4
8 3 4 8 3 4 8
3 4 8 3 4 8 3
4 8 3 4 8 3 4
8 3 4 8 3 4 8
3 4 8 3 4 8 3
4 8 3 4 8 3 4
```

<PIL.Image.Image image mode=RGB size=448x448 at 0x7A608C3127B0>
<PIL.Image.Image image mode=RGB size=1424x946 at 0x7A608CFC2170>Okay, let's analyze the provided examples to discern the transformation rule.

**Perception of Elements:**

The task involves 2D grids (matrices) where each cell contains a single digit integer (0-9), representing different colors. The transformation appears to involve replacing the zeros with a sequence of non-zero numbers. The non-zero values in input, do not appear in the same place in the output, rather they become the sequence of repeating non-zero digits.

**YAML Block (Facts):**


```yaml
objects:
  - grid: A 2D array of integers.
  - cell: An element within the grid, containing a single digit (0-9).
  - sequence:  A repeating pattern of non-zero digits extracted from the input grid.

properties:
  - grid_size:  The dimensions (rows x columns) of the grid.
  - cell_value: The integer value of a cell (representing a color).
  - non_zero_values: Set of digits in the input grid that aren't zero.

actions:
  - extract_sequence: Identify and order the unique non-zero digits from the input grid, it seems they are ordered numerically.
  - repeat_sequence:  Replicate the extracted sequence across the entire output grid, replacing 0 with repeating elements.

relationships:
  - input_to_sequence:  The non-zero values in the input grid define the repeating sequence in the output grid.
  - sequence_to_output: The sequence is used to fill all cells of the output grid, overwriting all original values.
```


**Natural Language Program:**

1.  **Extract Sequence:** Examine the input grid and identify all unique non-zero digits. Sort these digits numerically to form the repeating sequence.
2.  **Create Output Grid:** Create output grid that has same dimensions as the input grid.
3.  **Populate Output:** Iterate through the output grid, cell by cell. Populate all of the output grid cells by cycling through the elements of the extracted sequence, repeating the pattern. Ignore the input after extracting the sequence, all cells will contain repeating sequence items.

In simpler terms, the transformation identifies the unique non-zero digits in the input, orders them, and then uses this ordered sequence to completely fill the output grid, creating a repeating pattern that covers the entire grid.

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
