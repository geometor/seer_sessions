# 7ddcd7ec • 003 • example_1 • investigate_dreamer

---
Okay, let's analyze this input-output pair.

**Perception of the Elements:**

The task involves a grid of pixels, initially mostly white (0) with a few green (3) pixels. The transformation seems to involve extending the green pixels diagonally downwards and to the right. The initial green pixels form a 2x2 square and a single isolated pixel. The transformation creates a diagonal line of green pixels originating from each initial green pixel, extending to the bottom-right edge of the grid.

**YAML Block (Facts):**



```yaml
objects:
  - type: pixel
    color: white (0)
    property: background
  - type: pixel
    color: green (3)
    property: foreground
  - type: grid
    property: container

actions:
  - type: extension
    direction: diagonal_down_right
    object: green pixel
    constraint: grid boundary

relationships:
  - green pixels are within the grid
  - extension starts from original green pixels
  - extension continues until grid boundary
```



**Natural Language Program:**

1.  **Identify** all green (3) pixels in the input grid.
2.  For each green pixel:
    *   **Extend** a diagonal line of green pixels downwards and to the right.
    *   Continue the extension until the edge of the grid is reached (either the bottom edge, the right edge, or both).
3. All other pixels should be set to 0.

