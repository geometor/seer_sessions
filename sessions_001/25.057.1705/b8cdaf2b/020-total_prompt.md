# b8cdaf2b • 020 • example_4 • investigate_coder

---

## Example 4

**input:**
```
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 2 2 2 0 0
2 2 4 4 4 2 2
```

<PIL.Image.Image image mode=RGB size=448x448 at 0x7778516D1450>

**output:**
```
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
4 0 0 0 0 0 4
0 4 0 0 0 4 0
0 0 2 2 2 0 0
2 2 4 4 4 2 2
```

<PIL.Image.Image image mode=RGB size=448x448 at 0x777851398AF0>
Here's a report on my perception of the task, documented facts, and a natural language program describing the transformation:

**Perception:**

The task involves manipulating a grid of colored pixels. The primary colors involved seem to be white (0), red (2), and yellow (4). The transformation seems to involve a combination of identifying existing shapes and creating new ones based on their positions. The output grid retains the bottom two rows of the input grid and adds two new yellow (4) pixels above each original yellow (4) pixel on the border of red region.

**YAML Fact Representation:**


```yaml
facts:
  - observation: |
      The input grid contains a horizontal bar of red (2) pixels at the bottom row and a horizontal bar of yellow (4) pixels directly on top of it, and another bar of red pixels on top of the yellow pixels.
  - object: red_bar
    type: rectangle
    color: red (2)
    location: bottom row
    property: contiguous
  - object: yellow_bar
    type: rectangle
    color: yellow (4)
    location: above red_bar
    property: contiguous
  - object: upper_red_bar
    type: rectangle
    color: red
    location: above yellow_bar
    property: contiguous
  - action: create_yellow_pixels
    location: two rows above each original yellow (4) pixel adjacent to red.
    color: yellow (4)
  - rule: The bottom two rows remain the same.

```


**Natural Language Program:**

1.  **Copy:** Copy the bottom two rows of the input grid to the output grid.
2.  **Identify:** Locate all yellow (4) pixels within the copied region.
3. **Create:** Two rows above, for each identified yellow pixel which is adjacent to red pixel vertically or horizontally, change the corresponding pixel to value 4.
4. If the original yellow pixel does not has red neighbor vertically or horizontally, do nothing for that pixel.


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
