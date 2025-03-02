# be94b721 • 001 • all training • investigate_dreamer

---
Okay, let's analyze the provided examples to understand the transformation rule.

**Perception of Elements:**

The task involves 2D grids with single-digit integer values (0-9) representing different colors. The transformation seems to focus on extracting a specific colored object from the input grid and presenting it as the output grid, with the rest of the grid converted to 0. The extracted shapes are always solid rectangles and have the largest area compared to other colored object in the image.

**Facts (YAML):**



```yaml
objects:
  - name: input_grid
    type: 2D array
    properties:
      - values: integers (0-9)
      - colors: mapped to values (COLOR_MAP)

  - name: output_grid
    type: 2D array
    properties:
      - values: integers (0-9)
      - colors: mapped to values

  - name: target_object
    type: contiguous block
    properties:
      - color: single color
      - shape: rectangular
      - criteria: largest area among objects of distinct colors
      

actions:
  - name: identify_largest_object
    description: Find the largest contiguous rectangular block of a single color.
  - name: extract_object
    description: Create a new grid containing only the identified object.
  - name: pad_object
    description: replace all other values in new grid with 0

relationships:
  - input_grid contains multiple target_object instances
  - output_grid is a minimal representation of one target_object
  - output_grid is derived from the input_grid.

```



**Natural Language Program:**

1.  **Identify Objects:** Scan the input grid and identify all distinct contiguous rectangular regions of the same color.
2.  **Calculate Areas:** Determine the area (number of pixels) of each identified object.
3.  **Select Largest:** Find the object with the largest area.
4.  **Extract:** Create a new grid, copying only the pixels of the largest object, preserving its shape and relative position.
5.  **Isolate and output**: set every cell not part of the identified object in the new grid to 0 (white), the output grid shows only the largest object.


