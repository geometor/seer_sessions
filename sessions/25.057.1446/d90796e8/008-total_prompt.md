# d90796e8 • 008 • example_2 • investigate_coder

---

## Example 2

**input:**
```
5 0 0 0 0 0
0 0 3 2 0 0
0 0 0 0 0 0
0 3 0 0 0 2
0 2 0 0 0 0
5 0 0 3 0 0
0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=384x448 at 0x786C54B007D0>

**output:**
```
5 0 0 0 0 0
0 0 8 0 0 0
0 0 0 0 0 0
0 8 0 0 0 2
0 0 0 0 0 0
5 0 0 3 0 0
0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=384x448 at 0x786C54B01550>
Okay, here's my analysis of the provided example, focusing on perception, documenting facts, and creating a natural language program:

**Perception of Elements:**

*   **Grids:** The input and output are both 7x6 grids (7 rows, 6 columns).
*   **Colors:** The grids contain pixels of various colors, represented by numbers (0-9). The primary colors involved here seem to be white (0), gray (5), green (3), red (2), and azure (8).
*   **Objects**: Contiguous blocks of single color can be considered objects, for instance, the two gray(5) pixels at `[0,0]` and `[5,0]`
* **Change in color**: green (3) becomes azure (8)
* **Relative location**: The locations of the green (3) pixels that change to azure(8) are always adjacent to a red(2) pixel.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    dimensions: [7, 6]
    elements: pixels
    
  - type: pixel
    values: [0, 2, 3, 5, 8] # white, red, green, gray, azure

  - type: contiguous_block
    description: "one of more pixels of same color"

actions:
  - type: color_change
    from: 3  # Green
    to: 8    # Azure
    conditions:
      - adjacency_to: 2 # Red

relationships:
  - type: adjacency
    description: "Pixels directly next to each other (up, down, left, or right - not diagonally)."

```


**Natural Language Program:**

1.  **Identify** all pixels in the input grid that have the value 3 (green).
2.  **Check Adjacency:** For each green pixel, examine its immediate neighbors (up, down, left, and right).
3. **Conditional color change**: If a green pixel is directly adjacent to any pixel with value of 2 (red) on any of the four sides, change that green pixel's value to 8 (azure).
4.  **Preserve other pixels** All other pixels that are not a `3` adjacent to a `2` retain their original values.
5.  **Output:** Create the output grid with the modified pixel values.

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
