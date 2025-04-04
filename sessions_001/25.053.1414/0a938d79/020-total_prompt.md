# 0a938d79 • 020 • example_4 - CODE

---

# Example

**input:**
```
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=512x1536 at 0x7D261845B9D0>

**output:**
```
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
4 4 4 4 4 4 4 4
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
4 4 4 4 4 4 4 4
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
4 4 4 4 4 4 4 4
```

<PIL.Image.Image image mode=RGB size=512x1536 at 0x7D26184F12A0>
Okay, here's my analysis of the provided example input-output pair, formatted as requested:

**Perception of Task Elements:**

The task involves 2D grids containing numerical values representing colors. The primary colors observed are white (0), yellow (4), and blue (1). The transformation seems to involve replicating rows containing non-zero values and potentially stacking these replicated rows based on a specific pattern. The input grid contains single rows of yellow and blue, while the output consists of multiple, stacked rows of yellow and blue.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    properties:
      dimensions: [24, 8] # Height x Width
      colors: [0, 1, 4]
      rows:
        - row_index: 7
          color: 4 #yellow
          elements: [4, 0, 0, 0, 0, 0, 0, 0]
        - row_index: 11
          color: 1 # blue
          elements: [1, 0, 0, 0, 0, 0, 0, 0]

actions:
  - type: replication
    description: Rows with non-zero colors are replicated.
  - type: stacking
    description: Replicated rows are stacked, potentially repeating the pattern.

relationships:
  - type: spatial
    description: The spatial relationship between the original colored rows and the replicated rows is important. The single yellow row becomes three sets of yellow rows, and single blue row becomes two sets of blue rows in the output.

```


**Natural Language Program:**

1.  **Identify Target Rows:** Examine each row of the input grid. Identify rows that contain a non-zero value (in this case, rows with yellow (4) and blue (1)).

2.  **Replicate Rows:** For each identified target row:
    *   Replicate the row *n* times. *n* is determined for each input row. The yellow row appears to be replicated 4 times per stack, and the blue 4 times as well. There appear to be a total of 3 stacks for the yellow, and 2 for the blue

3.  **Stack Replicated Rows:** Create "stacks" of the replicated rows.

4. **Arrange Stacked Rows:** order the stacks according to the order they were found.

5. **Assemble Output Grid:** the final output is obtained by combining the identified stacks.

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
