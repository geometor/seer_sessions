# b527c5c6 • 004 • example_1 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 0 0 0 0 0
0 0 0 3 3 0 0 0 0 0
0 0 0 2 3 0 3 3 3 3
0 0 0 3 3 0 3 3 2 3
0 0 0 3 3 0 0 0 0 0
0 0 0 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7FC25B70BF50>

**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 0 0 0 0 0
3 3 3 3 3 0 0 0 0 0
2 2 2 2 3 0 3 3 3 3
3 3 3 3 3 0 3 3 2 3
0 0 0 3 3 0 0 3 2 3
0 0 0 3 3 0 0 3 2 3
0 0 0 0 0 0 0 3 2 3
0 0 0 0 0 0 0 3 2 3
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7FC25B709450>
Okay, let's analyze this input-output pair to understand the transformation.

**Perception of Elements:**

*   **Input:** A 10x10 grid with a central "cross" shape made of green (3) pixels. There are two red (2) pixels within the green cross. The rest of the grid is white (0).
*   **Output:** A 10x10 grid. The green cross shape seems to have expanded, especially vertically. The red pixels seem to have influenced the expansion, possibly duplicating themselves above and below, and to the sides, of the original red pixels.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    dimensions: 10x10
    elements: pixels
    
  - type: pixel
    values:
      - color: white
        value: 0
      - color: green
        value: 3
      - color: red
        value: 2

  - type: shape
    name: cross
    color: green
    initial_position: centered

actions:
  - name: expansion
    object: cross
    direction: vertical and horizontal, influenced by red pixels.
    
  - name: duplication
    object: red pixel

relationships:
  - red pixels are inside the green cross
  - red pixel positions seem to define the expansion of the green pixels.

```


**Natural Language Program:**

1.  **Identify Objects:** Find the green (3) "cross" shape and the red (2) pixels within it.
2.  **Red Pixel Duplication:** The red pixels are duplicated. For each original red pixel in the input, create four more copies in the output: One directly above, one directly below, one to the left, and one to the right. If green occupies the copy location, maintain green, only copy to white space.
3.  **Green Cross Expansion:** The green cross expands. From each exist green pixel, examine the spaces to it's left and right, and duplicate if white.
4. **Vertical Fill:** From each green pixel on the cross, scan upwards and downwards to any 0 and replace with a 3. Stop before other non-zero pixels.

In summary, the red pixels are duplicated around their original positions, creating new red pixels. The green cross expands left and right and then upward and downwards.

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
