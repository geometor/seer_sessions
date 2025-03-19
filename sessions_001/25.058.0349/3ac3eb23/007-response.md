# 3ac3eb23 • 007 • example_2 • investigate_dreamer

---
Okay, let's analyze this example and break down the transformation.

**Perception of Elements:**

*   **Input Grid:** A 6x7 grid with mostly '0' (white) pixels and a single '4' (yellow) pixel in the top row.
*   **Output Grid:** A 6x7 grid with a vertical, alternating pattern of '4' (yellow) and '0' (white) pixels, originating from where the yellow pixel was in the input and mirroring 4 on it's immediate right neighbor .
*   **Transformation:** The single yellow pixel seems to trigger a vertical "stripe" pattern, alternating yellow and white, downwards. The yellow is mirrored on its neighbor.

**YAML Block (Facts):**



```yaml
objects:
  - type: grid
    dimensions: [6, 7]
    elements:
      - value: 0
        color: white
      - value: 4
        color: yellow
    properties:
        - static # input grid appears unchanged

  - type: grid
    dimensions: [6, 7]
    elements:
      - value: 0
        color: white
      - value: 4
        color: yellow
    properties:
        - dynamic # output grid is generated

actions:
  - type: propagate
    trigger:
      object: pixel
      value: 4
      color: yellow
    direction: vertical_down
    pattern: alternate
    values: [4,0]
  - type: mirror
    trigger:
      object: pixel
      value: 4
      color: yellow
    direction: right
    pattern: once

relationships:
  - type: spatial
    between: [input_grid, output_grid]
    description: output_grid is generated from input_grid based on location of a specific element
```



**Natural Language Program:**

1.  **Locate:** Find the single yellow (4) pixel in the input grid.
2. **Mirror:** From the found position, copy it on the immediate right neighbor, if the neighbor is 0.
3.  **Propagate:** From the found position, draw a vertical line downwards to the bottom of the grid.
4.  **Alternate:** The vertical line alternates between yellow (4) and white (0) pixels.
5. Mirror: From each newly generated pixel, copy it on the immediate right neighbor, if neighbor is 0.
6. all other are unchanged.


