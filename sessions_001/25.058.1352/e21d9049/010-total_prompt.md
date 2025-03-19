# e21d9049 • 010 • example_2 • investigate_coder

---

## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 2 3 8 4 0 0 0
0 0 0 0 0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=896x960 at 0x7ACD21382DF0>

**output:**
```
0 0 0 0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 8 0 0 0 0 0
3 8 4 2 3 8 4 2 3 8 4 2 3 8
0 0 0 0 0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=896x960 at 0x7ACD21382990>
Okay, I'm ready to analyze this input-output pair and discern the transformation rule. Here's my report:

**Perception of Elements:**

*   The input and output are grids of size 15x14.
*   Most of the grid cells are filled with '0' (white).
*   The input grid contains a cluster of non-zero colored pixels in the center.
*    The input has single cells with colors yellow (4), azure(8), red(2), and green(3). The red, green, and azure colors are arranged in a horizontal line; a yellow cell is on top of the azure.
*   The output grid has a similar, but vertically elongated and mirrored structure. The 3 x 1 horizontal sequence of red, green, and azure becomes a 1 x 3 vertical sequence. The sequence is then duplicated (and include the yellow above the azure) across the entire vertical space of the output grid.

**YAML Block Documenting Facts:**


```yaml
facts:
  - object: grid
    properties:
      size: 15x14
      elements: integers (0-9) representing colors
  - object: cluster
    properties:
       location: center
       colors: [yellow(4), azure(8), red(2), green(3)]
    relation:  input cluster defines a seed for the output
  - action: transformation
    description: Elongate and duplicate the seed shape
    details: |
      The central cluster in the input is used as a basis. It contains the colors 4, 8, 2, and 3.
      These colors form a vertical line in the output, repeating.
      The horizontal '2 3 8 4' line is used as a basis, repeating down the center.
```


**Natural Language Program:**

1.  **Identify Seed:** Locate the contiguous non-zero pixels in the center of the input grid. Note the colors and their relative positions. Specifically, identify the horizontal sequence of red (2), green (3), and azure (8), and the yellow (4) positioned above the azure (8).

2.  **Vertical Elongation:** In the output grid, starting from the center row, replace the central column pixels. Transform the horizontal sequence '2 3 8' into a vertical sequence, with '2' at the bottom, '3' above it, and '8' above '3'. Place '4' (yellow) directly above '8'.

3. **Vertical Duplication**: Copy that vertical sequence of 2, 3, 8 and 4 in the center column of the output. Make copies up and down from the center. Make sure all the available rows in the output have pixels in the center defined in this color sequence.

4.  **Horizontal Duplication:** Duplicate this established 4-color pattern up to the available grid boundaries.

5. **Horizontal Seed Extension**: Create the horizontal sequence in the middle.

6. **Copy and Extend Vertically**: Extend to the available rows the sequence 3, 8, 4, 2.

7.  **Fill Remaining:** Leave all other cells in the output grid as '0' (white).

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
