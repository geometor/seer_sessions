# 6455b5f5 • 010 • example_2 • investigate_coder

---

## train_2

**input:**
```
0 0 0 0 2 0 0 0 0 0 0 0 0
0 0 0 0 2 2 2 2 2 2 2 2 2
0 0 0 0 2 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0 0 0
2 2 2 2 2 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=832x704 at 0x7B4BFE17A550>

**output:**
```
0 0 0 0 2 8 8 8 8 8 8 8 8
0 0 0 0 2 2 2 2 2 2 2 2 2
0 0 0 0 2 1 1 1 1 1 1 1 1
0 0 0 0 2 1 1 1 1 1 1 1 1
0 0 0 0 2 1 1 1 1 1 1 1 1
2 2 2 2 2 1 1 1 1 1 1 1 1
0 0 0 0 2 1 1 1 1 1 1 1 1
0 0 0 0 2 1 1 1 1 1 1 1 1
0 0 0 0 2 1 1 1 1 1 1 1 1
0 0 0 0 2 1 1 1 1 1 1 1 1
0 0 0 0 2 1 1 1 1 1 1 1 1
```

<PIL.Image.Image image mode=RGB size=832x704 at 0x7B4C05B57250>
Okay, let's analyze this input-output example.

**Perception of Elements:**

The task involves a grid of colored pixels. The primary colors involved are white (0), red (2), azure (8) and blue (1). The input grid seems to have a "cross" shape formed by red pixels on a white background. The output grid maintains the red cross but changes some of the surrounding white pixels. Specifically, white pixels to the right of the vertical red line change to azure, and the rest of the white pixels change to blue.

**YAML Block (Facts):**


```yaml
objects:
  - id: red_cross
    type: shape
    color: red (2)
    description: A cross shape formed by contiguous red pixels.
  - id: background
    type: area
    color:
      - initial: white (0)
      - final_top_right: azure (8)
      - final_other: blue (1)
    description:  The area surrounding the red cross, initially white, changes to azure and blue based on position relative to the cross.

actions:
  - name: color_change
    target: background
    parameters:
      color_map:
        right_of_vertical_red: azure (8)
        other: blue (1)
    description: Changing the color of the background based on its relative position to the red cross.

relationships:
   - type: spatial
     description: The background is divided based on its position relative to the vertical arm of the red_cross. Right of the vertical is colored azure, and the remaining white pixels are blue.

```


**Natural Language Program:**

1.  **Identify the "red cross":** Locate the contiguous red (2) pixels forming a cross shape.
2.  **Divide the background:** Divide remaining area, all initially white (0), into different sections, based on a vertical boundary defined by the vertical arm of the red cross.
3. **Change Colors.**
      *   Pixels to the right of the red cross's vertical arm change to azure (8).
    *   All other pixels previously white (0) change to blue (1)

In summary, the transformation maintains the red cross and recolors the background based on its position relative to the red cross's vertical arm.

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
